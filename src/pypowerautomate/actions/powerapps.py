from typing import Dict
from .base import BaseAction

class PowerAppsVariableType:
    text = {"name": "Text", "type": "string"}
    yes_no = {"name": "Yes/No", "type": "boolean"}
    file = {"name": "File", "type": "string", "format": "byte"}
    email = {"name": "Email", "type": "string", "format": "email"}
    number = {"name": "Number", "type": "number"}
    date = {"name": "Date", "type": "string", "format": "date"}

class PowerAppsRespondToPowerAppOrFlow(BaseAction):

    def __init__(self, name: str):
        super().__init__(name)
        self.type = "Response"
        self.kind = "PowerApp"

        self.body = {}
        self.schema = {"type": "object", "properties": {}}
        self.status_code = 200

    def add_input(self, title: str, type: Dict, parameter: str):
        if title in self.body:
            raise ValueError(f"Title of input must be unique. Duplicate input title {title} in action {self.action_name}")

        self.body[title] = parameter
        self.schema["properties"][title] = {"title": title, "x-ms-dynamically-added": True, "type": type["type"]}

        if "format" in type:
            self.schema["properties"][title]["format"] = type["format"]

    def export(self) -> Dict:
        d = {}

        d["type"] = self.type
        d["kind"] = self.kind
        d["inputs"] = {}

        d["inputs"]["statusCode"] = self.status_code
        d["inputs"]["body"] = self.body
        d["inputs"]["schema"] = self.schema
        
        return d

