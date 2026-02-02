import maya.cmds as maya

from .helpers import find_common_parent


def clean_combine():
    """
    combines selected nodes, leaving them within their closest parent group or world.
    """
    curr_selection = maya.ls(selection=True, long=True)

    if len(curr_selection) < 2:
        maya.error("Invalid selection. Combine needs at least 2 objects.")
        return

    try:
        combined = maya.polyUnite(curr_selection, ch=False)[0]

        maya.xform(combined, centerPivots=True)
        common_parent = find_common_parent(curr_selection)

        if common_parent:
            maya.parent(combined, common_parent)

        maya.select(combined)
        maya.inViewMessage(amg="Objects have been <h1>merged</h1>", pos="topCenter", fade=True)
    except RuntimeError:
        maya.error("Combine Failed.")


#### WORK IN PROGRESS ####
# def clean_detach():
#     """
#     Extracts mesh with selected faces into new object(s), deletes the original, clears history and parents new objects to world
#     """
#     selection = maya.ls(selection=True, flatten=True)
#     if not selection:
#         maya.warning("No faces selected.")
#         return

#     if not all(".f[" in s for s in selection):
#         maya.error("Please select only faces.")
#         return

#     original_object = selection[0].split(".")[0]

#     if any(s.split(".")[0] != original_object for s in selection):
#         maya.error("All selected faces must belong to the same object.")
#         return

#     try:
#         separated_objects = maya.polySeparate(original_object, rs=True, ch=False)

#         new_objects = separated_objects[:-1]
#         for obj in new_objects:
#             maya.xform(obj, centerPivots=True)
#             maya.parent(obj, world=True)

#         if maya.objExists(original_object):
#             maya.delete(original_object, ch=True)

#         new_group = maya.group(new_objects)
#         maya.select(new_group)
#         maya.inViewMessage(amg="Faces have been extracted into new object(s).", pos="topCenter", fade=True)

#         return new_objects

#     except RuntimeError as e:
#         maya.error(f"Failed to separate faces: {e}.")


def set_pivot_world_space():
    selection = maya.ls(selection=True)
    if not selection:
        return
    maya.xform(selection, pivots=(0, 0, 0), worldSpace=True)


def set_obj_world_space():
    selection = maya.ls(selection=True)

    if not selection:
        return

    maya.move(0, 0, 0, selection, rpr=True)


def select_every_other_face():
    """
    Selects every other face on the first selected mesh object.
    """
    selection = maya.ls(selection=True, transforms=True)
    if not selection:
        maya.warning("No objects selected.")
        return

    mesh_shapes = maya.listRelatives(selection[0], shapes=True, type="mesh", fullPath=True)
    if not mesh_shapes:
        maya.warning(f"No mesh found under {selection[0]}.")
        return

    shape = mesh_shapes[0]
    shape_faces = maya.ls(f"{shape}.f[*]", flatten=True)
    if not shape_faces:
        maya.warning("No faces found on the selected mesh.")
        return

    every_other_face = shape_faces[::2]
    maya.select(every_other_face)
    return every_other_face


def select_faces_with_material(material):
    selection = maya.ls(selection=True, type="transform")
    if not selection:
        maya.warning("Please select one or more mesh objects.")
        return

    sg = maya.listConnections(material, type="shadingEngine")
    if not sg:
        maya.warning(f"No shadingEngine found for material {material}")
        return

    faces_to_select = []
    for obj in selection:
        faces = [f for f in maya.sets(sg, q=True) or [] if f.startswith(obj + ".")]
        faces_to_select.extend(faces)

    if faces_to_select:
        maya.select(faces_to_select)
    else:
        maya.warning("No matching faces found on the selected objects.")


def change_outliner_colour(colour):
    COLOURS = {"green": (0, 1, 0), "red": (1, 0, 0), "blue": (0, 0, 1)}

    colour = colour.strip().lower()
    rgb = COLOURS.get(colour)
    if not rgb:
        maya.warning(f"Unknown colour: {colour}")
        return

    root = maya.ls(selection=True, type="transform", long=True)
    if not root:
        maya.warning("Select a group")
        return

    # only targeting direct children, not recursive.
    root_children = maya.listRelatives(root[0], children=True, type="transform", fullPath=True) or []
    for node in root_children:
        if not maya.listRelatives(node, shapes=True):
            maya.setAttr(f"{node}.useOutlinerColor", 1)
            maya.setAttr(f"{node}.outlinerColor", *rgb)

    maya.setAttr(f"{root[0]}.useOutlinerColor", 1)
    maya.setAttr(f"{root[0]}.outlinerColor", *rgb)
