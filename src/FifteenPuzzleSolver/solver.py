from queue import PriorityQueue
from time import perf_counter_ns
from FifteenPuzzleSolver.puzzle import Puzzle


class Solver:
    NONE_VALUE = 16

    def __init__(self, maps:str=None) -> None:
        """Create a new solver with maps.

        Args:
            maps (str, optional): Map to solve.
                Defaults to None.

        Raises:
            Exception: Invalid configuration map.
        """
        if maps is None: # We generate map from input
            self.map = [ 
                [
                    int(x) if x.isnumeric()
                    else Solver.NONE_VALUE
                    for x in input().split(' ')
                ]
                for _ in range(4)
            ]
            print("Searching for solution...")
        else: # Generate map from file
            self.map = [
                [
                    int(x) if x.isnumeric()
                    else Solver.NONE_VALUE
                    for x in s.split(' ')
                ]
                for s in maps.splitlines()
            ]
        # Check if map is valid (matrix 4x4)
        valid = len(self.map) == 4
        for i in self.map:
            if len(i) != 4:
                valid = True
        if not valid:
            raise Exception(
                "Invalid configuration map. Map is not a matrix 4 x 4."
            )
        # Reset, create root, and precalculate kurang(i), and solve
        self.reset()
        self.root = Puzzle(self, self.map)
        self.calc_kurang = [
            self.kurang(i*4+j+1)
            for j in range(4)
            for i in range(4)
        ]
        self.solve()

    def kurang(self, num) -> int:
        """Kurang(i) implementation.

        Args:
            num (int): Number to calculate as i.

        Returns:
            int: Kurang(num).
        """
        cnt = 0
        for i in range(4):
            for j in range(4):
                if self.map[i][j] == num:
                    for a in range(i, 4):
                        for b in range(4):
                            if a == i and b < j:
                                continue
                            if self.map[a][b] < self.map[i][j]:
                                cnt += 1
                    return cnt
        return cnt

    def visit(self, puzzle) -> bool:
        """Visit a puzzle.

        Args:
            puzzle (Puzzle): Puzzle to visit.

        Returns:
            bool: is puzzle already visited.
        """
        s = str(puzzle)
        if s in self.__visited:
            return True
        else:
            self.__visited[s] = True
            return False

    def reset(self):
        """Reset solver."""
        self.runtime = 0
        self.final = None
        self.count_nodes = 0
        self.__visited = {}

    def solve(self):
        """Solve this puzzle instantiation.
        """
        # Start timer
        self.runtime = perf_counter_ns()
        # If we can solve, create prioqueue, add root
        # to the queue and visit it.
        if self.can_solve():
            queue = PriorityQueue()
            queue.put(self.root)
            self.visit(self.root)
            # We visit every node in the queue
            # until we found the solution.
            while not queue.empty():
                m:Puzzle = queue.get()
                if m.is_solution():
                    self.final = m
                    break
                m.calc_next()
                for c in m.children:
                    self.count_nodes += 1
                    queue.put(c)
        # Stop timer and calculate runtime
        self.runtime = (perf_counter_ns() - self.runtime) * 0.000000001 #in seconds
    
    def bound(self) -> int:
        """Get the required bound to solve the puzzle.

        Returns:
            int: sum(kurang(i)) + X.
        """
        t = self.root.get_center()
        return (
            sum(self.calc_kurang)
            + (1 if any([
                (t[i%2] % 2 == 0 and t[(i+1)%2] % 2 != 0)
                for i in range(2)
            ]) else 0)
        )

    def can_solve(self):
        """Check if we can solve this puzzle.

        The puzzle can be solved if it has even bound.

        Returns:
            bool: If this puzzle can be solved.
        """
        return (self.bound() % 2 == 0)

    @staticmethod
    def solve_path(final) -> str:
        """Traverse to the root and return the path.

        Args:
            final (Puzzle): Solution node puzzle.

        Returns:
            str: Path from root to final node.
        """
        res = ""
        if final.parent is not None:
            res += Solver.solve_path(final.parent)
        return res + str(final) + "\n\n"

    def describe(self, show_solution=False) -> str:
        """Return string representation of this solver.

        Args:
            show_solution (bool, optional): Include solution path.
                Defaults to False.

        Returns:
            str: String representation of this solver.
        """
        return "\n\n".join([
            "> Initial Map",
            str(self.root),
            "> Kurang(i)",
            "\n".join([
                " ".join([
                    str(self.calc_kurang[j+i*4])
                    for j in range(4)
                ])
                for i in range(4)
            ]),
            "> Sum(kurang(i)) + X",
            str(self.bound()),
            (
                "> Solution\n\n" + (
                    "No solution found" if not self.can_solve()
                    else "Solution found!\n" + self.solve_path(self.final)
                ) + "\n> Runtime"
            ) if show_solution else "> Runtime",
            str(self.runtime) + "s",
            "> Node Count",
            str(self.count_nodes)
        ])

    def __str__(self) -> str:
        """Return string representation of this solver.

        Also includes the solution path.

        Returns:
            str: String representation with solution path.
        """
        return self.describe(True)
