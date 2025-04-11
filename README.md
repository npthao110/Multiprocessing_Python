# Python Multiprocessing

This project demonstrates how parallel programming can significantly improve the performance of computationally intensive tasks. By simulating 100 iterations of a cellular automaton, I explore how Python's `multiprocessing` module can be used to divide work across multiple processes, even in a language not optimized for concurrency.

## Project Summary
The program simulates a matrix-based system where each cell updates based on its neighbors using specific rules. It consists of:

- A serial version of the simulation
- A parallel version using the `multiprocessing` module

The matrix is processed for 100 generations and the result is written to an output text file. Users can specify input and output paths, as well as the number of processes, through command-line arguments.

## Scale of Computation
This project, running on `High Performance Computing (HPC)`, is designed to handle large-scale data:

- Tested on matrix sizes up to 10,000 × 10,000
- Runs 100 iterations per execution
- Executed with up to 32 parallel processes
- Serial execution for 10,000 × 10,000 matrices can take over 50 minutes
- Optimized parallel execution reduces this time to approximately 36.5 minutes

## Learning Outcomes
- Applied Python's `multiprocessing` module for performance improvement
- Gained experience with large-scale matrix computations
- Understood the impact of language selection on parallel program design
- Managed concurrency using only standard Python modules
- Optimized key parts of the simulation logic using `array` module for more memory efficiency, faster access and iteration than regular Python lists

## Limitations
- Use of external libraries such as `NumPy` or `SciPy` is not allowed
- Only base Python 3 modules were used (compatible with Python 3.12.1)



