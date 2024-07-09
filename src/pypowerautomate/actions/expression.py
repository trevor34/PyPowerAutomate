from typing import Literal, cast


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
            out = {self.operator: self.args[0].export_in_if()}
        else:
            for arg in self.args:
                if isinstance(arg, Expression):
                    out[self.operator].append(arg.export_in_if())
                else:
                    out[self.operator].append(LiteralExpression(arg).export_in_if())

        return out

    def export(self, top = True):
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

        out += self.expression.export(top)
        for arg in self.args:
            if isinstance(arg, Expression):
                out += "[" + arg.export(top) + "]"
            else:
                out += "[" + LiteralExpression(arg).export(False) + "]"

        return out

class LiteralExpression(Expression):
    def __init__(self, literal):
        self.literal = literal

    def export_in_if(self):
        if type(self.literal) is str:
            return self.literal
        return self.literal_export(True)

    def export(self, top=True):
        if top:
            return self.literal_export(top)

        return str(self.literal_export(top))

    def literal_export(self, top=True):
        out = ""
        if top:
            if type(self.literal) is str:
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
    
class ArrayExpression(Expression):
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

        return out_array

class ObjectExpression(Expression):
    def __init__(self, object: dict):
        self.object = object

    def export_in_if(self):
        return self.export(True)

    def export(self, top=True):
        out_dict = {}

        arr = self.object.items()
        for a in arr:
            key = ""
            value = ""
            if isinstance(a[0], Expression):
                key = str(a[0].export(True))
            else:
                key = LiteralExpression(a[0]).export(True)
            
            if isinstance(a[1], Expression):
                value = a[1].export(True)
            else:
                value = LiteralExpression(a[1]).export(True)
            out_dict[key] = value
        
        return out_dict

# import json
# b = SubscriptExpression(SubscriptExpression(SubscriptExpression(Expression("sub", 1, 2), 3), 4), 5)

# e = Expression("and", Expression("or", Expression("and",
#     Expression("not", Expression("equals", "te'st", LiteralExpression(True))),
#     Expression("add", b, 6)), Expression("startsWith", Expression("concat", 7, "te'st"), "eee")
# ), Expression("a", 3, 5))
# f = LiteralExpression("Hi")

# j = ObjectExpression({e: ArrayExpression(["Hi", Expression("hello", "yes", "no"), "maybe", 33, ObjectExpression({44: ArrayExpression([444, Expression("e", 2)])})])})
# print(json.dumps(e.export_in_if()))