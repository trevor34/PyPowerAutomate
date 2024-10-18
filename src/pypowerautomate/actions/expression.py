import json
from typing import Literal


if_operators = ["and", "or", "not", "contains", "equals", "greater", "greaterOrEquals", "less", "lessOrEquals", "startsWith", "endsWith"]

class Expression:
    '''Class to define expressions used in Power Automate.

    Attributes:
        operator (str): The operator or name of the current expression
        *args (tuple[any]): The arguments to be passed to the expression'''
    def __init__(self, operator: str, *args):
        self.operator = operator
        self.args = args

    def export_in_if(self):
        if self.operator not in if_operators:
            return self.export()

        out = {self.operator: []}
        if self.operator == "not":
            child_operator = self.args[0].operator

            if child_operator and child_operator not in if_operators:
                out = self.export()
            else:
                out = {self.operator: self.args[0].export_in_if()}
        else:
            for arg in self.args:
                if isinstance(arg, Expression):
                    out[self.operator].append(arg.export_in_if())
                else:
                    out[self.operator].append(LiteralExpression(arg).export_in_if())

        return out

    def export(self, top = True) -> str | list | dict:
        out = ""

        if top:
            out = "@"
            top = False

        out += self.operator + "("

        out_args = []
        for arg in self.args:
            if isinstance(arg, Expression):
                out_args.append(arg.export(top))
            else:
                out_args.append(LiteralExpression(arg).export(False))

        out += ",".join(out_args) + ")"

        return out

class SubscriptExpression(Expression):
    def __init__(self, expression: Expression, *args):
        self.expression = expression
        self.args = args

    def export_in_if(self):
        return self.export(True)

    def export(self, top=True):
        out = ""

        if top:
            out = "@"
            top = False

        out += str(self.expression.export(top))
        for arg in self.args:
            if isinstance(arg, Expression):
                out += "[" + str(arg.export(top)) + "]"
            else:
                out += "[" + LiteralExpression(arg).export(False) + "]"

        return out

class LiteralExpression(Expression):
    def __init__(self, literal):
        self.literal = literal

    def export_in_if(self):
        return self.literal_export(True)

    def export(self, top=True):
        if top:
            return self.literal_export(top)

        return str(self.literal_export(top))

    def literal_export(self, top=True):
        out = ""
        if top:
            if type(self.literal) is str or self.literal is None:
                return self.literal

            out = "@"
            top = False


        if self.literal is None:
            out += "null"
        elif type(self.literal) is bool:
            out += "true" if self.literal else "false"
        elif type(self.literal) is str:
            out = "'" + self.literal.replace("'", "''") + "'"
        else:
            out = self.literal

        return out

class ArrayExpression(LiteralExpression):
    def __init__(self, array: list):
        self.array = array

    def export_in_if(self):
        return self.export(True)

    def export(self, top=True):
        out_array = []
        for item in self.array:
            if isinstance(item, Expression):
                out_array.append(item.export(True))
            else:
                out_array.append(LiteralExpression(item).export(True))

        if not top:
            out_array = f"array('{json.dumps(out_array)}')"
        return out_array

class KeyValueExpression(LiteralExpression):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def export_in_if(self):
        return self.export(True)

    def export(self, top=True):
        return [self.key, self.value]

class ObjectExpression(LiteralExpression):
    def __init__(self, object: dict|list[KeyValueExpression]):
        self.object = object

    def export_in_if(self):
        return self.export(True)

    def export(self, top=True):
        out_dict = {}

        if type(self.object) is dict:
            arr = self.object.items()
        else:
            arr = [keyvaluepair.export() for keyvaluepair in self.object]

        for a in arr:
            key = ""
            value = ""
            if isinstance(a[0], Expression):
                key = a[0].export(True)

                if top:
                    key = str(key)
            else:
                key = LiteralExpression(a[0]).export(True)

            if isinstance(a[1], Expression):
                value = a[1].export(True)
            else:
                if not top:
                    value = a[1]
                else:
                    value = LiteralExpression(a[1]).export(True)
            out_dict[key] = value

        if not top:
            out_dict = f"json('{json.dumps(out_dict)}')"
        return out_dict

# a = SubscriptExpression(SubscriptExpression(SubscriptExpression(Expression("sub", 1, 2), 3), 4), 5)

# b = Expression("and", Expression("or", Expression("and",
#     Expression("not", Expression("equals", "te'st", LiteralExpression(True))),
#     Expression("add", a, 6)), Expression("startsWith", Expression("concat", 7, "te'st"), "eee")
# ), Expression("length", "wow"))
# c = LiteralExpression("Hi")

# d = ObjectExpression({"a": c, "c": Expression("length", "e")})

# e = Expression("contains", d, "a")

# f = ObjectExpression({44: ArrayExpression([444, Expression("length", ArrayExpression([1,2,3,ArrayExpression([4,Expression("length", "length")])]))])})

# g = ArrayExpression(["hello", e, LiteralExpression("maybe"), LiteralExpression(33), f])

# j = ObjectExpression({c: g})

# k = SubscriptExpression(ObjectExpression({"a": "b"}), "a")

# print(json.dumps(b.export_in_if()))