import argparse
import os

from FifteenPuzzleSolver.solver import Solver

# Argument Parser
parser = argparse.ArgumentParser(
    description=' '.join([
        'Main driver of Fifteen Puzzle Solver.',
        'It will generate a solution path for the problem instantiation.',
        'You can supply manually the initial state of the puzzle to show in GUI by specify -i/--input and -g/--gui.',
    ]),
)
parser.add_argument('-f', '--file', help='input file path.')
parser.add_argument('-g', '--gui', help='show GUI visualizer.', action='store_true')
parser.add_argument('-i', '--input', help='get puzzle from input.', action='store_true')
args = parser.parse_args()

# Get solver
solver = None
if args.file: # if file is specified, load solver from it
    try:
        with open(args.file, 'r') as f:
            solver = Solver(f.read())
    except FileNotFoundError:
        parser.error('File not found! Current working directory: {}'.format(os.getcwd()))
elif not args.gui or args.input: # if it's not GUI or input stdin enabled, ask the input map.
    print('Please enter the matrix instantiation of the problem.')
    print('Format Example:')
    print()
    print('3 1 2 4')
    print('- 5 7 8')
    print('10 6 11 12')
    print('9 13 14 15')
    print()
    print('NOTE: You can use any non numeric string or number 16 as the blank space.')
    print()
    solver = Solver()

if args.gui: # If gui, show the gui
    # Lazy load the gui
    from FifteenPuzzleSolver.visualizer import Visualizer
    Visualizer(solver)
else: # if not gui, just print the solver state with the solution
    print(solver)