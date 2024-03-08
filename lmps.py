import sys
from datetime import time


def read_input(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parsing input
    num_nodes = int(lines[0].strip())
    labels = [line.strip() for line in lines[1:]]

    # Build adjacency matrix of chords
    chord_table = [""] * num_nodes
    i = 0

    for label in labels:
        chord_table[i] = label
        i = i + 1
    return num_nodes, chord_table

def write_output(output_file, result):
    with open(output_file, 'w+') as file:
        file.write(f"{result[0]}\n")
        for edge in result[1]:
            file.write(f"{edge[0]} {edge[1]}\n")

def print_chords(labels, dp, i, j):
    result = []
    if i>=j:
        return result
    if labels[i] == labels[j] and dp[i][j] == dp[i + 1][j - 1] + 1:
        result.append((i,j))
        result.extend(print_chords(labels, dp, i + 1, j - 1))
    elif dp[i][j] == dp[i][j - 1]:
        result.extend(print_chords(labels, dp, i, j - 1))
    else:
        for k in range(i, j):
            if labels[k] == labels[j] and dp[i][j] == dp[i][k - 1] + dp[k + 1][j - 1] + 1:
                result.extend(print_chords(labels, dp, i, k - 1))
                result.append((k,j))
                result.extend(print_chords(labels, dp, k + 1, j - 1))
                break
    return result
def maximum_planar_subset(num_nodes, labels):
    # implementation for mps task goes here
    # Return a tuple (size_of_subset, subset_edges)
    #initialization
    dp = [[0] * num_nodes for _ in range(num_nodes)]
    memo = [[] * num_nodes for _ in range(num_nodes*num_nodes)]
    for j in range(num_nodes):
        label_j = labels[j]
        temp = []
        pos = 0
        for k in range(num_nodes):
            if label_j == labels[k] and k != j:
                temp.append(k)

        for i in range(j):

            if temp == []:
                dp[i][j] = dp[i][j - 1]

            else:
                for k in temp:
                    #case1: k is not in (i,j)
                    if k < i or k > j:
                        dp[i][j] = max(dp[i][j - 1],dp[i][j])
                    #case2
                    elif k == i:
                        if i == j - 1:
                            dp[i][j] = 1
                        else:
                            dp[i][j] = max(dp[i + 1][j - 1] + 1, dp[i][j])
                    #case3
                    else:
                        if dp[i][j - 1] <= dp[i][k - 1] + dp[k + 1][j - 1]:
                                dp[i][j] = max(dp[i][k - 1] + dp[k + 1][j - 1] + 1, dp[i][j])
                        else:
                            dp[i][j] = max(dp[i][j], dp[i][j - 1])

    result = print_chords(labels, dp, 0, num_nodes - 1)
    return dp[0][num_nodes - 1], result

if __name__ == "__main__":
    import time
    t0 = time.time()
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    num_nodes, chord_table = read_input(input_file)
    # Determine the task based on the number of nodes
    # Execute lmps task
    result = maximum_planar_subset(num_nodes, chord_table)
    write_output(output_file, result)
    t1 = time.time()
    print(t1 - t0)