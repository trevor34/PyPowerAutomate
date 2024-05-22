from typing import Dict
from .trigger import ExternalTrigger

class FormsResponseTrigger(ExternalTrigger):
    """
    A class defining a Forms response trigger

    Attributes:
        type (str): The type of trigger, defaults to 'OpenApiConnectionWebhook'.
        form_id (str): The ID that represents the Microsoft Forms page
    """

    connection_host = {
            "connectionName": "shared_microsoftforms",
            "operationId": "CreateFormWebhook",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_microsoftforms"
        }

    def __init__(self, name: str, form_id: str):
        """
        Initializes a new instance of the ManualTrigger class.

        Args:
            name (str): The name of the trigger.
            form_id (str): The ID that represents the Microsoft Forms page
        """
        super().__init__(name)

        self.type = "OpenApiConnectionWebhook"
        self.form_id = form_id

    def export(self) -> Dict:

        d = {}

        d["type"] = self.type
        d["inputs"] = {}
        d["inputs"]["host"] = FormsResponseTrigger.connection_host
        d["inputs"]["parameters"] = {
            "form_id": self.form_id
        }
        d["metadata"] = self.metadata
        d["splitOn"] = self.splitOn

        return d
