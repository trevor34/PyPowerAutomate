from typing import Dict
from .base import BaseAction
from .actions import Actions, RawActions
from .condition import Condition
from .expression import Expression


class IfStatement(BaseAction):
    """
    A class that defines an If statement.

    Args:
        name (str): The name of the If statement.
        condition (Condition): The condition to be evaluated.
    """

    def __init__(self, name: str, condition: Condition|Expression):
        super().__init__(name)
        self.type: str = "If"
        self.condition: Condition|Expression = condition
        self.true_actions: Actions|None = None
        self.false_actions: Actions|None = None

    def set_true_actions(self, actions: Actions):
        """
        Sets the actions to be executed if the condition is true.

        Args:
            actions (Actions): The actions to be executed if the condition is true.
        """
        self.true_actions = actions

    def set_false_actions(self, actions: Actions):
        """
        Sets the actions to be executed if the condition is false.

        Args:
            actions (Actions): The actions to be executed if the condition is false.
        """
        self.false_actions = actions

    def export(self) -> Dict:
        """
        Exports the If statement as a dictionary.

        Returns:
            Dict: A dictionary representing the If statement.
        """
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter

        if type(self.condition) is Condition:
            d["expression"] = self.condition.export()
        elif type(self.condition) is Expression:
            d["expression"] = self.condition.export_in_if()

        if self.true_actions:
            d["actions"] = self.true_actions.export()
        else:
            d["actions"] = {}

        if self.false_actions:
            d["else"] = {"actions": self.false_actions.export()}

        return d


class ForeachStatement(BaseAction):
    """
    A class that defines a Foreach statement.

    Args:
        name (str): The name of the Foreach statement.
        foreach (str): The variable to iterate over.
    """

    def __init__(self, name: str, foreach: str|Expression):
        super().__init__(name)
        self.type: str = "Foreach"

        if isinstance(foreach, Expression):
            foreach = foreach.export()

        self.foreach: str = foreach
        self.actions: Actions|None = None

    def set_actions(self, actions: Actions):
        """
        Sets the actions to be executed for each iteration.

        Args:
            actions (Actions): The actions to be executed for each iteration.
        """
        self.actions = actions

    def export(self) -> Dict:
        """
        Exports the Foreach statement as a dictionary.

        Returns:
            Dict: A dictionary representing the Foreach statement.
        """
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter

        if isinstance(self.foreach, Expression):
            self.foreach = self.foreach.export()

        d["foreach"] = self.foreach
        if self.actions != None:
            d["actions"] = self.actions.export()
        return d


class ScopeStatement(BaseAction):
    """
    A class that defines a Scope statement.

    Args:
        name (str): The name of the Scope statement.
        actions (Actions | RawActions): The actions to be executed within the scope.
    """

    def __init__(self, name: str, actions: Actions | RawActions):
        super().__init__(name)
        self.type: str = "Scope"

        self.actions: Actions | RawActions = actions

    def export(self) -> Dict:
        """
        Exports the Scope statement as a dictionary.

        Returns:
            Dict: A dictionary representing the Scope statement.
        """
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["actions"] = self.actions.export()
        return d


class DoUntilStatement(BaseAction):
    """
    A class that defines a Do Until statement.

    Args:
        name (str): The name of the Do Until statement.
        actions (Actions): The actions to be executed within the Do Until loop.
        expression (str): The expression to be evaluated to determine when to stop the loop.
        limit_count (int, optional): The maximum number of iterations to perform. Defaults to 60.
    """

    def __init__(self, name: str, actions: Actions, expression: str|Expression, limit_count: int = 60):
        super().__init__(name)
        self.type: str = "Until"

        if isinstance(expression, Expression):
            expression = expression.export()

        self.actions: Actions = actions
        self.limit = {
            "count": limit_count,
            "timeout": "PT1H"
        }
        self.expression = expression

    def export(self) -> Dict:
        """
        Exports the Do Until statement as a dictionary.

        Returns:
            Dict: A dictionary representing the Do Until statement.
        """
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["actions"] = self.actions.export()

        d["expression"] = self.expression
        d["limit"] = self.limit
        return d

class SwitchStatement(BaseAction):
    """
    A class that defines a Switch statement.

    Args:
        name (str): The name of the Switch statement.
        expression (str): The expression to be evaluated to determine which path to take.
    """

    def __init__(self, name: str, expression: str|Expression):
        super().__init__(name)

        self.type: str = "Switch"

        if isinstance(expression, Expression):
            expression = expression.export()

        self.expression: str = expression
        self.cases: Actions = Actions()
        self.used_names: list[str] = [] # Used case names are only local to each switch statement, unlike with actions.
        self.used_cases: list[int|str] = []
        self.default_case = DefaultCaseStatement(Actions())

    def add_case(self, case_statement: 'CaseStatement'):
        if case_statement.expression in self.used_cases:
            raise ValueError(f"Expressions in case statements must be distinct values. {case_statement.action_name} in switch statement {self.action_name}")

        self.used_cases.append(case_statement.expression)

        self.cases.append(case_statement)

    def set_default_case(self, case_statement: 'DefaultCaseStatement'):
        self.default_case = case_statement

    def export(self):
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["cases"] = self.cases.export()
        d["expression"] = self.expression

        d["default"] = self.default_case.export()

        return d

class CaseStatement(BaseAction):
    """
    A class that defines a Case statement.

    Args:
        name (str): The name of the Case statement.
        expression (int|str): The expression to test against the parent Switch statement
        actions (Actions): The actions to take if this case is used
    """
    def __init__(self, name: str, expression: int|str|Expression, actions: Actions):
        super().__init__(name)
        if isinstance(expression, Expression):
            expression = expression.export()
        self.expression = expression
        self.actions = actions

    def export(self):
        d = {}

        d["case"] = self.expression
        d["actions"] = self.actions.export()

        return d

class DefaultCaseStatement(CaseStatement):
    """
    A class that defines a Case statement.

    Args:
        expression (int|str): The expression to test against the parent Switch statement
    """
    def __init__(self, actions: Actions):
        super().__init__("default", None, actions) # type: ignore

    def export(self):
        d = {}

        d["actions"] = self.actions.export()

        return d