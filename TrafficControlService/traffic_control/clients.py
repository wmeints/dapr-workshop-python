from . import models
from dapr.clients import DaprClient


class FineCollectionClient:
   def __init__(self, base_address: str):
      self.base_address = base_address

   def collect_fine(self, violation: models.SpeedingViolation):
      with DaprClient() as client:
            client.publish_event("pubsub", "speedingviolations", violation.json())

