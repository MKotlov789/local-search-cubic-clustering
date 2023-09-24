import itertools
import time
from algorithm._basegreedyclustering import _BaseGreedyClustering


class GreedyMovingKl(_BaseGreedyClustering):
    """
    A class that implements the Greedy Moving-KL clustering algorithm.

    Inherits from _BaseGreedyClustering.

    Methods:

    greedy_moving():
        Performs an iteration if the Greedy Moving-KL clustering algorithm.
    do_clustering(measure_time=False):
        Executes the clustering process and measures the execution time.
    """
    def __init__(self, instance):
        super().__init__(instance)

        for node_index in range(self.node_number):
            self._nodes_index_partition.append({node_index})

    def _count_obj_func_change(self, moving_node_ind, move_from_set_ind, move_to_set_ind):
        """
                Calculate the change in the objective function when moving a node between sets.

                Args:
                moving_node_ind (int): Index of the node to be moved.
                move_from_set_ind (int): Index of the set to move the node from.
                move_to_set_ind (int): Index of the set to move the node to.

                Returns:
                float: Change in the objective function.
                """
        k = 1

        if move_from_set_ind == -1:
            changing_set = self._nodes_index_partition[move_to_set_ind]
        else:
            changing_set = self._nodes_index_partition[move_from_set_ind]
            k = -1

        sum = 0
        for elem in itertools.combinations(changing_set, 2):
            e1 = elem[0]
            e2 = elem[1]
            if moving_node_ind != e1 and moving_node_ind != e2:
                key = tuple(sorted([moving_node_ind, e1, e2]))
                sum += k * self.costs[key][1]

        return sum

    def _move_ind(self, moving_node_ind, move_from_set_ind, move_to_set_ind, change_set=False):

        if change_set:
            self._nodes_index_partition[move_to_set_ind].add(moving_node_ind)
            self._nodes_index_partition[move_from_set_ind].remove(moving_node_ind)

    def move(self, moving_node_ind, move_from_set_ind, move_to_set_ind, no_remove=False):
        """
                Move a node from one set to another.

                Args:
                moving_node_ind (int): Index of the node to be moved.
                move_from_set_ind (int): Index of the set to move the node from.
                move_to_set_ind (int): Index of the set to move the node to.
                no_remove (bool): If True, do not remove the node from the original set.

                Returns:
                None
                """

        self._nodes_index_partition[move_to_set_ind].add(moving_node_ind)
        self._nodes_index_partition[move_from_set_ind].remove(moving_node_ind)
        if not no_remove:
            self._removed.add(moving_node_ind)

        for key in dict(self.move_dif_dict).keys():
            if (key[0] == moving_node_ind) or (key[1] == move_to_set_ind or key[1] == move_from_set_ind) or (
                    key[2] == move_to_set_ind or key[2] == move_from_set_ind):
                del self.move_dif_dict[key]

    def _update_move_dif_dict(self, changed_sets_ind):
        """
                Update the dictionary of move differences based on changes in sets.

                Args:
                changed_sets_ind (list): List of indices of sets that have undergone changes.

                Returns:
                None
                """

        for move_from_set_ind in range(len(self._nodes_index_partition)):
            for node_ind in self._nodes_index_partition[move_from_set_ind]:
                if node_ind not in self._removed:
                    delta1 = self._count_obj_func_change(node_ind, move_from_set_ind=move_from_set_ind,
                                                         move_to_set_ind=-1)
                    for move_to_set_ind in range(len(self._nodes_index_partition)):
                        if self._nodes_index_partition[
                            move_to_set_ind] != set() and move_from_set_ind != move_to_set_ind and (
                                (move_to_set_ind in changed_sets_ind) or (move_from_set_ind in changed_sets_ind)):
                            delta2 = self._count_obj_func_change(node_ind, move_from_set_ind=-1,
                                                                 move_to_set_ind=move_to_set_ind)
                            self.move_dif_dict[(node_ind, move_from_set_ind, move_to_set_ind)] = delta2 + delta1
                    if move_from_set_ind in changed_sets_ind:
                        self.move_dif_dict[(node_ind, move_from_set_ind, -1)] = delta1

    def greedy_moving(self):
        self._removed = set()
        self.move_dif_dict = {}

        log = []
        sum_min = 0
        sum = 0
        changed_sets_ind = range(len(self._nodes_index_partition))

        while (len(self._removed) < self.node_number):
            self._update_move_dif_dict(changed_sets_ind)
            move = min(self.move_dif_dict, key=self.move_dif_dict.get)
            node_ind, move_from_set_ind, move_to_set_ind = move
            dif = self.move_dif_dict[move]
            if move_to_set_ind == -1:
                self._nodes_index_partition.append(set())
                move_to_set_ind = len(self._nodes_index_partition) - 1
            log.append([node_ind, move_from_set_ind, move_to_set_ind])
            sum += dif
            if round(sum, 15) < sum_min:
                sum_min = sum
                log.clear()

            self.move(node_ind, move_from_set_ind, move_to_set_ind)
            changed_sets_ind = [move_from_set_ind, move_to_set_ind]

        for node_ind in log:
            self._move_ind(node_ind[0], node_ind[2], node_ind[1], change_set=True)
        while set() in self._nodes_index_partition:
            self._nodes_index_partition.remove(set())
        print(self._nodes_index_partition)
        if round(sum_min, 15) >= 0:
            return False
        else:
            return True

    def do_clustering(self, measure_time=False):
        if measure_time:
            start = time.time()
        cont = True

        while cont:
            cont = self.greedy_moving()

        if measure_time:
            end = time.time()
            self.time = end - start
        self.nodes_partition = self._index_to_node(self._nodes_index_partition)
