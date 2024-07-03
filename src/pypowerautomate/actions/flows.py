from typing import Dict

from .expression import Expression

from ..triggers import ManualTrigger

from ..package import Package
from .base import BaseAction

class FlowRunChildAction(BaseAction):
    def __init__(self, name: str, child: Package|str|Expression, *args):
        super().__init__(name)

        self.name = name
        self.body = {}
        self.host = {}
        if type(child) == Package:
            self.host["workflowReferenceName"] = child.uuid
            if not isinstance(child.flow.triggers.nodes[0], ManualTrigger):
                raise ValueError(f"Flow of {child.display_name} must have a manual trigger.")

            input = list(child.flow.triggers.nodes[0].inputs["schema"]["properties"].values())

            for i in range(len(input)):
                self.add_input(input[i]["title"], args[i])
        else:
            self.host["workflowReferenceName"] = child

    def add_input(self, name: str, parameter: str|Expression):
        if name in self.body:
            raise ValueError(f"Name of parameter must be unique. Duplicate title {name} in run child flow {self.name}")

        if isinstance(parameter, Expression):
            parameter = parameter.export()

        self.body[name] = parameter

    def export(self) -> Dict:
        d = {}

        d["host"] = self.host
        d["body"] = self.body

        return d