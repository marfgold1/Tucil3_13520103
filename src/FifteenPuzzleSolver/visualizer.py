import os
from tkinter import NORMAL, DISABLED, ttk, messagebox, Tk, StringVar, IntVar
from typing import List

from FifteenPuzzleSolver.solver import Solver
from src.FifteenPuzzleSolver.puzzle import Puzzle


class Visualizer(Tk):
    def __init__(self, solver=None) -> None:
        """Initialize a new visualizer.

        Args:
            solver (Solver, optional): Solver instantiation.
                Defaults to None.
        """
        super().__init__()
        self.resizable(0, 0)
        self.title("15-Puzzle Solver")

        # create input btn
        frame1 = ttk.Frame(self)
        frame1.rowconfigure(0, weight=4)
        # inp file
        self.filename = StringVar()
        inp_file = ttk.Entry(frame1, textvariable=self.filename)
        inp_file.grid(row=0, column=0, columnspan=3)
        # btn apply
        btn_apply = ttk.Button(frame1, text="Load", command=self.apply)
        btn_apply.grid(row=0, column=3)
        # btn solve
        self.btn_solve = ttk.Button(frame1, text="Solve", command=self.solve)
        self.btn_solve.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.btn_solve.config(state=DISABLED)
        # btn reset
        self.btn_reset = ttk.Button(frame1, text="Reset", command=self.reset)
        self.btn_reset.grid(row=1, column=3)
        self.btn_reset.config(state=DISABLED)

        frame_slider = ttk.Frame(self)
        # slider label
        slider_label = ttk.Label(frame_slider, text="Speed")
        slider_label.grid(row=2, column=0, sticky="ew", ipadx=5)
        # slider value
        self.anim_speed = IntVar(value=50)
        self.slider_speed = ttk.Scale(frame_slider, from_=50, to=500,
            variable=self.anim_speed, orient="horizontal",
            command=lambda _: slider_val_lbl.config(text=str(self.anim_speed.get()) + "ms"))
        self.slider_speed.grid(row=2, column=1, columnspan=2, sticky="ew")
        # slider value label
        slider_val_lbl = ttk.Label(frame_slider, text="50ms")
        slider_val_lbl.grid(row=2, column=3, sticky="ew", ipadx=5)
        
        # create grid frame
        frame2 = ttk.Frame(self, relief="sunken", borderwidth=2)
        self.grid_puzzle:List[ttk.Label] = []
        for i in range(4):
            for j in range(4):
                g = ttk.Label(frame2, text=str(i*4+j+1), style="Puzzle.TLabel")
                g.grid(row=i, column=j)
                self.grid_puzzle.append(g)
        self.grid_puzzle[15].grid_remove()

        # style the grid
        grid_style = ttk.Style(frame2)
        grid_style.configure("Puzzle.TLabel",
            font=("Arial", 20),
            background="#aeb9c8",
            foreground="#000",
            width=3,
            borderwidth=5,
            relief="raised",
            anchor="center",
        )

        # show frame
        frame1.grid(padx=5, pady=5)
        frame_slider.grid()
        frame2.grid(padx=5, pady=5)

        self.after_list = []
        self.solver = None

        if solver:
            self.solver = solver
            self.load_solver()
        
        self.mainloop()

    def load_solver(self) -> None:
        """Load the solver instance.
        """
        messagebox.showinfo("Load","\n".join([
            "Successfully load puzzle!",
            "{}",
            "{}",
        ]).format(
            "This puzzle can be solved!"
            if self.solver.can_solve() else
            "This puzzle can't be solved.",
            self.solver.describe()
        ))
        if self.solver.can_solve():
            self.btn_solve["state"] = NORMAL
            self.btn_reset["state"] = NORMAL
        else:
            self.btn_solve["state"] = DISABLED
            self.btn_reset["state"] = DISABLED
        self.update(self.solver.root.map_)

    def apply(self) -> None:
        """Apply text in input file.
        """
        try:
            with open(self.filename.get(), "r") as f:
                self.solver = Solver(f.read())
                self.load_solver()
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "File not found! Current working directory: {}"
                .format(os.getcwd())
            )

    def update(self, cur_map) -> None:
        """Update the grid with map.

        Args:
            cur_map (list[list[int]]): Map to update.
        """
        for i in range(4):
            for j in range(4):
                g = self.grid_puzzle[i*4+j]
                if g["text"] == "16": # bring back last tile 16
                    g.grid(row=i, column=j)
                if cur_map[i][j] == 16: # hide current tile 16
                    g.grid_remove()
                g["text"] = str(cur_map[i][j])

    def update_after(self, depth, map):
        """Update from after coroutine.

        Args:
            depth (int): The depth of this map.
            map (list[list[int]]): The map to update.
        """
        self.update(map)
        if depth == self.solver.final.depth:
            # We update gui to normal after reaching solution.
            self.btn_solve.config(state=NORMAL)
            self.slider_speed.config(state=NORMAL)

    def traverse(self, depth, cur_state:Puzzle):
        """Traverse the puzzle in a delay animation.

        It will continously traverse parent from child
        first, then update the grid from the parent to
        child by increasing the delay time as it
        reaches the final node.

        Args:
            depth (int): Current depth of the traverse.
            cur_state (Puzzle): Current puzzle to traverse.
        """
        if cur_state.parent is not None:
            self.traverse(depth-1, cur_state.parent)
        self.after_list.append(self.after(
            self.anim_speed.get()*(depth),
            lambda: self.update_after(depth, cur_state.map_)
        ))

    def solve(self) -> None:
        """Start the solve animation.
        """
        # Disable buttons
        self.btn_solve.config(state=DISABLED)
        self.slider_speed.config(state=DISABLED)
        # Stop any after coroutine if available and clear
        for i in self.after_list:
            self.after_cancel(i)
        self.after_list.clear()
        # Start traversing and animating the solution
        self.traverse(self.solver.final.depth, self.solver.final)

    def reset(self) -> None:
        """Reset the solve animation.
        """
        # Enable buttons
        self.btn_solve.config(state=NORMAL)
        self.slider_speed.config(state=NORMAL)
        # Stop any after coroutine if available and clear
        for i in self.after_list:
            self.after_cancel(i)
        self.after_list.clear()
        # Reset the grid to initial root
        self.update(self.solver.root.map_)

if __name__ == "__main__":
    v = Visualizer()
