import re
from typing import Dict

VAR_NORMALIZED = re.compile(r"[^\w]")
def normalize_name(name: str):
    return VAR_NORMALIZED.sub('', name)

# Not a complete list. Still need to add Data Source and Secret variables, but those are more complicated.
class EnvironmentVariableType:
    integer = { "name": "Integer", "id": 100000001, "literal": "Int", "python_type": int }
    decimal_number = { "name": "Decimal Number", "id": 100000001, "literal": "Float", "python_type": float }
    json = { "name": "JSON", "id": 100000003, "literal": "Object", "python_type": dict }
    text = { "name": "Text", "id": 100000000, "literal": "String", "python_type": str }
    boolean = { "name": "Boolean", "id": 100000002, "literal": "Bool", "python_type": bool }


class EnvironmentVariable:
    def __init__(self, name: str, prefix: str, var_type: Dict, default_value, description: str = "", languagecode: int = 1033):

        if type(default_value) != var_type["python_type"]:
            raise TypeError(f"Incorrect typing {type(default_value)} of default_value in environment variable {name}. Must be {var_type["python_type"]} to be used in type {var_type["name"]}")

        self.name = name
        self.normalized_name = normalize_name(name)
        self.type = var_type

        self.prefix = prefix

        self.default_value = default_value


        self.description = description

        self.languagecode = languagecode

        self.__localized_names: Dict[int, str] = {}
        self.__localized_names[self.languagecode] = self.name
        self.__localized_descriptions: Dict = {}


    def add_localized_name(self, description: str, languagecode: int):
        self.__localized_names[languagecode] = description


    def add_localized_description(self, description: str, languagecode: int):
        self.__localized_descriptions[languagecode] = description


    def export(self, version: str) -> Dict:
        environment_variable = {}
        environment_variable["__attributes"] = {"schemaname": f"{self.prefix}_{self.normalized_name}"}

        if self.type == EnvironmentVariableType.boolean:
            environment_variable["defaultvalue"] = "yes" if self.default_value == True else "no"
        else:
            environment_variable["defaultvalue"] = self.default_value

        display_name = {}
        display_name["__attributes"] = {
            "default": self.name
        }
        display_name["__elements"] = []
        for code, name in self.__localized_names.items():
            display_name["__elements"].append({
                "label":
                {
                    "__attributes": {
                        "description": name,
                        "languagecode": code
                    }
                }
            })

        environment_variable["displayname"] = display_name

        if self.description:
            environment_variable["description"] = {
                "__attributes": {
                    "default": self.description,
                },
                "__elements": []
            }

            for code, name in self.__localized_descriptions.items():
                environment_variable["description"]["__elements"].append({
                    "label":
                    {
                        "__attributes": {
                            "description": name,
                            "languagecode": code
                        }
                    }
                })

        environment_variable["introducedversion"] = version
        environment_variable["iscustomizable"] = 1
        environment_variable["isrequired"] = 0
        environment_variable["secretstore"] = 0
        environment_variable["type"] = self.type["id"]

        return environment_variable