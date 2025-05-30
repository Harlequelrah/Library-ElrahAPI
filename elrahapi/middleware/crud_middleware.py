import json
import time
from elrahapi.database.session_manager import SessionManager
from fastapi import Request,status
from starlette.responses import Response
from  elrahapi.websocket.connection_manager import ConnectionManager
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
async def get_response_and_process_time(request:Request,call_next=None,response:Response=None):
    if call_next is None:
        process_time = (
            time.time() - request.state.start_time
            if hasattr(request.state, "start_time")
            else None
        )
        return [response,process_time]
    else:
        start_time=time.time()
        current_response = await call_next(request)
        process_time=time.time() - start_time
    return [current_response,process_time]

async def save_log(
    request: Request,LogModel, session_manager:SessionManager ,call_next=None,error=None,response:Response=None,websocket_manager:ConnectionManager=None
):
    if request.url.path in ["/openapi.json", "/docs", "/redoc", "/favicon.ico","/"]:
        if call_next is None:
            return
        else : return await call_next(request)
    response,process_time= await get_response_and_process_time(request,call_next,response)
    if error is None and (response.status_code <200 or response.status_code > 299)  :
        error = await read_response_body(response)
    log = LogModel(
    process_time=process_time,
    status_code=response.status_code,
    url=str(request.url),
    method=request.method,
    error_message=error,
    remote_address=str(request.client.host)
    )
    try :
        session = await session_manager.get_session()
        session.add(log)
        await session_manager.commit_and_refresh(
            session=session,
            object=log
            )
        if error is not None and websocket_manager is not None:
            message=f"An error occurred during the request with the status code {response.status_code}, please check the log {log.id} for more information"
            if websocket_manager is not None:
                await websocket_manager.broadcast(message)
        return response
    except Exception as err:
        await session_manager.rollback_session(session)
        error_message= f"error : An unexpected error occurred during saving log , details : {str(err)}"
        raise_custom_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
    finally :
        await session_manager.close_session(session)


async def read_response_body(response: Response)  -> str | None:
    """Capture, décode le corps de la réponse et extrait la valeur du champ 'detail'."""
    body = b""
    if response.body_iterator:
        async for chunk in response.body_iterator:
            body += chunk
        # Réinitialise l'itérateur pour un usage futur
        response.body_iterator = recreate_async_iterator(body)

    # Décoder en UTF-8
    decoded_body = body.decode("utf-8")

    # Vérifier si 'detail' est présent
    try:
        body_json = json.loads(decoded_body)
        if isinstance(body_json, dict) and "detail" in body_json:
            return str(body_json["detail"])
    except json.JSONDecodeError:
        # Si le corps n'est pas du JSON valide
        pass
    return None



async def recreate_async_iterator(body: bytes):
    """Crée un nouvel itérateur asynchrone pour la réponse."""
    for chunk in [body]:
        yield chunk
