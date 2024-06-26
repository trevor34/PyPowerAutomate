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

    def export(self, in_if = False, top = True):
        if in_if and self.operator not in if_operators:
            in_if = False

        if in_if:
            out = {self.operator: []}
            if self.operator == "not":
                out = {self.operator: self.args[0].export(in_if, top)}
            else:
                for arg in self.args:
                    if isinstance(arg, Expression):
                        out[self.operator].append(arg.export(in_if, top))
                    else:
                        out[self.operator].append(arg)

        else:
            out = ""

            if top:
                out = "@"
                top = False

            out += self.operator + "("

            out_args = []
            for arg in self.args:
                if isinstance(arg, Expression):
                    out_args.append(arg.export(in_if, top))
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

    def export(self, in_if=False, top=True):
        out = ""

        in_if = False

        if top:
            out = "@"
            top = False

        out += str(self.expression.export(False, False))
        for arg in self.args:
            if isinstance(arg, Expression):
                out += "[" + str(arg.export(in_if, top)) + "]"
            elif type(arg) is str:
                out += "['" + arg.replace("'", "''") + "']"
            else:
                out += "[" + str(arg) + "]"

        return out


# b = SubscriptExpression(SubscriptExpression(SubscriptExpression(Expression("sub"), 4), 5), 6)

# e = Expression("and",
#     Expression("not", Expression("equals", "te'st", 2)),
#     Expression("add", b, 3)
# )
# print(e.export(True))