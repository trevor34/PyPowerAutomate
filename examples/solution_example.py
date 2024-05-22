from pypowerautomate.actions.dataoperation import ComposeAction
from pypowerautomate.environment_variable import EnvironmentVariableType, EnvironmentVariable
from pypowerautomate.flow import Flow
from pypowerautomate.package import Package
from pypowerautomate.solution import Solution
from pypowerautomate.triggers.trigger import ManualTrigger

PREFIX = "pre"

# Create environment variables
variable_a = EnvironmentVariable("A", PREFIX, EnvironmentVariableType.integer, 12)
variable_b = EnvironmentVariable("B", PREFIX, EnvironmentVariableType.boolean, False)

# Create a new flow
flow = Flow()

flow.set_trigger(ManualTrigger("Test"))
flow.add_top_action(ComposeAction("A", "B"))
flow.append_action(ComposeAction("B", "A"))

# Add it into a package
package = Package("test",flow)

# Add connectors
package.set_sharepoint_connector("Sharepoint Connection")
package.set_forms_connector("Forms Connection")
package.set_excel_connector("Excel Connector")

# Create another flow
flow2 = Flow()

# Add environment variable to flow
flow2.add_environment_variable(variable_a)

flow2.set_trigger(ManualTrigger("Test 2"))
flow2.add_top_action(ComposeAction("B", "A"))
flow2.append_action(ComposeAction("A", "B"))

package2 = Package("test2",flow2)

package2.set_sharepoint_connector("Sharepoint Connection")
package2.set_forms_connector("Forms Connection")

# Create a solution
solution = Solution("solution_test", PREFIX, "publisher")

# Add environment variables to solution
solution.add_environment_variable(variable_a)
solution.add_environment_variable(variable_b)

# Add packages to solution
solution.add_package(package)
solution.add_package(package2)

# Export the solution
export = solution.export_zipfile()
print("Exported to", export)
