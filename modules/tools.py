import maya.cmds as maya


def clean_combine():
    curr_selection = maya.ls(selection=True)
    maya.polyUnite(curr_selection, constructionHistory=False)
    print("Test")


def clean_detach():
    selection = maya.ls(selection=True)

    # Ensure that the selection consists of faces
    if selection and all(".f[" in s for s in selection):
        original_object = selection[0].split(".")[0]

        separated_objects = maya.polySeparate(original_object, rs=True, ch=False)

        maya.parent(maya.ls(selection=True), world=True)
        maya.delete(original_object, ch=False)
        maya.select(separated_objects[:-1])

        new_objects = maya.ls(selection=True)
        for obj in new_objects:
            maya.xform(centerPivots=True)

        print("Faces have been separated into a new object")
    else:
        print("Please select faces from a polygonal object.")


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
    print(face_selection)


def select_faces_with_material(obj, material):
    sg = maya.listConnections(material, type="shadingEngine")
    if sg:
        faces = [f for f in maya.sets(sg, q=True) or [] if f.startswith(obj + ".")]
        maya.select(faces) if faces else print("No matching faces found.")


# Example usage
select_faces_with_material("pCube1", "lambert1")
