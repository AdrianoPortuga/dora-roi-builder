# app/routers/vendors.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.security import get_current_user

router = APIRouter()

# ===== Schemas =====
class VendorBase(BaseModel):
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2, max_length=2)  # ISO-2 (ex.: BR, PT)
    criticality: str = Field(..., pattern="^(low|medium|high)$")

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int

# ===== “DB” em memória para os testes =====
VENDORS_DB: list[Vendor] = [
    Vendor(id=1, name="NovaCo", country="BR", criticality="low"),
]
_next_id = 2

def _next() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

# ===== Rotas (todas protegidas por Bearer) =====
@router.get("/", response_model=List[Vendor])
def list_vendors(_: dict = Depends(get_current_user)):
    return VENDORS_DB

@router.post("/", response_model=Vendor, status_code=status.HTTP_201_CREATED)
def create_vendor(payload: VendorCreate, _: dict = Depends(get_current_user)):
    vendor = Vendor(id=_next(), **payload.model_dump())
    VENDORS_DB.append(vendor)
    return vendor

@router.get("/{vendor_id}", response_model=Vendor)
def get_vendor(vendor_id: int, _: dict = Depends(get_current_user)):
    for v in VENDORS_DB:
        if v.id == vendor_id:
            return v
    raise HTTPException(status_code=404, detail="Vendor não encontrado")

@router.put("/{vendor_id}", response_model=Vendor)
def update_vendor(vendor_id: int, payload: VendorBase, _: dict = Depends(get_current_user)):
    for i, v in enumerate(VENDORS_DB):
        if v.id == vendor_id:
            updated = Vendor(id=vendor_id, **payload.model_dump())
            VENDORS_DB[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Vendor não encontrado")

@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: int, _: dict = Depends(get_current_user)):
    global VENDORS_DB
    before = len(VENDORS_DB)
    VENDORS_DB = [v for v in VENDORS_DB if v.id != vendor_id]
    if len(VENDORS_DB) == before:
        raise HTTPException(status_code=404, detail="Vendor não encontrado")
    return
