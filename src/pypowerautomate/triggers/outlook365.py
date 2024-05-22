from .trigger import ExternalTrigger

IMPORTANCE = set(["Any", "Low", "Normal", "High"])

class OutlookSharedInboxNewEmailTrigger(ExternalTrigger):
    """
    A class defining a trigger for when a new email comes into a shared mailbox

    Attributes:
        kind (str): The kind of manual trigger, defaults to 'Button'.
        inputs (Dict): The inputs required by the trigger, defined by a schema.
    """

    connection_host = {
        "connectionName": "shared_office365",
        "operationId": "SharedMailboxOnNewEmailV2",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365"
    }

    def __init__(self, name: str, mailboxAddress: str, folderId: str|None = None, to: list[str] = [], cc: list[str] = [], toOrCc: list[str] = [], From: list[str] = [], importance: str = "Any", hasAttachments: bool = False, includeAttachments: bool = False, subjectFilter: str|None = None):
        super().__init__(name)

        self.__set_frequency(5, "Minutes")

        self.type = "OpenApiConnection"

        self.mailboxAddress = mailboxAddress
        self.folderId = folderId
        self.to = ";".join(to)
        self.cc = ";".join(cc)
        self.toOrCc = ";".join(toOrCc)
        self.From = ";".join(From)

        if importance not in IMPORTANCE:
            raise ValueError(f"Unsupported importance type {importance} in action {name}. Must be one of the following: {IMPORTANCE}")

        self.importance = importance

        self.hasAttachments = hasAttachments
        self.includeAttachments = includeAttachments
        self.subjectFilter = subjectFilter

    def export(self):
        d = {}
        d["recurrence"] = self.recurrence
        d["splitOn"] = self.splitOn
        d["type"] = self.type

        inputs = {}

        inputs["host"] = OutlookSharedInboxNewEmailTrigger.connection_host

        parameters = {}
        parameters["mailboxAddress"] = self.mailboxAddress
        parameters["folderId"] = self.folderId
        parameters["to"] = self.to
        parameters["cc"] = self.cc
        parameters["toOrCc"] = self.toOrCc
        parameters["importance"] = self.importance
        parameters["hasAttachments"] = self.hasAttachments
        parameters["includeAttachments"] = self.includeAttachments
        parameters["subjectFilter"] = self.subjectFilter

        inputs["parameters"] = parameters

        d["inputs"] = inputs

        return d


