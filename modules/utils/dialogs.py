import maya.cmds as maya


def shelf_dialog(title="input", message="Enter value:", buttons=["Ok", "Cancel"], valid=None):
    result = maya.promptDialog(
        title=title, message=message, button=buttons, defaultButton="Ok", cancelButton="Cancel", dismissString="Cancel"
    )

    if result == "Ok":
        text = maya.promptDialog(query=True, text=True)
        if valid and text.lower() not in valid:
            maya.warning(f"Invalid input: {text}")
            return None
        return text
    return None
