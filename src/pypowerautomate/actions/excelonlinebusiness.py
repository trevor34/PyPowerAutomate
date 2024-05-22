from typing import Dict
from .base import BaseAction

DATETIME_FORMAT = set([None, "Serial Number", "ISO 8601"])

class ExcelOnlineGetTables(BaseAction):
    connection_host = {
        "connectionName": "shared_excelonlinebusiness",
        "operationId": "GetTables",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness"
    }

    def __init__(self, name: str, location: str, documentLibrary: str, file: str):
        """
        Initializes a new Get Tables action with specified parameters.

        Args:
            name (str): The name of the action.
            location (str): Can be one of the following:
                - "me"
                - "SharePoint Site URL"
                - "users/someone's UPN"
                - "groups/group Id"
                - "sites/SharePoint Site URL:/teams/team name:" (colons are required).
            documentLibrary (str): The ID of the document library.
            file (str): The path to the file within the online drive.
        """
        super().__init__(name)
        self.type = "OpenApiConnection"

        self.location: str = location
        self.documentLibrary: str = documentLibrary
        self.file: str = file

    def export(self) -> Dict:
        """
        Exports the current state and configuration of the Get Tables action in a dictionary format suitable for JSON serialization.

        Returns:
            Dict: A dictionary containing all the inputs and settings of the Get Tables.
        """
        inputs = {}
        parameters = {}

        parameters["source"] = self.location
        parameters["drive"] = self.documentLibrary
        parameters["file"] = self.file

        inputs["host"] = ExcelOnlineGetTables.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d

class ExcelOnlineGetRow(BaseAction):
    connection_host = {
        "connectionName": "shared_excelonlinebusiness",
        "operationId": "GetItem",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness"
    }

    def __init__(self, name: str, location: str, documentLibrary: str, file: str, table: str, keyColumn: str, keyValue: str, dateTimeFormat: str|None = None):
        """
        Initializes a new Get Tables action with specified parameters.

        Args:
            name (str): The name of the action.
            location (str): Can be one of the following:
                - "me"
                - "SharePoint Site URL"
                - "users/someone's UPN"
                - "groups/group Id"
                - "sites/SharePoint Site URL:/teams/team name:" (colons are required).
            documentLibrary (str): The ID of the document library.
            file (str): The path to the file within the online drive.
            table (str): The ID of the table.
            keyColumn (str): The name of the column to treat as a key.
            keyValue (str): The value to match against to get the row.
        """
        super().__init__(name)
        self.type = "OpenApiConnection"

        self.location: str = location
        self.documentLibrary: str = documentLibrary
        self.file: str = file
        self.table: str = table
        self.keyColumn: str = keyColumn
        self.keyValue: str = keyValue

        if dateTimeFormat not in DATETIME_FORMAT:
            raise ValueError(f"Unsupported DateTime format type {dateTimeFormat} in action {name}. Must be one of the following: {DATETIME_FORMAT}")

        self.dateTimeFormat: str|None = dateTimeFormat

    def export(self) -> Dict:
        """
        Exports the current state and configuration of the Get Row action in a dictionary format suitable for JSON serialization.

        Returns:
            Dict: A dictionary containing all the inputs and settings of the Get Tables.
        """
        inputs = {}
        parameters = {}

        parameters["source"] = self.location
        parameters["drive"] = self.documentLibrary
        parameters["file"] = self.file
        parameters["table"] = self.table
        parameters["idColumn"] = self.keyColumn
        parameters["id"] = self.keyValue

        if self.dateTimeFormat:
            parameters["dateTimeFormat"] = self.dateTimeFormat

        inputs["host"] = ExcelOnlineGetRow.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d