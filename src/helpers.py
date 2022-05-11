from src.vertex_class import Vertex

def preprocess(data):
    vertex_data_dict = {}
    max_gain = 0
    with open(data) as f:
        for line in f:
            items = str(line).split()
            # from_item is the attribute: number, which is the id of the vertex
            id = items[0]
            to_items = items[3:]
            gain_to_items = len(to_items)
            if gain_to_items > max_gain:
                max_gain = gain_to_items
            # all vertex objects start with partition 0?
            vertex = Vertex(id, 0, 0, to_items)
            vertex_data_dict[id] = vertex
    return vertex_data_dict, max_gain
