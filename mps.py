import sys
from datetime import time


def read_input(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parsing input
    num_nodes = int(lines[0].strip())
    edges = [tuple(map(int, line.strip().split())) for line in lines[1:] if line.strip() != 'EOF']

    # Build adjacency matrix of chords
    chord_table = [-1] * num_nodes
    for edge in edges:
        chord_table[edge[0]] = edge[1]
        chord_table[edge[1]] = edge[0]
    return num_nodes, chord_table
def write_output(output_file, result):
    with open(output_file, 'w+') as file:
        file.write(f"{result[0]}\n")
        for edge in result[1]:
            file.write(f"{edge[0]} {edge[1]}\n")

def print_chords(chords, dp, i, j, result):
    k = chords[j]
    if i < j:
         if k != -1:
            if (k < i or k > j):
                print_chords(chords, dp, i, j - 1, result)
            elif k == i:
                result.append((i, j))
                print_chords(chords, dp, i + 1, j - 1, result)
            else:
                if dp[i][j - 1] <= dp[i][k - 1] + dp[k + 1][j - 1]:
                    result.append((k, j))
                    print_chords(chords, dp, k + 1, j - 1, result)
                    print_chords(chords, dp, i, k - 1, result)
                else:
                    print_chords(chords, dp, i, j - 1, result)
         else:
            print_chords(chords, dp, i, j - 1, result)

    return result
def maximum_planar_subset(num_nodes, chords):
    # implementation for mps task goes here
    # Return a tuple (size_of_subset, subset_edges)
    #initialization
    dp = [[0] * num_nodes for _ in range(num_nodes)]

    for j in range(1,num_nodes):
        for i in range(j):
            k = chords[j]
            if k != -1:
                #case1: k is not in (i,j)
                if(k < i or k > j):
                    dp[i][j] = dp[i][j - 1]
                #case2
                elif (k == i):
                   if i == j - 1:
                        dp[i][j] = 1
                   else:
                        dp[i][j] = dp[i + 1][j - 1] + 1
                #case3
                else:
                    if (dp[i][j - 1] <= dp[i][k - 1] + dp[k + 1][j - 1]):
                        dp[i][j] = dp[i][k - 1] + dp[k + 1][j - 1] + 1
                    else:
                        dp[i][j] = dp[i][j - 1]
            else:
                dp[i][j] = dp[i][j - 1]

    result = print_chords(chords, dp, 0, num_nodes - 1, [])

    return dp[0][num_nodes - 1], result

if __name__ == "__main__":
    import time
    t0 = time.time()
    import sys

    sys.setrecursionlimit(5000)
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    num_nodes, chord_table = read_input(input_file)
    # Determine the task based on the number of nodes
    # Execute mps task
    result = maximum_planar_subset(num_nodes, chord_table)
    write_output(output_file, result)
    t1 = time.time()
    print(t1 - t0)
