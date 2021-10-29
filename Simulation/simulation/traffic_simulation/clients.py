from . import events
from paho.mqtt.client import Client


class ClientError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TrafficControlClient:
    def __init__(self, base_address: str):
        self.base_address = base_address
        self.messaging_adapter = Client(client_id="simulation")
        self.messaging_adapter.connect("localhost")

    def send_vehicle_entry(self, evt: events.VehicleRegistered):
        self.messaging_adapter.publish("trafficcontrol/entrycam", payload=evt.json())

    def send_vehicle_exit(self, evt: events.VehicleRegistered):
        self.messaging_adapter.publish("trafficcontrol/exitcam", payload=evt.json())
