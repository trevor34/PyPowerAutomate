from typing import Dict, cast

from .expression import Expression
from .base import BaseAction


class Outlook365SendAnEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "SendEmailV2"
    }

    def __init__(self, name: str, to: str|Expression, subject: str|Expression, body: str|Expression, importance: str|Expression):
        super().__init__(name)
        self.type = "OpenApiConnection"
        if isinstance(to, Expression):
            to = cast(str, to.export())
        if isinstance(subject, Expression):
            subject = cast(str, subject.export())
        if isinstance(body, Expression):
            body = cast(str, body.export())
        if isinstance(importance, Expression):
            importance = cast(str, importance.export())

        self.to: str = to
        self.subject: str = subject
        self.body: str = body
        self.importance: str = importance

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["emailMessage/To"] = self.to
        parameters["emailMessage/Subject"] = self.subject
        parameters["emailMessage/Body"] = self.body
        parameters["emailMessage/Importance"] = self.importance

        inputs["host"] = Outlook365SendAnEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365DeleteEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "DeleteEmail_V2"
    }

    def __init__(self, name: str, messageid: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid

        inputs["host"] = Outlook365DeleteEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365ExportEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "ExportEmail_V2"
    }

    def __init__(self, name: str, messageid: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid

        inputs["host"] = Outlook365ExportEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365FindMeetingTimesV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "FindMeetingTimes_V2"
    }

    def __init__(self, name: str, activitydomain: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.activitydomain: str = activitydomain

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["body/ActivityDomain"] = self.activitydomain

        inputs["host"] = Outlook365FindMeetingTimesV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365FlagEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "Flag_V2"
    }

    def __init__(self, name: str, messageid: str, flagstatus: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid
        self.flagstatus: str = flagstatus

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid
        parameters["body/flag/flagStatus"] = self.flagstatus

        inputs["host"] = Outlook365FlagEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365ForwardAnEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "ForwardEmail_V2"
    }

    def __init__(self, name: str, message_id: str, torecipients: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.message_id: str = message_id
        self.torecipients: str = torecipients

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["message_id"] = self.message_id
        parameters["body/ToRecipients"] = self.torecipients

        inputs["host"] = Outlook365ForwardAnEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365GetAttachmentV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "GetAttachment_V2"
    }

    def __init__(self, name: str, messageid: str, attachmentid: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid
        self.attachmentid: str = attachmentid

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid
        parameters["attachmentId"] = self.attachmentid

        inputs["host"] = Outlook365GetAttachmentV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365GetCalendarViewOfEventsV3(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "GetEventsCalendarViewV3"
    }

    def __init__(self, name: str, calendarid: str, startdatetimeutc: str, enddatetimeutc: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.calendarid: str = calendarid
        self.startdatetimeutc: str = startdatetimeutc
        self.enddatetimeutc: str = enddatetimeutc

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["calendarId"] = self.calendarid
        parameters["startDateTimeUtc"] = self.startdatetimeutc
        parameters["endDateTimeUtc"] = self.enddatetimeutc

        inputs["host"] = Outlook365GetCalendarViewOfEventsV3.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365GetCalendarsV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "CalendarGetTables_V2"
    }

    def __init__(self, name: str):
        super().__init__(name)
        self.type = "OpenApiConnection"

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        inputs["host"] = Outlook365GetCalendarsV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365GetEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "GetEmailV2"
    }

    def __init__(self, name: str, messageid: str, includeattachments: bool):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid
        self.includeattachments: str = str(includeattachments)

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid
        parameters["includeAttachments"] = self.includeattachments

        inputs["host"] = Outlook365GetEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365GetEmailsV3(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "GetEmailsV3"
    }

    def __init__(self, name: str, folderpath: str|Expression|None = None, to_email: str|Expression|None = None, from_email: str|Expression|None = None, fetch_only_unread: str|bool|Expression|None = None, mailbox_address: str|Expression|None = None, include_attachments: str|bool|Expression|None = None, search_query: str|Expression|None = None, top: str|int|Expression|None = None, cc: str|Expression|None = None, to_or_cc: str|Expression|None = None, importance: str|Expression|None = None, fetch_only_with_attachment: str|bool|Expression|None = None, subject_filter: str|Expression|None = None):
        super().__init__(name)
        self.type = "OpenApiConnection"

        if isinstance(folderpath, Expression):
            folderpath = cast(str, folderpath.export())
        if isinstance(to_email, Expression):
            to_email = cast(str, to_email.export())
        if isinstance(from_email, Expression):
            from_email = cast(str, from_email.export())
        if isinstance(fetch_only_unread, Expression):
            fetch_only_unread = cast(str, fetch_only_unread.export())
        if isinstance(mailbox_address, Expression):
            mailbox_address = cast(str, mailbox_address.export())
        if isinstance(include_attachments, Expression):
            include_attachments = cast(str, include_attachments.export())
        if isinstance(search_query, Expression):
            search_query = cast(str, search_query.export())
        if isinstance(top, Expression):
            top = cast(str, top.export())
        if isinstance(cc, Expression):
            cc = cast(str, cc.export())
        if isinstance(to_or_cc, Expression):
            to_or_cc = cast(str, to_or_cc.export())
        if isinstance(importance, Expression):
            importance = cast(str, importance.export())
        if isinstance(fetch_only_with_attachment, Expression):
            fetch_only_with_attachment = cast(str, fetch_only_with_attachment.export())
        if isinstance(subject_filter, Expression):
            subject_filter = cast(str, subject_filter.export())

        self.folderpath: str|None = folderpath
        self.to_email: str|None = to_email
        self.from_email = from_email
        self.fetch_only_unread: str|None = str(fetch_only_unread) if type(fetch_only_unread) is bool else fetch_only_unread
        self.mailbox_address: str|None = mailbox_address
        self.include_attachments: str|None = str(include_attachments) if type(include_attachments) is bool else include_attachments
        self.search_query: str|None = search_query
        self.top: str|int|None = top
        self.cc: str|None = cc
        self.to_or_cc: str|None = to_or_cc
        self.importance: str|None = importance
        self.fetch_only_with_attachment: str|None = str(fetch_only_with_attachment) if type(include_attachments) is bool else include_attachments
        self.subject_filter: str|None = subject_filter

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        if self.folderpath is not None: parameters["folderPath"] = self.folderpath
        if self.to_email is not None: parameters["to"] = self.to_email
        if self.from_email is not None: parameters["from"] = self.from_email
        if self.fetch_only_unread is not None: parameters["fetchOnlyUnread"] = self.fetch_only_unread
        if self.mailbox_address is not None: parameters["mailboxAddress"] = self.mailbox_address
        if self.include_attachments is not None: parameters["includeAttachments"] = self.include_attachments
        if self.search_query is not None: parameters["searchQuery"] = self.search_query
        if self.top is not None: parameters["top"] = self.top
        if self.cc is not None: parameters["cc"] = self.cc
        if self.to_or_cc is not None: parameters["toOrCc"] = self.to_or_cc
        if self.importance is not None: parameters["importance"] = self.importance
        if self.fetch_only_with_attachment is not None: parameters["fetchOnlyWithAttachment"] = self.fetch_only_with_attachment
        if self.subject_filter is not None: parameters["subjectFilter"] = self.subject_filter

        inputs["host"] = Outlook365GetEmailsV3.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365MarkAsReadOrUnreadV3(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "MarkAsRead_V3"
    }

    def __init__(self, name: str, messageid: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid

        inputs["host"] = Outlook365MarkAsReadOrUnreadV3.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365MoveEmailV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "MoveV2"
    }

    def __init__(self, name: str, messageid: str|Expression, folderpath: str|Expression, mailbox_address: str|Expression|None = None):
        super().__init__(name)
        self.type = "OpenApiConnection"

        if isinstance(messageid, Expression):
            messageid = cast(str, messageid.export())
        if isinstance(folderpath, Expression):
            folderpath = cast(str, folderpath.export())
        if isinstance(mailbox_address, Expression):
            mailbox_address = cast(str, mailbox_address.export())

        self.messageid: str = messageid
        self.folderpath: str = folderpath
        self.mailbox_address: str|None = mailbox_address

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid
        parameters["folderPath"] = self.folderpath
        parameters["mailboxAddress"] = self.mailbox_address

        inputs["host"] = Outlook365MoveEmailV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365ReplyToEmailV3(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "ReplyToV3"
    }

    def __init__(self, name: str, messageid: str, body: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.messageid: str = messageid
        self.body: str = body

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["messageId"] = self.messageid
        parameters["replyParameters/Body"] = self.body

        inputs["host"] = Outlook365ReplyToEmailV3.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365SendEmailWithOptions(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "SendMailWithOptions"
    }

    def __init__(self, name: str, to: str, subject: str, options: str, importance: str, hidehtmlmessage: bool, showhtmlconfirmationdialog: bool, hidemicrosoftfooter: bool):
        super().__init__(name)
        self.type = "OpenApiConnectionWebhook"
        self.to: str = to
        self.subject: str = subject
        self.options: str = options
        self.importance: str = importance
        self.hidehtmlmessage: str = str(hidehtmlmessage)
        self.showhtmlconfirmationdialog: str = str(showhtmlconfirmationdialog)
        self.hidemicrosoftfooter: str = str(hidemicrosoftfooter)

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["optionsEmailSubscription/Message/To"] = self.to
        parameters["optionsEmailSubscription/Message/Subject"] = self.subject
        parameters["optionsEmailSubscription/Message/Options"] = self.options
        parameters["optionsEmailSubscription/Message/Importance"] = self.importance
        parameters["optionsEmailSubscription/Message/HideHTMLMessage"] = self.hidehtmlmessage
        parameters["optionsEmailSubscription/Message/ShowHTMLConfirmationDialog"] = self.showhtmlconfirmationdialog
        parameters["optionsEmailSubscription/Message/HideMicrosoftFooter"] = self.hidemicrosoftfooter

        inputs["host"] = Outlook365SendEmailWithOptions.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d


class Outlook365SetUpAutomaticRepliesV2(BaseAction):
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionName": "shared_office365",
        "operationId": "SetAutomaticRepliesSetting_V2"
    }

    def __init__(self, name: str, status: str, externalaudience: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.status: str = status
        self.externalaudience: str = externalaudience

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["body/automaticRepliesSetting/status"] = self.status
        parameters["body/automaticRepliesSetting/externalAudience"] = self.externalaudience

        inputs["host"] = Outlook365SetUpAutomaticRepliesV2.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["inputs"] = inputs

        return d
