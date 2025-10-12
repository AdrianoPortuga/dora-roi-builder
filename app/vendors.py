from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..security_rbac import require_permissions

router = APIRouter(prefix="/vendors", tags=["vendors"])

class VendorIn(BaseModel):
    name: str
    country: str | None = None
    criticality: str | None = None

# Exemplo: apenas quem tem vendors:read pode listar
@router.get("/", dependencies=[Depends(require_permissions("vendors:read"))])
def list_vendors():
    return [
        {"id": 1, "name": "Acme Cloud", "country": "PT", "criticality": "high"},
        {"id": 2, "name": "DataSafe Ltd", "country": "BR", "criticality": "medium"},
    ]

# Exemplo: criar exige vendors:write
@router.post("/", dependencies=[Depends(require_permissions("vendors:write"))])
def create_vendor(v: VendorIn):
    return {"id": 999, **v.model_dump()}
