import requests
from . import models
from dapr.clients import DaprClient


class VehicleStateRepository:
    def __init__(self):
        self.state = {}

    def get_vehicle_state(self, license_number: str) -> models.VehicleState or None:
        with DaprClient() as client:
            return models.VehicleState.parse_raw(client.get_state("statestore", license_number).text())

    def set_vehicle_state(self, vehicle_state: models.VehicleState) -> None:
        with DaprClient() as client:
            client.save_state("statestore", vehicle_state.license_number, vehicle_state.json())
