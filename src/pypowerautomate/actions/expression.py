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
        return self.literal_export()

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
            out += "'" + self.literal.replace("'", "''") + "'"
        else:
            out = self.literal

        return out

import json
b = SubscriptExpression(SubscriptExpression(SubscriptExpression(Expression("sub", 1, 2), 3), 4), 5)

e = Expression("and", Expression("or", Expression("and",
    Expression("not", Expression("equals", "te'st", 0)),
    Expression("add", b, 6)), Expression("startsWith", Expression("concat", 7, "te'st"), "eee")
), Expression(""))
f = LiteralExpression(False)
print(json.dumps(e.export_in_if()))