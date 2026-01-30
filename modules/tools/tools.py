import maya.cmds as maya


def clean_combine():
    curr_selection = maya.ls(selection=True)
    try:
        maya.polyUnite(curr_selection, constructionHistory=False)
        maya.xform(centerPivots=True)
        maya.warning("objects have been merged.")
    except RuntimeError:
        maya.error("Invalid Selection. Combine needs at least 2 polygonal objects selected.")


def clean_detach():
    selection = maya.ls(selection=True)
    # Ensure that the selection consists of faces
    try:
        if selection and all(".f[" in s for s in selection):
            original_object = selection[0].split(".")[0]

            separated_objects = maya.polySeparate(original_object, rs=True, ch=False)

            maya.parent(maya.ls(selection=True), world=True)
            maya.delete(original_object, ch=False)
            maya.select(separated_objects[:-1])
            new_objects = maya.ls(selection=True)
            for obj in new_objects:
                maya.xform(centerPivots=True)

            maya.warning("Faces have been separated into a new object")
    except RuntimeError:
        maya.error("Invalid Selection. Please select faces from a polygonal object.")


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
    shape = maya.ls(selection=True)
    shape_faces = maya.ls(f"{shape[0]}.f[*]", flatten=True)
    face_selection = maya.select(shape_faces[::2])
    return face_selection


def select_faces_with_material(obj, material):
    sg = maya.listConnections(material, type="shadingEngine")
    if sg:
        faces = [f for f in maya.sets(sg, q=True) or [] if f.startswith(obj + ".")]
        maya.select(faces) if faces else print("No matching faces found.")


def change_outliner_colour(colour):
    COLOURS = {
        "green": (0, 1, 0),
        "red": (1, 0, 0),
    }

    colour = colour.strip().lower()
    rgb = COLOURS.get(colour)
    if not rgb:
        maya.warning(f"Unknown colour: {colour}")
        return

    root = maya.ls(selection=True, type="transform")
    if not root:
        maya.warning("Select a group")
        return

    # only targeting direct children, not recursive.
    root_children = maya.listRelatives(root[0], children=True, type="transform") or []
    for node in root_children:
        if not maya.listRelatives(node, shapes=True):
            maya.setAttr(f"{node}.useOutlinerColor", 1)
            maya.setAttr(f"{node}.outlinerColor", *rgb)
