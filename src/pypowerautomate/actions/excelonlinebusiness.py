from enum import Enum
from typing import Dict, cast

from .expression import Expression
from .base import BaseAction

class DATETIME_FORMAT(str, Enum):
    serial_number = "Serial Number"
    iso_8601 = "ISO 8601"

# DATETIME_FORMAT = set([None, "Serial Number", "ISO 8601"])

class ExcelOnlineGetTables(BaseAction):
    connection_host = {
        "connectionName": "shared_excelonlinebusiness",
        "operationId": "GetTables",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness"
    }

    def __init__(self, name: str, location: str|Expression, documentLibrary: str|Expression, file: str|Expression):
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
        if isinstance(location, Expression):
            location = location.export()
        if isinstance(documentLibrary, Expression):
            documentLibrary = documentLibrary.export()
        if isinstance(file, Expression):
            file = file.export()
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

    def __init__(self, name: str, location: str|Expression, documentLibrary: str|Expression, file: str|Expression, table: str|Expression, keyColumn: str|Expression, keyValue: str|Expression, dateTimeFormat: str|Expression|None = None):
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
            dateTimeFormat (str): The desired date time format.
        """
        super().__init__(name)
        self.type = "OpenApiConnection"
        if isinstance(location, Expression):
            location = location.export()
        if isinstance(documentLibrary, Expression):
            documentLibrary = documentLibrary.export()
        if isinstance(file, Expression):
            file = file.export()
        if isinstance(table, Expression):
            table = table.export()
        if isinstance(keyColumn, Expression):
            keyColumn = keyColumn.export()
        if isinstance(keyValue, Expression):
            keyValue = keyValue.export()
        if isinstance(dateTimeFormat, Expression):
            dateTimeFormat = dateTimeFormat.export()

        self.location: str = location
        self.documentLibrary: str = documentLibrary
        self.file: str = file
        self.table: str = table
        self.keyColumn: str = keyColumn
        self.keyValue: str = keyValue

        # if dateTimeFormat not in DATETIME_FORMAT:
        #     raise ValueError(f"Unsupported DateTime format type {dateTimeFormat} in action {name}. Must be one of the following: {DATETIME_FORMAT}")

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

class ExcelOnlineListRows(BaseAction):
    connection_host = {
        "connectionName": "shared_excelonlinebusiness",
        "operationId": "GetItems",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness"
    }

    def __init__(self, name: str, location: str|Expression, documentLibrary: str|Expression, file: str|Expression, table: str|Expression, filterQuery: str|Expression|None = None, orderBy: str|Expression|None = None, top: int|str|Expression|None = None, skip: int|str|Expression|None = None, select: str|Expression|None = None, dateTimeFormat: str|Expression|None = None):
        """
        Initializes a new List Rows action with specified parameters.

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
            filterQuery (str, optional): An ODATA filter query to restrict the entries returned.
            orderBy (str, optional): An ODATA orderBy query for specifying the order of entries.
            top (int, optional): Total number of entries to retrieve (default = all).
            skip (int, optional): The number of entries to skip (default = 0).
            select (str, optional): Comma-separated list of columns to retrieve (first 500 by default).
            dateTimeFormat (str, optional): The desired date time format.
        """
        super().__init__(name)
        self.type = "OpenApiConnection"
        if isinstance(location, Expression):
            location = cast(str, location.export())
        if isinstance(documentLibrary, Expression):
            documentLibrary = cast(str, documentLibrary.export())
        if isinstance(file, Expression):
            file = cast(str, file.export())
        if isinstance(table, Expression):
            table = cast(str, table.export())
        if isinstance(filterQuery, Expression):
            filterQuery = cast(str, filterQuery.export())
        if isinstance(orderBy, Expression):
            orderBy = cast(str, orderBy.export())
        if isinstance(top, Expression):
            top = cast(str, top.export())
        if isinstance(skip, Expression):
            skip = cast(str, skip.export())
        if isinstance(select, Expression):
            select = cast(str, select.export())
        if isinstance(dateTimeFormat, Expression):
            dateTimeFormat = cast(str, dateTimeFormat.export())

        self.location: str = location
        self.documentLibrary: str = documentLibrary
        self.file: str = file
        self.table: str = table

        self.filterQuery: str|None = filterQuery
        self.orderBy: str|None = orderBy
        self.top: int|str|None = top
        self.skip: int|str|None = skip
        self.select: str|None = select


        # if dateTimeFormat not in DATETIME_FORMAT:
        #     raise ValueError(f"Unsupported DateTime format type {dateTimeFormat} in action {name}. Must be one of the following: {DATETIME_FORMAT}")

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

        if self.orderBy:
            parameters["$orderby"] = self.orderBy

        if self.top:
            parameters["$top"] = self.top

        if self.skip:
            parameters["$skip"] = self.skip

        if self.select:
            parameters["$select"] = self.select

        if self.dateTimeFormat:
            parameters["dateTimeFormat"] = self.dateTimeFormat

        inputs["host"] = ExcelOnlineGetTables.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d