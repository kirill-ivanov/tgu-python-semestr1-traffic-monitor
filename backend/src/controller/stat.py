from typing import Optional
from fastapi import APIRouter
from db.dao import *

router = APIRouter(prefix="/api/stat")


@router.get("")
def list_stat(type: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None,
              group: Optional[str] = None):
    if group is None or group == "no":
        return {"result": filter_stat(type, date_from, date_to)}
    else:
        return {"result": group_stat(type, group, date_from, date_to)}


@router.get("/last")
def last():
    return last_stat()
