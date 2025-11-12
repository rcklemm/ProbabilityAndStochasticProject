import random
import subprocess
import os

def get_output(listfile: str, optlevel=0) -> str:
    result = subprocess.run(
        [f'./sort_tracking_O{optlevel}', listfile, 'sorted.list.txt'],
        capture_output=True,
        text=True
    )

    return result.stdout

def build_random_list(size: int, outfile: str) -> None:
    with open(outfile, 'w') as f:
        f.write(f'{size}\n')
        entries = ''
        for i in range(size):
            entry = random.randint(0, 2**30)
            entries += str(entry) + ' '
        f.write(entries)
    return

def main() -> None:
    for loglist in range(8, 20, 5):
        print(f"LIST SIZE 2^{loglist}:")
        for trial in range(5):
            print(f"TRIAL #{trial}")
            build_random_list(2**loglist, 'tmp.list.txt')
            out = get_output('tmp.list.txt')
            print(f"output:\n{out}")
            print()
            os.remove('tmp.list.txt')

    return


if __name__ == '__main__':
    main()

