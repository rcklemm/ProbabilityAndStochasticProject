import numpy as np
from scipy.stats import pearsonr
import sys
from collections import defaultdict

def normalized(arr):
    arr = np.array(arr, dtype=float)
    if arr.max() == 0:
        return arr
    return arr / arr.max()

def compute_corr(empirical, sim):
    L = min(len(empirical), len(sim))
    empirical = np.asarray(empirical[:L], float)
    sim = np.asarray(sim[:L], float)

    e_norm = normalized(empirical)
    s_norm = normalized(sim)

    r, p = pearsonr(e_norm, s_norm)

    return r*r

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
        #print(f"depth {depth} done")
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

def main():
    if len(sys.argv) < 2:
        print(f"USAGE: python3 {sys.argv[0]} <sorted_output_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        lines = f.read().split('\n')
    
    print("PARSING REAL DATA")
    part_instr = 0
    swp_cnt = 0
    cmp_cnt = 0
    depth = 0
    totals = {}
    for l in lines:
        if l.strip() == '':
            continue
        this_depth = int(l.split(' ')[0])
        if this_depth != depth:
            print(f"DEPTH {depth} totals: {part_instr} partition instructions, {swp_cnt} swaps, {cmp_cnt} comparisons")
            totals[depth] = (part_instr, swp_cnt, cmp_cnt)
            depth = this_depth
            swp_cnt = 0
            part_instr = 0
            cmp_cnt = 0
        this_part = int(l.split('=')[3].split(',')[0])
        this_swp = int(l.split('=')[4].split(',')[0])
        this_cmp = int(l.split('=')[5])      
        part_instr += this_part
        swp_cnt += this_swp
        cmp_cnt += this_cmp  

    print(f"DEPTH {depth} totals: {part_instr} partition instructions, {swp_cnt} swaps, {cmp_cnt} comparisons")
    totals[depth] = (part_instr, swp_cnt, cmp_cnt)

    xs = list(totals.keys())
    yp = [totals[x][0] for x in xs]
    ys = [totals[x][1] for x in xs]
    yc = [totals[x][2] for x in xs]


    print("GENERATING SIMULATION DATA")
    _, sim_sums = monte_carlo(2**22, trials=10)

    xsim = sim_sums.keys()
    ysim = [sim_sums.get(x, 0.0) for x in xsim]

    print("Correlation sim <-> instructions:")
    r1 = compute_corr(yp, ysim)
    print(f"r^2={r1}")

    print("Correlation sim <-> swaps:")
    r2 = compute_corr(ys, ysim)
    print(f"r^2={r2}")
    
    print("Correlation sim <-> compares:")
    r3 = compute_corr(yc, ysim)
    print(f"r^2={r3}")

if __name__ == '__main__':
    main()
