import numpy as np
import matplotlib.pyplot as plt


def generate_random_lists(n: int):
    """Generate random lists of numbers

    Args:
        n: number of lists to generate

    Returns:
        list of lists of random numbers
    """
    np.random.seed(40)
    lists = [np.random.randint(n, size=(n)) for _ in range(n)]
    return lists


def create_stats():
    np.random.seed(40)
    n = 1000
    # generate random lists
    lists = generate_random_lists(n)
    precent_success_for_given_index = []

    # loop through all the indices
    for i in range(n):
        print(f"i = {i}...")
        # create a list of successes for the given index
        successes = []
        for index_lis in lists:
            # find the max value in the list
            max_ = max(index_lis)
            # start the max loop at -inf
            max_look = -np.inf
            for j in range(n):
                # while the index is less than the loop index for cutoff of 
                # look time
                if i >= j:
                    # if the value at the index is greater than the max look
                    max_look = max(max_look, index_lis[j])
                # after the look time
                else:
                    # if the value at the index is greater than the max look
                    if index_lis[j] >= max_look:
                        # print(f"index_lis[j] = {index_lis[j]} > max_look = {max_look}")
                        # if the value at the index is the actual max
                        if index_lis[j] == max_: 
                            # print(f"index_lis[j] = {index_lis[j]} == max_ = {max_}")
                            successes.append(1)
                        break

        # find the precent of total successes for the given index
        precent_success_for_given_index.append(len(successes))
    plt.bar([i for i in range(n)], precent_success_for_given_index)
    plt.show()

if __name__ == "__main__":
    create_stats()
        
        
        



