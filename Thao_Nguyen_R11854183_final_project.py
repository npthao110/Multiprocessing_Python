import argparse
import os
import sys
import multiprocessing as mp
from array import array

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the cellular life simulator.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input matrix file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output matrix file.")
    parser.add_argument("-p", "--processes", type=int, default=1, help="Number of processes to use (default: 1). Must be > 0.")
    args = parser.parse_args()
    return args

#read from input file
def read_matrix(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f if line.strip()]

#write to output file
def write_matrix(matrix, file_path):
    with open(file_path, 'w') as f:
        for row in matrix:
            f.write(row + '\n')

#sets of prime and power of 2 to check
PRIMES = {2, 3, 5, 7, 11, 13}
POWERS_OF_2 = {1, 2, 4, 8, 16}

def update_cell(value, neighbor_sum):
    if value == 2 and neighbor_sum in POWERS_OF_2:
        return 0
    elif value == 2 and neighbor_sum < 10:
        return 1
    elif value == 1 and neighbor_sum <= 0:
        return 0
    elif value == 1 and neighbor_sum >= 8:
        return 2
    elif value == 0 and neighbor_sum in PRIMES:
        return 1
    elif value == 0 and abs(neighbor_sum) in PRIMES:
        return -1
    elif value == -1 and neighbor_sum >= 1:
        return 0
    elif value == -1 and neighbor_sum <= -8:
        return -2
    elif value == -2 and abs(neighbor_sum) in POWERS_OF_2:
        return 0
    elif value == -2 and neighbor_sum > -10:
        return -1
    else:
        return value

#8 directions to go
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

def calculate_neighbor_sum(matrix, row, col):
    neighbor_sum = 0
    rows, cols = len(matrix), len(matrix[0])
    for dr, dc in DIRECTIONS:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbor_sum += matrix[new_r][new_c]
    return neighbor_sum

#processes a chunk of the matrix by updating the state of each cell in the assigned rows.
def process_chunk(args):
    matrix, rows_to_process, total_rows, total_cols = args
    updated_rows = []
    for r in rows_to_process:
        new_row = array('i', [0] * total_cols)  #array of signed integer 'i'
        for c in range(total_cols):
            neighbor_sum = calculate_neighbor_sum(matrix, r, c)
            new_value = update_cell(matrix[r][c], neighbor_sum)
            new_row[c] = new_value
        updated_rows.append((r, new_row))
    return updated_rows

def process_matrix_parallel(matrix, num_processes):
    rows, cols = len(matrix), len(matrix[0])
    if num_processes > rows:
        num_processes = rows
    #create list of row indices
    row_indices = list(range(rows))
    #divides the list of row indices into interleaved chunks, step = num_processes
    chunks = [row_indices[i::num_processes] for i in range(num_processes)]
    args_list = [(matrix, chunk, rows, cols) for chunk in chunks]
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, args_list)
    #assemble new_matrix 
    new_matrix = [None] * rows
    for updated_rows in results:
        for r, new_row in updated_rows:
            new_matrix[r] = new_row
    return new_matrix

def main():
    print("Project :: R11854183", file=sys.stdout)
    args = parse_arguments()

    #get input matrix
    input_matrix = read_matrix(args.input)

    #convert symbols to numeric representation using arrays
    symbol_to_value = {'O': 2, 'o': 1, 'X': -2, 'x': -1, '.': 0}
    numeric_matrix = [array('i', [symbol_to_value[cell] for cell in row]) for row in input_matrix]

    #process the matrix for 100 iterations
    for _ in range(100):
        numeric_matrix = process_matrix_parallel(numeric_matrix, args.processes)

    #convert numeric matrix to symbols
    value_to_symbol = {2: 'O', 1: 'o', -2: 'X', -1: 'x', 0: '.'}
    output_matrix = [''.join([value_to_symbol[cell] for cell in row]) for row in numeric_matrix]

    #final output matrix
    write_matrix(output_matrix, args.output)
    print(f"Output file written to: {os.path.abspath(args.output)}")

if __name__ == '__main__':
    main()
