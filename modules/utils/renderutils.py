import maya.app.renderSetup.model.renderSetup as renderSetup


def append_diffuse_to_render_layers(suffix=None, skip_master_layer=True):
    """
    Appends a suffix to the names of render layers in Maya's Render Setup.

    :param suffix: The suffix to append (default: "Diffuse")
    :param skip_master_layer: Whether to skip the defaultRenderLayer
    :return: List of tuples (old_name, new_name) of renamed layers
    """
    if not isinstance(suffix, str) or not suffix:
        print("Suffix must be a non-empty string")
        return []

    rs = renderSetup.instance()
    all_layers = rs.getRenderLayers()

    for layer in all_layers:
        layer_name = layer.name()

        if skip_master_layer and layer_name == "defaultRenderLayer":
            print(f"Skipping master layer: {layer_name}")
            continue

        if layer_name.endswith(suffix):
            print(f"Already has suffix, skipping: {layer_name}")
            continue

        new_name = f"{layer_name}_{suffix}"
        try:
            layer.setName(new_name)
            print(f"Renamed {layer_name} → {new_name}")
        except Exception as e:
            print(f"Failed to rename {layer_name}: {e}")


def count_render_layers():
    rs = renderSetup.instance()
    all_layers = rs.getRenderLayers()
    total_layers = len(all_layers)
    print("Total Render Layers:", total_layers)
    return total_layers
