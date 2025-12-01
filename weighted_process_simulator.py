import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt

def simulate_wbp(n, max_depth=200):
    """
    Simulate one realization of the Quicksort-weight WBP.
    
    n: array size (nodes die when weight < 1/n)
    max_depth: safety cutoff to prevent infinite loops

    Returns: dict depth -> number of alive nodes at that depth
    """
    cutoff = 1.0

    # level 0 has a single node of weight 1
    frontier = [n]
    depth_counts = defaultdict(int)
    depth_sums = defaultdict(float)
    depth_sums[0] = n
    depth_counts[0] = 1

    depth = 0
    while frontier and depth < max_depth:
        next_frontier = []

        for w in frontier:
            # kill the node if its weight is too small
            if w < cutoff:
                continue

            # draw U and generate two children
            U = np.random.rand()
            w1 = w * U
            w2 = w * (1 - U)

            # children are added only if they are alive
            if w1 >= cutoff:
                next_frontier.append(w1)
            if w2 >= cutoff:
                next_frontier.append(w2)

        depth += 1
        print(f"depth {depth} done")
        if next_frontier:
            depth_counts[depth] = len(next_frontier)
            depth_sums[depth] = sum(next_frontier)

        frontier = next_frontier

    return depth_counts, depth_sums


def monte_carlo(n, trials=2000, max_depth=200):
    """
    Run many trials and compute mean alive nodes per depth.
    """
    aggregate_cnt = defaultdict(float)
    aggregate_sum = defaultdict(float)

    for t in range(trials):
        sample_cnt, sample_sum = simulate_wbp(n, max_depth)
        for d, count in sample_cnt.items():
            aggregate_cnt[d] += count
        for d, s in sample_sum.items():
            aggregate_sum[d] += s

        print(f"Trial {t} done")

    # convert to average counts
    for d in aggregate_cnt:
        aggregate_cnt[d] /= trials
    for d in aggregate_sum:
        aggregate_sum[d] /= trials

    return aggregate_cnt, aggregate_sum


if __name__ == "__main__":
    n = 2**20
    trials = 100

    result_cnt, result_sum = monte_carlo(n, trials)

    # print the first 60 depths for inspection
    xs = []
    ys = []
    end = max(result_cnt.keys())
    for d in range(end):
        xs.append(d)
        ys.append(result_sum.get(d, 0.0) / 1e6)
        print(d, result_sum.get(d, 0.0))

    plt.plot(xs, ys)
    plt.xlabel("Generation")
    plt.ylabel("Elements left to sort (Millions)")
    plt.title("Weighted Branching Process Simulation on 4 million nodes")
    plt.show()

