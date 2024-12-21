from fastapi.responses import JSONResponse
from sqlalchemy import func
from harlequelrah_fastapi.authorization.privilege_model import Privilege, PrivilegeCreate, PrivilegeUpdate
from harlequelrah_fastapi.utility.utils import update_entity
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, status
