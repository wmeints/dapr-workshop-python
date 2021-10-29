from fastapi import FastAPI, Body
from fastapi.responses import Response
from . import models, settings, services, clients
from os import environ
from dapr.clients import DaprClient


app = FastAPI()
app_settings = settings.ApplicationSettings()

with DaprClient() as client:
    license_key = client.get_secret("trafficcontrol-secrets", "finecalculator.licensekey").secret["finecalculator.licensekey"]
    print(f"Loaded license key from the Dapr secret store {license_key}")


processor = services.ViolationProcessor(
    services.FineCalculator(license_key),
    clients.VehicleRegistrationClient(app_settings.vehicle_registration_address)
)


@app.get("/dapr/subscribe")
def subscribe():
   subscription = [dict(
      pubsubname="pubsub",
      topic="speedingviolations",
      route="/collectfine"
   )]

   return subscription


@app.post("/collectfine")
def collect_fine(evt_data=Body(...)) -> Response:
    violation = models.SpeedingViolation.parse_raw(evt_data["data"])
    processor.process_speed_violation(violation)

    return Response(status_code=200)
