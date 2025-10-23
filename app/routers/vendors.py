from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.vendor import Vendor  # ajuste se seu modelo estiver em outro caminho
from app.models.user import User

router = APIRouter(prefix="/vendors", tags=["vendors"])

# Schemas simples (evita dependência de schemas externos)
class VendorIn(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    country: Optional[constr(strip_whitespace=True, min_length=2, max_length=3)] = None
    criticality: Optional[constr(strip_whitespace=True)] = None

class VendorOut(BaseModel):
    id: int
    name: str
    country: Optional[str] = None
    criticality: Optional[str] = None

    class Config:
        from_attributes = True  # pydantic v2

@router.get("/", response_model=List[VendorOut])
def list_vendors(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.query(Vendor).order_by(Vendor.id.asc()).all()

@router.post("/", response_model=VendorOut, status_code=status.HTTP_201_CREATED)
def create_vendor(
    payload: VendorIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = Vendor(name=payload.name, country=payload.country, criticality=payload.criticality)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

@router.get("/{vendor_id}", response_model=VendorOut)
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = db.get(Vendor, vendor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendor não encontrado")
    return v

@router.put("/{vendor_id}", response_model=VendorOut)
def update_vendor(
    vendor_id: int,
    payload: VendorIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = db.get(Vendor, vendor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendor não encontrado")
    v.name = payload.name
    v.country = payload.country
    v.criticality = payload.criticality
    db.commit()
    db.refresh(v)
    return v

@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = db.get(Vendor, vendor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendor não encontrado")
    db.delete(v)
    db.commit()
    return None
