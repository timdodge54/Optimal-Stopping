import typing
from copy import deepcopy
from multiprocessing.pool import Pool
from sys import argv

import matplotlib.pyplot as plt
import numpy as np


def _generate_random_lists(n: int) -> typing.List[typing.List[int]]:
    "Generate list of lists with n size and n range."

    list_of_lists = [np.random.uniform(n, size=(n)) for _ in range(n)]
    return list_of_lists


def loop_logic(
    stopping_num: int, lists: typing.List[typing.List[int]]
) -> typing.Tuple[int, int]:
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
        max_look = max(list_[: stopping_num + 1])
        for number in list_[stopping_num + 1 :]:
            # max_look  = _decrement_max(stopping_num, number, n)
            if number > max_look:
                if number == max_:
                    success.append(1)
                break
    return (stopping_num, len(success))


def _decrement_max(
    max_: int, loop_number: int, stop_number: int, len_list: int
) -> float:
    """Decrement the max value based on the loop number."""
    if loop_number < stop_number:
        return max_
    total_diff = len_list - stop_number
    percent_diff = (loop_number - stop_number) / total_diff
    if np.random.random() < percent_diff:
        return max_ - (1 * (1 + percent_diff))
    return max_


def max_benifit_stopping_loop(
    stopping_number: int, lists: typing.List[typing.List[int]]
) -> typing.Tuple[int, int]:
    """Loop through the list and find the best benifit.

    Args:
        index: the index of the list
        list: the list of numbers

    Returns:
        the index of the best benifit and the index of the list
    """
    list_of_reward = []
    for list_ in lists:
        max_look = -np.inf
        for i, num in enumerate(list_):
            if i <= stopping_number:
                if num > max_look:
                    max_look = num - (stopping_number + 1)
            else:
                number_explored = i + 1
                reward = num - number_explored
                if reward > max_look:
                    list_of_reward.append(reward)
                    break
                elif i == len(list_) - 1:
                    list_of_reward.append(reward)
                    break
    average_reward = np.mean(list_of_reward)

    return average_reward, stopping_number


def max_benifit_stopping(n: int) -> None:
    """Loops through the list of lists and finds the best benifit.

    Args:
        lists: the list of lists of numbers 
        n: number of lists and elements in list 
    """
    listss = []
    list_uniform = [np.random.uniform(1, 99, size=(99)) for _ in range(n)]
    listss.append(list_uniform)
    list_normal = [np.random.normal(50, 10, size=(99)) for _ in range(n)]
    list_normal_cap = [
        [99 if num > 99 else 0 if num < 0 else num for num in list_]
        for list_ in list_normal
    ]
    listss.append(list_normal_cap)
    for i, lists in enumerate(listss):
        list_of_best_indecies = np.zeros(99)
        params = [(i, lists) for i in range(99)]
        with Pool() as pool:
            for result in pool.starmap(max_benifit_stopping_loop, params):
                best_index, stopping_number = result
                list_of_best_indecies[stopping_number] += best_index
        plt.bar(np.arange(99), list_of_best_indecies)
        plt.xlabel("Stopping Number")
        plt.ylabel("Average Reward")
        if i == 0:
            plt.title("Uniform Distribution")
        else:
            plt.title("Normal Distribution")
        plt.show()


def optimial_stopping(list_: typing.List[int], stopping_num: int) -> int:
    max_look = max(list_[:stopping_num])
    for i, num in enumerate(list_[stopping_num:]):
        max_look = _decrement_max(max_look, i, stopping_num, len(list_))
        if num > max_look:
            return num
    return list_[-1]


def percent_37(list_: typing.List[int]) -> int:
    thirty_seven = int(len(list_) * 0.37)
    max_look = max(list_[:thirty_seven])
    for i, num in enumerate(list_[thirty_seven:]):
        if num > max_look:
            return num
    return list_[-1]


def _main(files: typing.List[str] = None):
    # Part 1
    np.random.seed(30)
    n = 1000
    list_of_lists = _generate_random_lists(n)
    list_of_params = [(i, list_of_lists) for i in range(n - 1)]
    list_of_success = np.zeros(n - 1, dtype=int)
    with Pool() as pool:
        for result in pool.starmap(loop_logic, list_of_params):
            stop_num, num_success = result
            list_of_success[stop_num] = num_success
    range_of_success = [i for i in range(n - 1)]
    plt.bar(range_of_success, list_of_success)
    plt.xlabel("Stopping Number")
    plt.ylabel("Number of Success")
    plt.title("Vanilla Stopping Rule")
    plt.show()
    index_of_best = np.argmax(list_of_success)
    index_of_best = index_of_best / 1000
    print(f"Best Stopping Number: {index_of_best}")
    if files:
        list_of_lists = []
        for file in files:
            try:
                with open(file) as f:
                    info = np.genfromtxt(file, dtype=int)
                    index_stopping = int(len(info) * index_of_best)
                    optimal_value = optimial_stopping(info, index_stopping)
                    thirty_seven = percent_37(info)
                    print(f"Optimal Value: {optimal_value}")
                    print(f"37% Value: {thirty_seven}")
                    plt.title(file)
                    plt.bar(np.arange(len(info)), info)
                    plt.show()
            except FileNotFoundError:
                print(f"File {file} not found")
                exit()

    # Part 2
    max_benifit_stopping(n)


if __name__ == "__main__":
    if len(argv) >= 2:
        _main(argv[1:])
    else:
        _main()
