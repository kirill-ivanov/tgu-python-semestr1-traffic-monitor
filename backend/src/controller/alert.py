from typing import Optional
from fastapi import APIRouter
from db.dao import *

router = APIRouter(prefix="/api/alert")


@router.get("")
def list_alert(type: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None):
    if type == 'all':
        type = None
    return {"result": filter_alert(type, date_from, date_to)}
