from app.models.customer import CustomerStatus
from app.schemas.customer import CustomerCreate, CustomerLocationCreate

def test_customer_schema_accepts_live_location():
    customer=CustomerCreate(customer_code="C-001",name="Test Customer",latitude=23.7,longitude=90.4)
    assert customer.status is CustomerStatus.ACTIVE
    assert customer.latitude == 23.7

def test_customer_location_schema_bounds():
    location=CustomerLocationCreate(latitude=23.7,longitude=90.4,accuracy_m=8.5,source="gps")
    assert location.accuracy_m == 8.5
