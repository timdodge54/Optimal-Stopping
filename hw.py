import numpy as np
import copy
from sys import argv
import matplotlib.pyplot as plt
from multiprocessing import Pool
import typing as t


def generate_random_lists(n: int):
    """Generate random lists of numbers.

    Args:
        n: number of lists to generate

    Returns:
        list of lists of random numbers
    """
    np.random.seed(100)
    lists = [np.random.randint(n, size=(n)) for _ in range(n)]
    return lists

def _decrement_max(max_: int, loop_number: int, stop_number: int, len_list: int) -> int:
    """Decrement the max value based on the loop number."""
    total_diff = len_list - stop_number
    if loop_number < stop_number:
        return max_
    else:
        if loop_number < stop_number + total_diff * 0.25:
            if np.random.random() > 0.75:
                return max_ - 1
        elif loop_number < stop_number + total_diff * 0.5:
            if np.random.random() > 0.5:
                return max_ - 1
        elif loop_number < stop_number + total_diff * 0.75:
            if np.random.random() > 0.25:
                return max_ - 1
        return max_  

def _loop_logic(stop_number: int, lists) -> t.Tuple[int, int]:
    """Create the logic for searaching all lists for a given index."""
    # create a list of successes for the given index
    print(stop_number)
    successes = []
    for index_list in lists:
        # find the max value in the list
        max_ = max(index_list)
        # true_max = copy.deepcopy(max_)
        # start the max loop at -inf
        max_look = max(index_list[:stop_number + 1])
        for j in range(len(index_list[stop_number + 1:])):
            # max_look = _decrement_max(max_look, j, stop_number, len(index_list))
            if index_list[j] > max_look:
                # if the value at the index is the actual max
                if index_list[j] == max_:
                     successes.append(1)
                break
    # find the precent of total successes for the given index
    return (stop_number, len(successes))


def create_stats(file: t.Optional[str] = None):
    np.random.seed(100)
    n = 1000
    # generate random lists
    if file:
        with open(file) as f:
            lists = [np.genfromtxt(f)]
    else:
        lists = generate_random_lists(n)
    precent_success_for_given_index = np.zeros(n - 1)

    # loop through all the indices
    list_of_index = [(i, lists) for i in range(n - 1)]
    with Pool() as pool:
        for result in pool.starmap(_loop_logic, list_of_index):
            number, success = result
            precent_success_for_given_index[number] = success
        pool.close()
    print(precent_success_for_given_index.shape)
    plt.bar(np.arange(n -1), precent_success_for_given_index)
    plt.show()

if __name__ == "__main__":
    if len(argv) == 2:
        create_stats(argv[1])
    else:
        create_stats()

