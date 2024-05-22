import json
from os import makedirs, path, walk
from random import choices
import shutil
import string
from typing import Dict, List
import tempfile
from xml.etree.ElementTree import Element, tostring
import re
import zipfile

from ..environment_variable import EnvironmentVariable
from ..package import Package, Resource

# TODO: Add method comments

VAR_NORMALIZED = re.compile(r"[^\w]")
def normalize_name(name: str):
    return VAR_NORMALIZED.sub('', name)


class Solution:
    """
    Manages the packaging of PowerAutomate or Microsoft Dataverse solutions into a deployable ZIP file format,
    encapsulating all necessary components like APIs, connections, and definitions.

    [Zip directory structure]
    .
    ├── Workflows
    │   └── {flow}-{uuid}.json
    ├── environmentvariablesdefinitions
    │   └── {prefix}_{normalized_name}
    │       └── environmentvariabledefinition.xml
    ├── [Content_Types].xml
    ├── customizations.xml
    └── solution.xml
    """
    def __init__(self, display_name: str, prefix: str, publisher: str, version: str = "1.0.0.0", languagecode: int = 1033):
        """
        Initializes a new instance of the Solution class.

        Args:
            display_name (str): The name of the solution.
            prefix (str): The prefix to be used by the solution
            publisher (str): The publisher of the solution
            version (str): The version of the solution
            languagecode (int, optional): The language code for the solution. Use the following to find the correct code: https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a Defaults to 1033, for US English.
        """

        self.display_name = display_name
        self.prefix = prefix
        self.version = version

        self.__packages: Dict[str, Package] = {}
        self.__environment_variables: Dict[str, EnvironmentVariable] = {}
        self.__connections: Dict[str, Resource] = {}
        self.__localized_names: Dict = {}

        self.__localized_names[languagecode] = display_name

        self.languagecode = languagecode

        self.unique_name = normalize_name(display_name)

        self.publisher = publisher
        self.unique_publisher = normalize_name(publisher)

        self.__localized_publisher_names: Dict = {}
        self.__localized_publisher_names[languagecode] = self.publisher


    def add_environment_variable(self, variable: EnvironmentVariable):
        if variable.normalized_name in self.__environment_variables:
            raise ValueError(f"Variable name {variable.normalized_name} already exists in solution {self.display_name}. Environment variable names must be unique.")

        self.__environment_variables[variable.normalized_name] = variable

    def add_localized_name(self, name: str, languagecode: int):
        if languagecode in self.__localized_names:
            raise ValueError(f"Language codes must be unique. Duplicate code of {languagecode}")

        self.__localized_names[languagecode] = {"description": name}

    def __random_id(self):
        return ''.join(choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=5))

    def add_package(self, package: Package):
        for connection in package.get_api_connections():
            if connection.id in self.__connections:
                name = self.__connections[connection.id].get_connection_reference_logical_name()
                if name != None:
                    connection.set_connection_reference_logical_name(name)
            elif connection.id != None:
                connection.set_connection_reference_logical_name(f"{self.prefix}_{connection.id.split("/")[-1]}_{self.__random_id()}")
                self.__connections[connection.id] = connection

        self.__packages[package.uuid] = package

    def dict_to_xml(self, tag: str, item) -> Element:
        elem = Element(tag)

        if type(item) == dict:
            if "__elements" in item:
                elem = self.dict_to_xml(tag, item["__elements"])
            else:
                attributes = item.pop("__attributes", None)
                for key, val in item.items():
                    child = self.dict_to_xml(key, val)
                    elem.append(child)
                if attributes != None:
                    item["__attributes"] = attributes

            if "__attributes" in item:
                for key, val in item["__attributes"].items():
                    elem.set(key, str(val))
        elif type(item) == list:
            for index in item:
                for key, val in index.items():
                    child = self.dict_to_xml(key, val)
                    elem.append(child)
        # Don't use this unless xmlns:xsi is set to http://www.w3.org/2001/XMLSchema-instance
        elif item == None:
            elem.set("xsi:nil", "true")
        else:
            elem.text = str(item)

        return elem

    def export_solution_manifest(self) -> Element:
        import_export = {}
        attributes = {}
        attributes["version"] = "9.2.24041.216"
        attributes["SolutionPackageVersion"] = "9.2"
        attributes["languagecode"] = self.languagecode
        attributes["generatedBy"] = "CrmLive"
        attributes["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"

        import_export["__attributes"] = attributes

        manifest = {}

        manifest["UniqueName"] = normalize_name(self.display_name)
        manifest["LocalizedNames"] = []
        for code, name in self.__localized_names.items():
            localized_name = {}
            localized_name["description"] = name
            localized_name["languagecode"] = code
            manifest["LocalizedNames"].append({"LocalizedName": {"__attributes": localized_name}})

        manifest["Descriptions"] = {}
        manifest["Version"] = self.version
        manifest["Managed"] = 0

        publisher = {}

        publisher["UniqueName"] = self.unique_publisher

        publisher["LocalizedNames"] = []

        for code, name in self.__localized_publisher_names.items():
            localized_name = {}
            localized_name["description"] = name
            localized_name["languagecode"] = code
            publisher["LocalizedNames"].append({"LocalizedName": {"__attributes": localized_name}})

        publisher["EMailAddress"] = None
        publisher["CustomizationPrefix"] = self.prefix
        publisher["CustomizationOptionValuePrefix"] = 12691

        # Not sure if this is nessasary. Adding it in and testing later once its all up and running.
        publisher["Addresses"] = []

        for i in range(1, 3):
            address = {}

            address["AddressNumber"] = i
            address["AddressTypeCode"] = 1
            address["City"] = None
            address["County"] = None
            address["Country"] = None
            address["Fax"] = None
            address["FreightTermsCode"] = None
            address["ImportSequenceNumber"] = None
            address["Latitude"] = None
            address["Line1"] = None
            address["Line2"] = None
            address["Line3"] = None
            address["Longitude"] = None
            address["Name"] = None
            address["PostalCode"] = None
            address["PostOfficeBox"] = None
            address["PrimaryContactName"] = None
            address["ShippingMethodCode"] = 1
            address["StateOrProvince"] = None
            address["Telephone1"] = None
            address["Telephone2"] = None
            address["Telephone3"] = None
            address["TimeZoneRuleVersionNumber"] = None
            address["UPSZone"] = None
            address["UTCOffset"] = None
            address["UTCConversionTimeZoneCode"] = None

            publisher["Addresses"].append({"Address": address})

        manifest["Publisher"] = publisher

        manifest["RootComponents"] = []

        for uuid in self.__packages.keys():
            attributes = {}

            attributes["type"] = 29
            # Using {{ or }} escapes the { or }. Comes out as {00000000-0000-0000-0000-000000000000}
            attributes["id"] = f"{{{uuid}}}"
            attributes["behavior"] = 0

            manifest["RootComponents"].append({"RootComponent": {"__attributes": attributes}})

        manifest["MissingDependencies"] = {}

        import_export["SolutionManifest"] = manifest

        return self.dict_to_xml("ImportExportXml", import_export)

    def export_customizations(self) -> Element:
        customizations = {}

        customizations["__attributes"] = {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}

        customizations["Entities"] = {}
        customizations["Roles"] = {}
        customizations["Workflows"] = []

        for uuid, package in self.__packages.items():

            workflow = {}
            workflow["__attributes"] = {}
            workflow["__attributes"]["WorkflowId"] = f"{{{uuid}}}"
            workflow["__attributes"]["Name"] = package.display_name
            workflow["JsonFileName"] = f"/Workflows/{normalize_name(package.display_name)}-{uuid}.json"
            workflow["Type"] = 1
            workflow["Subprocess"] = 0
            workflow["Category"] = 5
            workflow["Mode"] = 0
            workflow["Scope"] = 4
            workflow["OnDemand"] = 0
            workflow["TriggerOnCreate"] = 0
            workflow["TriggerOnDelete"] = 0
            workflow["AsyncAutodelete"] = 0
            workflow["SyncWorkflowLogOnFailure"] = 0
            workflow["StateCode"] = 1
            workflow["StatusCode"] = 2
            workflow["RunAs"] = 1
            workflow["IsTransacted"] = 1
            workflow["IntroducedVersion"] = self.version
            workflow["IsCustomizable"] = 1
            workflow["BusinessProcessType"] = 0
            workflow["IsCustomProcessingStepAllowedForOtherPublishers"] = 1
            workflow["PrimaryEntity"] = "none"

            workflow["LocalizedNames"] = []

            for code, name in package.get_localized_names().items():
                localized_name = {}
                localized_name["languagecode"] = code
                localized_name["description"] = name
                workflow["LocalizedNames"].append({"LocalizedName": {"__attributes": localized_name}})

            customizations["Workflows"].append({"Workflow": workflow})

        customizations["FieldSecurityProfiles"] = {}
        customizations["Templates"] = {}
        customizations["EntityMaps"] = {}
        customizations["EntityRelationships"] = {}
        customizations["OrganizationSettings"] = {}
        customizations["optionsets"] = {}
        customizations["CustomControls"] = {}
        customizations["EntityDataProviders"] = {}

        customizations["connectionreferences"] = []

        for id, connection in self.__connections.items():
            connection_reference = {}

            connection_reference["__attributes"] = {"connectionreferencelogicalname": connection.get_connection_reference_logical_name()}

            connection_reference["connectionreferencedisplayname"] = connection.display_name
            connection_reference["connectorid"] = id
            connection_reference["iscustomizable"] = 1
            connection_reference["statecode"] = 0
            connection_reference["statuscode"] = 1

            customizations["connectionreferences"].append({"connectionreference": connection_reference})

        customizations["Languages"] = []
        customizations["Languages"].append({"Language": self.languagecode})

        return self.dict_to_xml("ImportExportXml", customizations)


    def export_content_types(self) -> Element:
        types = {}

        types["__attributes"] = {"xmlns": "http://schemas.openxmlformats.org/package/2006/content-types"}

        types["__elements"] = []

        for extension in ["xml", "json"]:
            attributes = {}
            attributes["Extension"] = extension
            attributes["ContentType"] = "application/octet-stream"
            types["__elements"].append({"Default": {"__attributes": attributes}})

        return self.dict_to_xml("Types", types)


    def export_environment_variables(self) -> Dict[str, Element]: # Dictionary of schemaname: Element
        environment_variables = {}
        for name, variable in self.__environment_variables.items():
            environment_variable = variable.export(self.version)

            environment_variables[environment_variable["__attributes"]["schemaname"]] = self.dict_to_xml("environmentvariabledefinition", environment_variable)

        return environment_variables


    def export_workflows(self) -> Dict:
        workflows = {}
        for uuid, package in self.__packages.items():
            workflow = package.export_definition(embedded = True)
            workflows[package.display_name] = {"definition": workflow, "uuid": uuid}

        return workflows

    def __write_json_file(self, path: str, content: dict):
        with open(path, 'w') as f:
            f.write(json.dumps(content))


    def __write_xml_file(self, path: str, content: Element, xml_declaration=False):
        # The tostring function outputs a byte string. We must output it with 'wb' instead of 'w'
        with open(path, 'wb') as f:
            f.write(tostring(content, encoding="utf-8", xml_declaration=xml_declaration))

    def export_zipfile(self, output_dir: str = ".") -> str:
        work_dir = tempfile.TemporaryDirectory().name

        # Directory hierarchy creation
        makedirs(work_dir, exist_ok=True)

        # ./solution.xml
        self.__write_xml_file(
            path.join(work_dir, "solution.xml"), self.export_solution_manifest())
        # ./customizations.xml
        self.__write_xml_file(path.join(
            work_dir, "customizations.xml"), self.export_customizations())
        # ./[Content_Types].xml
        self.__write_xml_file(path.join(
            work_dir, "[Content_Types].xml"), self.export_content_types(), xml_declaration=True)
        # ./environmentvariabledefinitions/{name}/environmentvariabledefinition.xml
        for name, definition in self.export_environment_variables().items():
            definition_dir = path.join(work_dir, "environmentvariabledefinitions", name)

            # Directory hierarchy creation
            makedirs(definition_dir, exist_ok=True)

            self.__write_xml_file(
                path.join(definition_dir, "environmentvariabledefinition.xml"), definition
            )

        # ./Workflows/{name}-{uuid}.json
        definition_dir = path.join(work_dir, "Workflows")
        makedirs(definition_dir, exist_ok=True)
        for name, flow in self.export_workflows().items():
            self.__write_json_file(
                path.join(definition_dir, f"{name}-{flow["uuid"]}.json"), flow["definition"])

        # zip file creation
        filepath = path.join(output_dir, f"{self.display_name}.zip")
        zip_file = zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED)
        for root, _, files in walk(work_dir):
            for file in files:
                zip_file.write(path.join(root, file), path.relpath(
                    path.join(root, file), work_dir))

        zip_file.comment = b'\xe2\xa0\x89\xe2\xa0\x97\xe2\xa0\x91\xe2\xa0\x81\xe2\xa0\x9e\xe2\xa0\x91\xe2\xa0\x99\xe2\xa0\x80\xe2\xa0\x83\xe2\xa0\xbd\xe2\xa0\x80\xe2\xa0\x9e\xe2\xa0\x91\xe2\xa0\x81\xe2\xa0\x8d\xe2\xa0\xa7'
        zip_file.close()

        # clean-up
        shutil.rmtree(work_dir)
        return path.abspath(filepath)
