import random
import smtplib
from email.message import EmailMessage

from elrahapi import database
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.authentication.authentication_router_provider import (
    AuthenticationRouterProvider,
)
from elrahapi.authentication.token import FullTempToken, TempToken, TokenType
from elrahapi.database.session_manager import SessionManager
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.router.route_additional_config import (
    AuthorizationConfig,
    ResponseModelConfig,
)
from elrahapi.router.route_config import RouteConfig
from elrahapi.router.router_namespace import USER_AUTH_CONFIG_ROUTES
from elrahapi.router.router_routes_name import DefaultRoutesName
from elrahapi.user.schemas import UserLoginRequestModel
from elrahapi.utility.types import ElrahSession
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from redis import Redis

from fastapi import Depends, status


class OTPAuthManager(AuthenticationManager):

    def __init__(
        self,
        session_manager: SessionManager,
        redis: Redis,
        smtp_email: str,
        smtp_password: str,
        opt_expire_time: int,
        secret_key: str | None = None,
        algorithm: str | None = None,
        refresh_token_expiration: int | None = None,
        access_token_expiration: int | None = None,
        temp_token_expiration: int | None = None,
        security: OAuth2PasswordBearer | HTTPBearer | None = None,
    ):
        super().__init__(
            session_manager=session_manager,
            secret_key=secret_key,
            algorithm=algorithm,
            refresh_token_expiration=refresh_token_expiration,
            access_token_expiration=access_token_expiration,
            temp_token_expiration=temp_token_expiration,
            security=security,
        )
        self.redis = redis
        self.otp_expire_time=opt_expire_time
        self.smtp_email=smtp_email
        self.smtp_password=smtp_password

    def generate_otp(self) -> str:
        otp = str(random.randint(100000, 999999))
        return otp

    def get_logout_user_sub(self, token: str):
        return super().get_sub_from_token(token=token)

    def validate_token(self, token: str):
        my_token = super().validate_token(token)
        sub = None
        if my_token is not None:
            sub = my_token.get("sub")
        blacklisted_token = self.redis.get(f"token:{sub}") if sub else None
        if blacklisted_token and token == blacklisted_token:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide"
            )
        return my_token

    def send_otp_mail(self, user_email: str, otp: str):
        msg = EmailMessage()
        msg["Subject"] = "CODE OTP"
        msg["To"] = user_email
        msg.set_content(f"Code OTP : {otp}")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.smtp_email, self.smtp_password)
            smtp.send_message(msg)


class OTPAuthRouterProvider(AuthenticationRouterProvider):
    def __init__(
        self,
        authentication: OTPAuthManager,
        read_with_relations: bool | None = False,
        roles: list[str] | None = None,
        privileges: list[str] | None = None,
    ):
        super().__init__(
            authentication=authentication,
            read_with_relations=read_with_relations,
            roles=roles,
            privileges=privileges,
        )

    def get_auth_router(
        self,
        init_data: list[RouteConfig] = USER_AUTH_CONFIG_ROUTES,
        authorizations: list[AuthorizationConfig] | None = None,
        exclude_routes_name: list[DefaultRoutesName] | None = None,
        response_model_configs: list[ResponseModelConfig] | None = None,
    ):
        authentication_router = super().get_auth_router(
            init_data=init_data,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name + [DefaultRoutesName.LOGIN],
            response_model_configs=response_model_configs,
        )

        @authentication_router.post("/login", response_model=FullTempToken)
        async def login(
            usermodel: UserLoginRequestModel,
            session: ElrahSession = Depends(database.session_manager.yield_session),
        ):
            otp = self.authentication.generate_otp()
            login_sub = usermodel.sub
            user = await self.authentication.authenticate_user(
                session=session, password=usermodel.password, sub=login_sub
            )
            sub = getattr(
                user, self.authentication.authentication_models.primary_key_name
            )
            key = f"otp:{sub}"
            self.authentication.redis.set(key, otp, ex=self.authentication.opt_expire_time)
            self.authentication.send_otp_mail(
                otp=otp,
                user_email=user.email)
            temp_token_data = {"sub": str(sub), "email": user.email}
            temp_token: TempToken = self.authentication.create_token(
                data=temp_token_data, token_type=TokenType.TEMP_TOKEN
            )
            full_temp_token = FullTempToken(
                temp_token=temp_token["temp_token"],
                token_type=temp_token["token_type"],
                message="OTP envoyé par email",
                status="pending_2fa",
            )
            return full_temp_token
