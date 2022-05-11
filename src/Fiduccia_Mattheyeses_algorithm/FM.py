import random


class FM_agorithm:
    """The Fiduccia-Mattheyeses heuristic"""

    def __init__(self, vertex_data_dict, max_gain):
        # need dict in reverse order
        self.left_gain_bucket = {i: set() for i in range(max_gain, -max_gain - 1, -1)}
        self.left_gain_bucket_l = 0
        self.right_gain_bucket = {i: set() for i in range(max_gain, -max_gain - 1, -1)}
        self.right_gain_bucket_l = 0
        self.vertex_data_dict = vertex_data_dict
        self.total_cuts = 0

    def getPartition(self):
        return [self.vertex_data_dict[key].partition for key in self.vertex_data_dict]

    def create_split(self):
        length_vertex_list = len(self.vertex_data_dict)
        half_length = int(length_vertex_list / 2)
        zero_partition = [0 for i in range(half_length)]
        one_partition = [1 for i in range(half_length)]
        solution = zero_partition + one_partition
        random.shuffle(solution)
        for i, key in enumerate(self.vertex_data_dict):
            self.vertex_data_dict[key].partition = solution[i]

    def set_split(self, solution):
        for i, key in enumerate(self.vertex_data_dict):
            self.vertex_data_dict[key].partition = solution[i]

    def reset_gains(self):
        for key in self.vertex_data_dict:
            vertex = self.vertex_data_dict[key]
            vertex.gain = 0
            vertex.cuts = 0

    def calculate_gain(self):
        for key in self.vertex_data_dict:
            vertex = self.vertex_data_dict[key]
            for key_neighbor in vertex.neighbors:
                neighbor_vertex = self.vertex_data_dict[key_neighbor]
                if neighbor_vertex.partition == vertex.partition:
                    vertex.gain -= 1
                else:
                    vertex.gain += 1
                    vertex.cuts += 1

    def calculate_cuts(self):
        self.total_cuts = 0
        for key in self.right_gain_bucket:
            for number in self.right_gain_bucket[key]:
                # print(self.vertex_data_dict[number].cuts)
                self.total_cuts += self.vertex_data_dict[number].cuts

    def getCuts(self):
        return self.total_cuts

    def fill_buckets(self):
        for key in self.vertex_data_dict:
            vertex = self.vertex_data_dict[key]
            vertex_partition = vertex.partition
            vertex_gain = vertex.gain
            vertex_number = vertex.number
            if vertex_partition == 0:
                self.left_gain_bucket_l += 1
                self.left_gain_bucket[vertex_gain].add(vertex_number)
            else:
                self.right_gain_bucket_l += 1
                self.right_gain_bucket[vertex_gain].add(vertex_number)

    def roll_back_to_best_solution(self, roll_back_list, index_best_solution):
        # print(roll_back_list)
        steps_back = len(roll_back_list) - index_best_solution - 1

        for index in range(steps_back):
            if roll_back_list[index] == "nothing changed":
                break
            vertex = self.vertex_data_dict[roll_back_list[index]]
            vertex.partition = 1 - vertex.partition

    def select_bucket(self):
        if self.left_gain_bucket_l > self.right_gain_bucket_l:
            bucket_to_search = self.left_gain_bucket
            self.left_gain_bucket_l -= 1
        else:
            bucket_to_search = self.right_gain_bucket
            self.right_gain_bucket_l -= 1
        return bucket_to_search

    def update_neighbors_gains(self, vertex_to_lock):
        """updates the gains of the neighbors of the locked vertex"""
        # reposition vertex
        vertex_to_lock.partition = 1 - vertex_to_lock.partition

        # search for neighbors and update their gains according to replaced vertex
        neighbors = vertex_to_lock.neighbors
        for neighbor in neighbors:
            # get neighbor from list
            neighbor_vertex = self.vertex_data_dict[neighbor]
            # get partition of neighbor
            neighbor_vertex_partition = neighbor_vertex.partition
            if neighbor_vertex_partition == 0:
                neighbor_bucket_to_search = self.left_gain_bucket

            else:
                neighbor_bucket_to_search = self.right_gain_bucket

            # get neigbor gain
            neighbor_gain = neighbor_vertex.gain
            # delete neigbor from bucket if already deleted do nothing
            if neighbor in neighbor_bucket_to_search[neighbor_gain]:
                neighbor_bucket_to_search[neighbor_gain].remove(neighbor)
                # update gain
                if neighbor_vertex.partition == vertex_to_lock.partition:
                    neighbor_vertex.gain -= 2
                else:
                    neighbor_vertex.gain += 2
                # insert in bucket
                neighbor_bucket_to_search[neighbor_vertex.gain].add(neighbor)

    def fm_pass(self):
        # fill buckets
        amount_iterations = self.left_gain_bucket_l + self.right_gain_bucket_l
        total_cuts_array = []
        roll_back_list = []
        total_cuts_array.append(self.total_cuts)
        roll_back_list.append("nothing changed")
        while amount_iterations > 0:
            bucket_to_search = self.select_bucket()
            for gain in bucket_to_search:
                if len(bucket_to_search[gain]) != 0:
                    # delete from bucket
                    number_to_lock = random.sample(bucket_to_search[gain], 1)[0]
                    bucket_to_search[gain].remove(number_to_lock)

                    # get vertex
                    vertex_to_lock = self.vertex_data_dict[number_to_lock]
                    self.update_neighbors_gains(vertex_to_lock)
                    # change amount_total_cuts by gain of vertex
                    self.total_cuts -= gain

                    roll_back_list.append(number_to_lock)
                    total_cuts_array.append(self.total_cuts)
                    # update amount_iterations
                    amount_iterations -= 1
                    break

        even_total_cuts = total_cuts_array[::2]
        min_index_even = len(even_total_cuts) - even_total_cuts[::-1].index(min(even_total_cuts)) - 1
        min_index_total = min_index_even * 2
        self.roll_back_to_best_solution(roll_back_list[::-1], min_index_total)

        return self.vertex_data_dict, total_cuts_array[min_index_total]
