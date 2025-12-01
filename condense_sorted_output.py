import sys
from matplotlib import pyplot as plt

def main():
    if len(sys.argv) < 2:
        print(f"USAGE: python3 {sys.argv[0]} <sorted_output_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        lines = f.read().split('\n')

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
    yp = [totals[x][0] / 1e6 for x in xs]
    ys = [totals[x][1] / 1e6 for x in xs]
    yc = [totals[x][2] / 1e6 for x in xs]

    plt.plot(xs, yp)
    plt.title("Quicksort on Array of 4 million elements")
    plt.xlabel("Depth")
    plt.ylabel("Partition Instructions (Millions)")
    plt.show()

    plt.plot(xs, ys, color='orange')
    plt.title("Quicksort on Array of 4 million elements")
    plt.xlabel("Depth")
    plt.ylabel("Swap Count (Millions)")
    plt.show()

    plt.plot(xs, yc, color='green')
    plt.title("Quicksort on Array of 4 million elements")
    plt.xlabel("Depth")
    plt.ylabel("Comparison Count (Millions)")
    plt.show()

if __name__ == '__main__':
    main()

