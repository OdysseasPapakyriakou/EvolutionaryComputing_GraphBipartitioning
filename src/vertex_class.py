class Vertex:

    def __init__(self, number, gain, partition, neighbors) -> None:
        self.gain = gain
        self.partition = partition
        self.number = number
        self.neighbors = neighbors
        self.cuts = 0
