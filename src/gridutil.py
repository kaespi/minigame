
def grid_index_up(node_x, node_y):
    """Returns the indices for the node's (given by node_x/node_y coordinate) grid element in up direction"""
    ix_v = int(node_y) * 2 - 1
    ix_h = int(node_x)
    return ix_v, ix_h


def grid_index_right(node_x, node_y):
    """Returns the indices for the node's (given by node_x/node_y coordinate) grid element in right direction"""
    ix_v = int(node_y) * 2
    ix_h = int(node_x)
    return ix_v, ix_h


def grid_index_down(node_x, node_y):
    """Returns the indices for the node's (given by node_x/node_y coordinate) grid element in down direction"""
    ix_v = int(node_y) * 2 + 1
    ix_h = int(node_x)
    return ix_v, ix_h


def grid_index_left(node_x, node_y):
    """Returns the indices for the node's (given by node_x/node_y coordinate) grid element in right direction"""
    ix_v = int(node_y) * 2
    ix_h = int(node_x) - 1
    return ix_v, ix_h


def grid_index(x, y):
    """Returns the index of the grid element on which this position appers"""
    if int(y) == y:
        # horizontal grid element...
        ix_v = int(y) * 2
        ix_h = int(x)
    elif int(x) == x:
        # vertical grid element...
        ix_v = int(y) * 2 + 1
        ix_h = int(x)
    else:
        # unknown grid element...
        ix_v = None
        ix_h = None
    return ix_v, ix_h
