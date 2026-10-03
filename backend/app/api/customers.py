from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.auth import Role, require_roles
from app.core.database import get_db
from app.models.customer import Customer, CustomerLocation
from app.models.device import Device
from app.schemas.customer import CustomerCreate, CustomerLocationCreate, CustomerLocationRead, CustomerRead, CustomerUpdate
router = APIRouter(prefix="/api/v1/customers", tags=["customers"])
def _validate_device(device_id: int | None, db: Session) -> None:
    if device_id is not None and not db.get(Device, device_id):
        raise HTTPException(422, "Linked device not found")
@router.post("", response_model=CustomerRead, status_code=201, dependencies=[Depends(require_roles(Role.ADMIN, Role.TECHNICIAN))])
def create_customer(body: CustomerCreate, db: Session = Depends(get_db)):
    if db.query(Customer).filter(Customer.customer_code == body.customer_code).first():
        raise HTTPException(409, "Customer code already exists")
    _validate_device(body.device_id, db)
    customer = Customer(**body.model_dump())
    db.add(customer); db.commit(); db.refresh(customer)
    return customer
@router.get("", response_model=list[CustomerRead], dependencies=[Depends(require_roles(Role.ADMIN, Role.TECHNICIAN))])
def list_customers(q: str | None = Query(default=None, max_length=160), db: Session = Depends(get_db)):
    query = db.query(Customer).order_by(Customer.id)
    if q:
        pattern = f"%{q}%"
        query = query.filter(Customer.customer_code.ilike(pattern) | Customer.name.ilike(pattern) | Customer.phone.ilike(pattern) | Customer.pppoe_username.ilike(pattern))
    return query.all()
@router.get("/{customer_id}", response_model=CustomerRead, dependencies=[Depends(require_roles(Role.ADMIN, Role.TECHNICIAN))])
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer: raise HTTPException(404, "Customer not found")
    return customer
@router.patch("/{customer_id}", response_model=CustomerRead, dependencies=[Depends(require_roles(Role.ADMIN, Role.TECHNICIAN))])
def update_customer(customer_id: int, body: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer: raise HTTPException(404, "Customer not found")
    _validate_device(body.device_id, db)
    values = body.model_dump(exclude_unset=True)
    if "customer_code" in values:
        duplicate = db.query(Customer).filter(Customer.customer_code == values["customer_code"], Customer.id != customer_id).first()
        if duplicate: raise HTTPException(409, "Customer code already exists")
    for key, value in values.items(): setattr(customer, key, value)
    db.commit(); db.refresh(customer); return customer
@router.delete("/{customer_id}", status_code=204, dependencies=[Depends(require_roles(Role.ADMIN))])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer: raise HTTPException(404, "Customer not found")
    db.delete(customer); db.commit()
@router.post("/{customer_id}/location", response_model=CustomerLocationRead, dependencies=[Depends(require_roles(Role.ADMIN, Role.TECHNICIAN))])
def update_customer_location(customer_id: int, body: CustomerLocationCreate, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer: raise HTTPException(404, "Customer not found")
    captured = body.captured_at or datetime.utcnow()
    location = CustomerLocation(customer_id=customer_id, latitude=body.latitude, longitude=body.longitude, accuracy_m=body.accuracy_m, source=body.source, captured_at=captured)
    customer.latitude=body.latitude; customer.longitude=body.longitude; customer.location_accuracy_m=body.accuracy_m; customer.location_source=body.source; customer.location_updated_at=captured
    db.add(location); db.add(customer); db.commit(); db.refresh(location); return location
@router.get("/{customer_id}/locations", response_model=list[CustomerLocationRead], dependencies=[Depends(require_roles(Role.ADMIN, Role.TECHNICIAN))])
def customer_location_history(customer_id: int, limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    if not db.get(Customer, customer_id): raise HTTPException(404, "Customer not found")
    return db.query(CustomerLocation).filter(CustomerLocation.customer_id == customer_id).order_by(CustomerLocation.captured_at.desc()).limit(limit).all()
