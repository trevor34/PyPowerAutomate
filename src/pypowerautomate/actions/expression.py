from typing import cast


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
                    out[self.operator].append(arg)

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
            elif type(arg) is str:
                out_args.append("'" + arg.replace("'", "''") + "'")
            else:
                out_args.append(str(arg))

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
            elif type(arg) is str:
                out += "['" + arg.replace("'", "''") + "']"
            else:
                out += "[" + str(arg) + "]"

        return out

class LiteralExpression(Expression):
    def __init__(self, literal):
        self.literal = literal

    def export_in_if(self):
        return self.export(True)

    def export(self, top=True):
        out = ""
        if top:
            out = "@"
            top = False

        if self.literal is None:
            out += "null"
        else:
            out = self.literal

        return out

# import json
# b = SubscriptExpression(SubscriptExpression(SubscriptExpression(Expression("sub"), 4), 5), 6)

# e = Expression("and",
#     Expression("not", Expression("equals", "test", 2)),
#     Expression("add", b, 3)
# )
# f = LiteralExpression(False)
# print(json.dumps(f.export_in_if()))