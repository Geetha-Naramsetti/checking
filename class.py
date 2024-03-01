from .assignment import scanAssignment
from .function import scanFunction
from .decorated import scanDecoratedFunction

def scanClass(node):
    class_name = node.childForFieldname("name").text
    functions_in_class = []
    variables_in_class = []
    calls_in_class = []

    for child in node.childForFieldname("body").children:
        if child.type == "function_definition":
            [
                function_name,
                function_args,
                variables,
                calls,
                returns,
                nested_functions,
                nested_classes,
                start_point,
                end_point
            ] = scanFunction(child)

            functions_in_class.append({
                "name": function_name,
                "args": function_args,
                "variables": variables,
                "calls": calls,
                "returns": returns,
                "nested_functions": nested_functions,
                "nested_classes": nested_classes,
                "static": False,
                "start_point": start_point,
                "end_point": end_point
            })
        elif child.type == "decorated_definition":
            [
                function_name,
                function_args,
                variables,
                calls,
                returns,
                nested_functions,
                nested_classes,
                start_point,
                end_point
            ] = scanDecoratedFunction(child)

            functions_in_class.append({
                "name": function_name,
                "args": function_args,
                "variables": variables,
                "calls": calls,
                "returns": returns,
                "nested_functions": nested_functions,
                "nested_classes": nested_classes,
                "static": True,
                "start_point": start_point,
                "end_point": end_point
            })
        elif child.type == "expression_statement":
            for subchild in child.children:
                if subchild.type == "assignment":
                    vars, fcalls = scanAssignment(subchild)
                    variables_in_class.append(vars)
                    calls_in_class.append(fcalls)
        elif child.type == "call":
            calls_in_class.append({
                "name": child.text,
                "start_point": child.startPosition,
                "end_point": child.endPosition,
            })
        elif child.type == "class_definition":
            nested_class_name, functions, variables, calls = scanClass(child)
            functions_in_class.extend(functions)
            variables_in_class.extend(variables)
            calls_in_class.extend(calls)

    return class_name, functions_in_class, variables_in_class, calls_in_class
