from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES


class GameBoard:
    """
    Game board manager class. Encapsulates behaviors concerning the state of the board.
    """

    def __init__(self):
        """
        Initialize `board` as the adjacency matrix for the starting board.
        Use `Color.NONE` for edges that do not exist, and `Color.UNCOLORED` for the other edges.
        """
        self.board: Board = [
            [Color.NONE if i == j else Color.UNCOLORED for j in range(NUM_NODES)]
            for i in range(NUM_NODES)
        ]

    def color_edge(self, edge: Edge, color: Color) -> None:
        """
        Update `board` to reflect coloring the given edge.
        """
        i, j = edge
        self.board[i][j] = color
        self.board[j][i] = color

    def get_winner(self) -> Color | None:
        """
        Return the color of the player that has won (Color.P1 or Color.P2).
        If the game is still in progress (no one has won yet), return None.
        """
        b = self.board
        for i in range(NUM_NODES):
            for j in range(i + 1, NUM_NODES):
                c = b[i][j]
                if c != Color.P1 and c != Color.P2:
                    continue
                for k in range(j + 1, NUM_NODES):
                    if b[i][k] == c and b[j][k] == c:
                        # The player who formed a triangle loses.
                        return Color.P2 if c == Color.P1 else Color.P1
        return None

    def __str__(self):
        """
        Formats the board as a string. Provided for your convenience while debugging.
        """
        string = ""
        for row in self.board:
            for item in row:
                string += "{edge:<10}".format(edge=item.name)
            string += "\n"
        return string
