import maya.cmds as m


def clean_combine():
    curr_selection = m.ls(selection=True)
    try:
        m.polyUnite(curr_selection, constructionHistory=False)
        m.xform(centerPivots=True)
        m.warning("objects have been merged.")
    except RuntimeError:
        m.error("Invalid Selection. Combine needs at least 2 polygonal objects selected.")


def clean_detach():
    selection = m.ls(selection=True)

    # Ensure that the selection consists of faces
    try:
        if selection and all(".f[" in s for s in selection):
            original_object = selection[0].split(".")[0]

            separated_objects = m.polySeparate(original_object, rs=True, ch=False)

            m.parent(m.ls(selection=True), world=True)
            m.delete(original_object, ch=False)
            m.select(separated_objects[:-1])

            new_objects = m.ls(selection=True)
            for obj in new_objects:
                m.xform(centerPivots=True)

            m.warning("Faces have been separated into a new object")
    except RuntimeError:
        m.error("Invalid Selection. Please select faces from a polygonal object.")


def set_pivot_world_space():
    selection = m.ls(selection=True)

    if not selection:
        return
    m.xform(selection, pivots=(0, 0, 0), worldSpace=True)


def set_obj_world_space():
    selection = m.ls(selection=True)

    if not selection:
        return

    m.move(0, 0, 0, selection, rpr=True)


def select_every_other_face():
    shape = m.ls(selection=True)
    shape_faces = m.ls(f"{shape[0]}.f[*]", flatten=True)
    face_selection = m.select(shape_faces[::2])


def select_faces_with_material(obj, material):
    sg = m.listConnections(material, type="shadingEngine")
    if sg:
        faces = [f for f in m.sets(sg, q=True) or [] if f.startswith(obj + ".")]
        m.select(faces) if faces else print("No matching faces found.")


# Example usage
select_faces_with_material("pCube1", "lambert1")
