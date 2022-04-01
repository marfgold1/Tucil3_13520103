from enum import Enum
from typing import List, Tuple, Union


class MoveDirection(Enum):
    """Valid move direction

    Args:
        Enum (Enum): Enumerable type object.
    """
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class Puzzle:
    def __init__(self, context, last_map, action=None, last_center=None, depth=0, parent=None) -> None:
        """Initialize new puzzle node.

        Args:
            context (Solver): The solver context for this puzzle.
            last_map (list[list]): The map before action applied.
            action (MoveDirection, optional): The direction of move action. Defaults to None.
            last_center (tuple[int,int], optional): The position of empty block. Defaults to None.
            depth (int, optional): The depth of this puzzle node. Defaults to 0.
            parent (Puzzle, optional): The puzzle parent of this node. Defaults to None.
        """
        self.context = context
        """The solver context for this puzzle."""
        self.depth = depth
        """The depth of this puzzle node."""
        self.parent:Puzzle = parent
        """The parent of this puzzle node"""
        self.children: List[Puzzle] = []
        """The childrens of this puzzle node."""
        self.map_ = [ [ last_map[i][j] for j in range(4) ] for i in range(4) ]
        """The map of this puzzle node."""
        self.action:MoveDirection = action
        """The action taken for this puzzle node."""
        self.__center:Tuple[int,int] = None
        """The position of empty block in this puzzle node."""
        if last_center is None:
            self.get_center() # If root, we find manually the empty block pos
        else: # if not root, we adjust from center point beforehand.
            self.__center = self.get_next_point(last_center, action)
            self.swap(last_center, self.__center)
        self.cost = self.depth + self.__h()
        """The cost of this puzzle node."""

    def __h(self) -> int:
        """Get the heuristic cost approximation of this node.

        Cost approximation is based on the number of misplaced
        tiles in compare to the goal state (except empty tile).

        Returns:
            int: The heuristic cost approximation of this node.
        """
        cnt = 0
        for i in range(4):
            for j in range(4):
                # Exclude empty tile AND check if the tile[i][j] is misplaced
                if (i, j) != self.__center and self.map_[i][j] - 1 != i * 4 + j:
                    cnt += 1
        return cnt

    def swap(self, p1, p2):
        """Swap the number of two tiles in coord p1 and p2.

        Args:
            p1 (Tuple[int,int]): Tile 1 coordinate.
            p2 (Tuple[int,int]): Tile 2 coordinate.
        """
        temp = self.map_[p1[0]][p1[1]]
        self.map_[p1[0]][p1[1]] = self.map_[p2[0]][p2[1]]
        self.map_[p2[0]][p2[1]] = temp

    def calc_next(self) -> None:
        """Calculate the next puzzle node.
        """
        self.children.clear()
        for act in MoveDirection:
            # For every move, we check if it's in map boundary
            if self.is_valid_pos(act):
                # If it's in boundary, we create a new puzzle node
                new_puzzle = Puzzle(
                    self.context,
                    self.map_,
                    act,
                    self.__center,
                    self.depth + 1,
                    self
                )
                # Check if we already visit the puzzle.
                # If not, we append to the child.
                # If yes, we delete the new puzzle.
                if not self.context.visit(new_puzzle):
                    self.children.append(new_puzzle)
                else:
                    del new_puzzle

    def is_valid_pos(self, action:MoveDirection) -> bool:
        """Check if action returning to valid position.

        Valid position is 0 <= i <= 3 and 0 <= j <= 3.

        Args:
            action (MoveDirection): The direction move.

        Returns:
            bool: Validity of the action.
        """
        next_point = self.get_next_point(self.__center, action)
        return (
            next_point[0] >= 0 and next_point[0] < 4
            and next_point[1] >= 0 and next_point[1] < 4
        )

    def is_solution(self) -> bool:
        """Check if this node is a solution node.

        Returns:
            bool: True if node is a solution node.
        """
        for i in range(4):
            for j in range(4):
                if self.map_[i][j] - 1 != i * 4 + j:
                    return False
        return True

    @staticmethod
    def get_next_point(pfrom:Tuple[int,int], action:MoveDirection) -> Tuple[int,int]:
        """Get the next empty block position after move action.

        Will calculate the next empty block from pfrom
        based on the action that will be taken.

        Args:
            pfrom (tuple[int,int]): The last position of empty block.
            action (MoveDirection): The action that will be taken.

        Returns:
            Tuple[int,int]: The next point after action taken.
        """
        res = [pfrom[0], pfrom[1]]
        if action == MoveDirection.DOWN:
            res[0] += 1
        elif action == MoveDirection.UP:
            res[0] -= 1
        elif action == MoveDirection.LEFT:
            res[1] -= 1
        elif action == MoveDirection.RIGHT:
            res[1] += 1
        return (res[0], res[1])
    
    def get_center(self) -> Union[Tuple[int, int], None]:
        """Get the empty block position if any.

        Returns:
            Union[Tuple[int, int], None]: The empty block position.
        """
        if self.__center is None:
            for i in range(4):
                for j in range(4):
                    if self.map_[i][j] == 16:
                        self.__center = (i, j)
        return self.__center

    def __lt__(self, other) -> bool:
        """Lower than comparison for this object.

        Comparison is based on the node cost.

        Args:
            other (Puzzle): The other puzzle node to be compared with.

        Returns:
            bool: Is this puzzle cost lower than other puzzle cost.
        """
        return self.cost < other.cost

    def __str__(self) -> str:
        """Convert the puzzle map to string.

        Returns:
            str: String representation of the puzzle map.
        """
        return "".join([
            "\n".join([" ".join(
                map(lambda x: str(x) if x != 16 else "-", v)
            )
            for v in self.map_]),
            "\nStep {} | Action {}".format(
                self.depth,
                self.action.name
            ) if self.action else ""
        ])
