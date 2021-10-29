from pydantic import BaseModel
from dapr.clients import DaprClient


class Vehicle(BaseModel):
   vehicleId: str
   make: str
   model: str
   ownerName: str
   ownerEmail: str


class VehicleRegistrationClient:
   def __init__(self, base_address: str):
      self.base_address = base_address

   def get_vehicle_info(self, license_number: str) -> Vehicle:
      with DaprClient() as client:
            response = client.invoke_method(
               "vehicleregistrationservice",
               f"vehicleinfo/{license_number}",
               data=b'',
               http_verb="GET"
            )

            return Vehicle.parse_raw(response.text())

