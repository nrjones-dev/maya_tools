import maya.cmds as maya


def get_parent_chain(node):
    """
    Returns all parent transforms of a node, from immediate parent up to root.
    """

    parents = []
    current = node
    while True:
        parent = maya.listRelatives(current, parent=True, fullPath=True)
        if not parent:
            break
        parents.append(parent[0])
        current = parent[0]
    return parents


def find_common_parent(nodes):
    """
    Finds the deepest common parent shared by the given nodes.
    """
    if not nodes:
        return None

    parent_chains = [get_parent_chain(n) for n in nodes]

    common_parents = set(parent_chains[0])

    for chain in parent_chains[1:]:
        common_parents &= set(chain)

    if not common_parents:
        return None

    return max(common_parents, key=lambda p: p.count("|"))
