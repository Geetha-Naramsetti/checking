def scanImport(node):
    module_name = node.text
    imported_names = []

    if node.childForFieldname("alias"):
        imported_names.append({
            "name": node.childForFieldname("alias").text,
            "startPoint": node.startPosition,
            "endPoint": node.endPosition,
        })
    else:
        imported_names.append({
            "name": module_name,
            "startPoint": node.startPosition,
            "endPoint": node.endPosition,
        })

    return imported_names


def scanImportFrom(node):
    module_name = node.childForFieldname("module_name").text
    imported_names = []

    for child in node.childForFieldname("names").children:
        if child.type == "aliased_import":
            if child.has_child_with_field_name("alias"):
                imported_names.append(child.childForFieldname("alias").text)
            else:
                imported_names.append(child.childForFieldname("name").text)
        elif child.type == "wildcard_import":
            imported_names.append(child.text)

    return [module_name, imported_names]
