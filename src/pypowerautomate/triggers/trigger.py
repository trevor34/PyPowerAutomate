from typing import List, Dict
import uuid

class TriggerInputVariableType:
    """
    Variables defined for trigger inputs. Contains the following types:
    Text - A string of text
    Yes/No - A boolean value of "yes" or "no". Produces a toggle switch on a manual start
    File - A file input
    Email - An email address
    Number - A number
    Date - A date. Produces a calendar when used on a manual start
    Multi-Select - A type that allows for multiple selections.
    Dropdown - A type that produces a dropdown when ran manually.
    """
    text = {"name": "Text", "type": "string", "hint": "TEXT"}
    yes_no = {"name": "Yes/No", "type": "boolean", "hint": "BOOLEAN"}
    file = {"name": "File", "type": "object", "hint": "FILE"}
    email = {"name": "Email", "type": "string", "hint": "EMAIL", "format": "email"}
    number = {"name": "Number", "type": "number", "hint": "NUMBER"}
    date = {"name": "Date", "type": "string", "hint": "DATE", "format": "date"}

    # The following two types aren't directly selectable by the normal input in PowerAutomate
    # You can see them by selecting the "Text" type and clicking the 3 dots menu
    multi_select = {"name": "Multi-Select", "type": "array", "hint": "TEXT"}
    dropdown = {"name": "Dropdown", "type": "string", "hint": "TEXT"}


class BaseTrigger:
    """
    A base class for defining triggers. Triggers are building blocks in automation workflows,
    designed to initiate actions based on specific conditions.

    Attributes:
        trigger_name (str): The name of the trigger.
        metadata (Dict): A dictionary storing metadata related to the trigger, including a unique operation metadata ID.
        type (str): The type of the trigger, to be defined in derived classes.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the BaseTrigger class.

        Args:
            name (str): The name of the trigger.
        """
        self.trigger_name: str = name
        self.metadata: Dict = {}
        self.metadata["operationMetadataId"] = uuid.uuid4().__str__()
        self.type: str|None = None

    def export(self) -> Dict:
        """
        Exports the trigger's data in a dictionary format. This method should be implemented by derived classes.

        Raises:
            NotImplementedError: If the method is not overridden in a derived class.
        """
        raise NotImplementedError()

    def __repr__(self):
        return f"TriggerNode:{self.trigger_name}({self.type})"


class Triggers:
    """
    A class to aggregate multiple trigger nodes into a list structure, corresponding to the 'Triggers' field
    in a JSON schema.

    Attributes:
        nodes (List[BaseTrigger]): A list of trigger nodes.
    """

    def __init__(self, is_root: bool = False) -> None:
        """
        Initializes a new instance of the Triggers class.

        Args:
            is_root (bool): Indicates if this instance is at the root of trigger hierarchy. Defaults to False.
        """
        self.nodes: List[BaseTrigger] = []

    def append(self, new_trigger: BaseTrigger):
        """
        Appends a new trigger to the list of trigger nodes.

        Args:
            new_trigger (BaseTrigger): The trigger to be added to the nodes list.

        Raises:
            ValueError: If the trigger already exists in the nodes list.
        """
        if new_trigger in self.nodes:
            raise ValueError(f"{new_trigger} already exists in Triggers")
        self.nodes.append(new_trigger)

    def export(self) -> Dict:
        """
        Exports all trigger nodes into a dictionary format.

        Returns:
            Dict: A dictionary representation of all trigger nodes.
        """
        d = {}
        for node in self.nodes:
            d[node.trigger_name] = node.export()
        return d


class RecurrenceTrigger(BaseTrigger):
    """
    A class defining a recurrence trigger that schedules actions to occur repeatedly.

    Attributes:
        recurrence (Dict): Dictionary holding recurrence schedule details.
    """

    def __init__(self, name: str, frequency: str, interval: int):
        """
        Initializes a new instance of the RecurrenceTrigger class.

        Args:
            name (str): The name of the trigger.
        """
        super().__init__(name)
        self.type = "Recurrence"
        self.recurrence = {"frequency": frequency, "interval": interval}

    def set_schedule(self, frequency: str, interval: int):
        """
        Sets the recurrence schedule for the trigger.

        Args:
            frequency (str): The frequency of recurrence (e.g., 'Daily', 'Weekly').
            interval (int): The interval number between each recurrence.
        """
        self.recurrence["frequency"] = frequency
        self.recurrence["interval"] = interval

    def export(self):
        """
        Exports the recurrence trigger's data in a dictionary format.

        Returns:
            Dict: A dictionary representation of the recurrence trigger including metadata, type, and recurrence details.
        """
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["recurrence"] = self.recurrence
        return d

class ManualTrigger(BaseTrigger):
    """
    A class defining a manual trigger, typically used for triggers that require user intervention to activate,
    such as a button press.

    Attributes:
        kind (str): The kind of manual trigger, defaults to 'Button'.
        inputs (Dict): The inputs required by the trigger, defined by a schema.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the ManualTrigger class.

        Args:
            name (str): The name of the trigger.
        """
        super().__init__(name)

        self.type = "Request"
        self.kind = "Button"
        self.inputs = {"schema": {"type": "object", "properties": {}, "required": []}}

    def add_input(self, type: dict, title: str, description: str, required: bool = True, options: list[str]|None = None):
        """
        Adds an input to the manual trigger

        Args:
            type (dict): The type of variable, defined in TriggerInputVariableType
            title (str): The title of the input. Must be unique.
            description (str): The description of the input.
            required (bool, optional): Sets if the variable is required or not.
            options (list[str], optional): A list containing options for the input. Only available if type is dropdown or multi_select.
        """

        if title in self.inputs["schema"]["properties"]:
            raise ValueError(f"Title of input must be unique. Duplicate title {title} in trigger {self.trigger_name}")

        self.inputs["schema"]["properties"][title] = {
            "title": title,
            "type": type["type"],
            "x-ms-dynamically-added": True,
            "description": description,
            "x-ms-content-hint": type["hint"]
        }

        if "format" in type:
            self.inputs["schema"]["properties"][title]["format"] = type["format"]

        if options is not None and len(options) == 0 and (type == TriggerInputVariableType.dropdown or type == TriggerInputVariableType.multi_select):
            raise ValueError(f"Input '{title}' of '{self.trigger_name}' must have options. Is Type {type["name"]}.")

        if type == TriggerInputVariableType.multi_select:
                self.inputs["schema"]["properties"][title]["items"] = {"enum": options, "type": "string"}
        elif type == TriggerInputVariableType.dropdown:
            self.inputs["schema"]["properties"][title]["enum"] = options

        if type == TriggerInputVariableType.file:
            self.inputs["schema"]["properties"][title]["properties"] = {"name": {"type": "string"},"contentBytes": {"type": "string","format": "byte"}}

        if required:
            self.inputs["schema"]["required"].append(title)

    def export(self):
        """
        Exports the manual trigger's data in a dictionary format.

        Returns:
            Dict: A dictionary representation of the manual trigger including metadata, type, kind, and input details.
        """
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["kind"] = self.kind
        d["inputs"] = self.inputs
        return d

class ExternalTrigger(BaseTrigger):
    """
    A class defining an external trigger. Typically used for triggers that watch external data, such as email or form connectors

    Attributes:
        kind (str): The kind of manual trigger, defaults to 'Button'.
        inputs (Dict): The inputs required by the trigger, defined by a schema.
        reoccurrence (Dict): An optional timer used by some triggers.
    """
    def __init__(self, name: str, splitOn: str = "@triggerOutputs()?['body/value']"):
        super().__init__(name)

        self.splitOn = splitOn

    def _set_frequency(self, interval: int, frequency: str):
        self.recurrence = {"interval": interval, "frequency": frequency}

    def export(self):
        """
        Exports the trigger's data in a dictionary format. This method should be implemented by derived classes.

        Raises:
            NotImplementedError: If the method is not overridden in a derived class.
        """
        raise NotImplementedError()
