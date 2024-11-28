import argparse
import os
import sys

# set of primes and power of 2 numbers
PRIMES = {2, 3, 5, 7, 11, 13}
POWERS_OF_2 = {1, 2, 4, 8, 16}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the cellular life simulator.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input matrix file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output matrix file.")
    parser.add_argument("-p", "--processes", type=int, default=1, help="Number of processes to use (default: 1). Must be > 0.")
    args = parser.parse_args()

    # Validate input file
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Validate output directory
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.isdir(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Validate process count
    if args.processes <= 0:
        print("Error: Number of processes must be > 0.", file=sys.stderr)
        sys.exit(1)

    return args

#read from input file
def read_matrix(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f]

#write to output file
def write_matrix(matrix, file_path):
    with open(file_path, 'w') as f:
        for row in matrix:
            f.write(''.join(row) + '\n')

#Check if a number is prime by looking up in a set
def is_prime(num):
    return num in PRIMES

#Check if a number is a power of 2 by looking up in a set
def is_powerof2(num):
    return num in POWERS_OF_2

#Calculate the sum of neighbor cells based on their values.
def calculate_neighbor_sum(matrix, row, col, directions):
    rows, cols = len(matrix), len(matrix[0])
    neighbor_sum = 0
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor_sum += matrix[nr][nc]
    return neighbor_sum

#Update the value of a cell based on the rules.
def update_cell(value, neighbor_sum):
    if value == 2:  # Healthy O Cell
        if is_powerof2(neighbor_sum):
            return 0  # Dies
        elif neighbor_sum < 10:
            return 1  # Becomes Weakened o
    elif value == 1:  # Weakened o Cell
        if neighbor_sum <= 0:
            return 0  # Dies
        elif neighbor_sum >= 8:
            return 2  # Becomes Healthy O
    elif value == 0:  # Dead Cell
        if is_prime(neighbor_sum):
            return 1  # Becomes Weakened o
        elif is_prime(abs(neighbor_sum)):
            return -1  # Becomes Weakened x
    elif value == -1:  # Weakened x Cell
        if neighbor_sum >= 1:
            return 0  # Dies
        elif neighbor_sum <= -8:
            return -2  # Becomes Healthy X
    elif value == -2:  # Healthy X Cell
        if is_powerof2(abs(neighbor_sum)):
            return 0  # Dies
        elif neighbor_sum > -10:
            return -1  # Becomes Weakened x
    return value  # Remains unchanged

#Process the matrix for one iteration (serial implementation).
def process_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),            (0, 1),
        (1, -1),   (1, 0),  (1, 1)]

    #declare a matrix to store intermediate values
    new_matrix = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbor_sum = calculate_neighbor_sum(matrix, r, c, directions)
            new_matrix[r][c] = update_cell(matrix[r][c], neighbor_sum)
    return new_matrix


def main():
    print("Project :: R11854183", file=sys.stdout) 
    args = parse_arguments()

    # Read the input matrix
    input_matrix = read_matrix(args.input)

    # Convert symbols to numeric representation
    symbol_to_value = {'O': 2, 'o': 1, 'X': -2, 'x': -1, '.': 0}
    numeric_matrix = [[symbol_to_value[cell] for cell in row] for row in input_matrix]

    # Process the matrix for 100 iterations
    for _ in range(100):
        numeric_matrix = process_matrix(numeric_matrix)

    # Convert numeric matrix back to symbols
    value_to_symbol = {2: 'O', 1: 'o', -2: 'X', -1: 'x', 0: '.'}
    output_matrix = [[value_to_symbol[cell] for cell in row] for row in numeric_matrix]

    # Write the final output matrix
    write_matrix(output_matrix, args.output)

if __name__ == '__main__':
    main()
