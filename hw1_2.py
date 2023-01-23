import numpy as np
from sys import argv
import typing
import matplotlib.pyplot as plt
from multiprocessing.pool import Pool
from copy import deepcopy as dc
from IPython import display


def _generate_random_lists(n: int):
    "Generate list of lists with n size and n range."

    list_of_lists = [np.random.uniform(n, size=(n)) for _ in range(n)]
    return list_of_lists

def loop_logic(stopping_num: int, lists: typing.List[typing.List[int]]) -> typing.Tuple[int, int]:
    """Calculate the number of success for given stoping number.

    Args:
        stopping_num: The index to stop the look phase.
        lists: the list of lists of random numbers.

    Returns:
        The stopping index and the number of success for the given index
    """
    success = []
    for list_ in lists:
        max_ = max(list_)
        max_look = max(list_[:stopping_num + 1])
        for number in list_[stopping_num + 1:]:
            # max_look  = _decrement_max(stopping_num, number, n)
            if number > max_look:
                if number == max_:
                    success.append(1)
                break
    return (stopping_num, len(success)) 

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

def max_benifit_stopping_loop(index, list_):
    best_benifit = 0
    best_index = 0
    for i, num in enumerate(list_):
        reward = num - i
        if reward > best_benifit:
            best_benifit = reward
            best_index = i
    return best_index, index

def max_benifit_stopping(lists, n):
    list_of_best_indecies = np.zeros(n)
    params = [(i, list_) for i, list_ in enumerate(lists)]
    with Pool() as pool:
        for result in pool.starmap(max_benifit_stopping_loop, params):
            best_index, curr_index = result
            list_of_best_indecies[curr_index] = best_index
    plt.bar([i for i in range(n)], list_of_best_indecies)
    print(np.median(list_of_best_indecies))
    plt.show()
            

    
def _main(files: typing.List[str] = None):
    np.random.seed(42)
    n = 1000
    if files:
        list_of_lists = []
        for file in files:
            with open(file) as f:
                list_of_lists.append(np.genfromtxt(file))
    else:
        list_of_lists = _generate_random_lists(n)
    list_of_params = [(i, list_of_lists) for i in range(n - 1)]
    list_of_success = np.zeros(n - 1, dtype=int)
    with Pool() as pool:
        for result in pool.starmap(loop_logic, list_of_params):
            stop_num, num_success = result
            list_of_success[stop_num] = num_success
    range_of_success = [i for i in range(n-1)]
    plt.bar(range_of_success, list_of_success)
    msg = ""
    for i, x in zip(range_of_success, list_of_success):
        if i % 10 == 0 and not i == 0:
            msg += "\n"
        msg += f"{i}: {[x]}, "
    print(msg)
    plt.show()
    max_benifit_stopping(list_of_lists, n)

if __name__ == "__main__":
    if len(argv) >= 2:
        _main(argv[1:])
    else:
        _main()
                
                

            

    
    
