import numpy as np
from sys import argv
import matplotlib.pyplot as plt
from multiprocessing import Pool


def generate_random_lists(n: int):
    """Generate random lists of numbers

    Args:
        n: number of lists to generate

    Returns:
        list of lists of random numbers
    """
    np.random.seed(100)
    lists = [np.random.randint(n, size=(n)) for _ in range(n)]
    return lists

def loop_logic(number: int, lists):
    # create a list of successes for the given index
    successes = []
    for index_list in lists:
        # find the max value in the list
        max_ = max(index_list)
        # start the max loop at -inf
        if number == 0:
            max_look = index_list[0]
        else:
            max_look = max(index_list[:number])
        for j in range(len(index_list[number:])):
            if index_list[j] > max_look:
                # if the value at the index is the actual max
                if index_list[j] == max_:
                    successes.append(1)
                break
    # find the precent of total successes for the given index
    return (number, len(successes))


def create_stats(file = None):
    np.random.seed(100)
    n = 1000
    # generate random lists
    if file:
        with open(file) as f:
            lists = [np.genfromtxt(f)]
    else:
        lists = generate_random_lists(n)
    precent_success_for_given_index = np.zeros(n)

    # loop through all the indices
    list_of_index = [(i, lists) for i in range(n)]
    with Pool() as pool:
        for result in pool.starmap(loop_logic, list_of_index):
            number, success = result
            precent_success_for_given_index[number] = success
        pool.close()
    print(precent_success_for_given_index.shape)

    plt.bar(np.arange(n), precent_success_for_given_index)
    plt.show()

if __name__ == "__main__":
    if len(argv) == 2:
        create_stats(argv[1])
    else:
        create_stats()

