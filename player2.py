from __future__ import annotations
from itertools import combinations

from consts import Board, Color, Edge, NUM_NODES


def _forms_triangle(player: Color, board: Board, i: int, j: int) -> bool:
    """True if coloring edge (i, j) with `player` would complete a triangle of that color."""
    for k in range(NUM_NODES):
        if k != i and k != j and board[i][k] == player and board[j][k] == player:
            return True
    return False


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim
    """

    @staticmethod
    def get_move(board: Board) -> Edge:
        """
        Return a possible move for the second player (blue) that follows the optimal strategy laid out in the handout,
        given the input board state. If multiple moves are viable, this method can return any of them.
        """
        mini = Player2.get_miniboard(board)
        if mini is None:
            mini = board

        candidates = Player2.get_allowed_moves(Color.P2, mini)
        if len(candidates) <= 1:
            return candidates[0]

        # Step 3: greatest number of maximal P2-allowed sets
        p2_sets = Player2.get_maximal_allowed_sets(Color.P2, mini)
        counts = {m: sum(1 for s in p2_sets if m in s) for m in candidates}
        best = max(counts.values())
        candidates = [m for m in candidates if counts[m] == best]
        if len(candidates) == 1:
            return candidates[0]

        # Step 4: greatest number of maximal P1-allowed sets
        p1_sets = Player2.get_maximal_allowed_sets(Color.P1, mini)
        counts = {m: sum(1 for s in p1_sets if m in s) for m in candidates}
        best = max(counts.values())
        return next(m for m in candidates if counts[m] == best)

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        required = [
            n
            for n in range(NUM_NODES)
            if any(board[n][m] in (Color.P1, Color.P2) for m in range(NUM_NODES) if m != n)
        ]
        others = [n for n in range(NUM_NODES) if n not in required]

        # Add the fewest extra nodes possible, so the result is minimal.
        for extra in range(len(others) + 1):
            for added in combinations(others, extra):
                nodes = set(required) | set(added)
                mini: Board = [
                    [
                        board[i][j] if (i in nodes and j in nodes and i != j) else Color.NONE
                        for j in range(NUM_NODES)
                    ]
                    for i in range(NUM_NODES)
                ]
                if Player2.get_allowed_moves(Color.P2, mini):
                    return mini
        return None

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """
        moves = Player2.get_allowed_moves(player, board)

        # Adjacency of the player's already-colored edges; chosen edges are added temporarily.
        adj = [set() for _ in range(NUM_NODES)]
        for i in range(NUM_NODES):
            for j in range(NUM_NODES):
                if i != j and board[i][j] == player:
                    adj[i].add(j)

        best = -1
        results: set[frozenset[Edge]] = set()
        chosen: list[Edge] = []

        def search(idx: int) -> None:
            nonlocal best, results
            if len(chosen) + (len(moves) - idx) < best:
                return
            if idx == len(moves):
                size = len(chosen)
                if size > best:
                    best = size
                    results = {frozenset(chosen)}
                elif size == best:
                    results.add(frozenset(chosen))
                return
            i, j = moves[idx]
            if not (adj[i] & adj[j]):
                adj[i].add(j)
                adj[j].add(i)
                chosen.append((i, j))
                search(idx + 1)
                chosen.pop()
                adj[i].discard(j)
                adj[j].discard(i)
            search(idx + 1)

        search(0)
        return results

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.
        """
        return [
            (i, j)
            for i in range(NUM_NODES)
            for j in range(i + 1, NUM_NODES)
            if board[i][j] == Color.UNCOLORED and not _forms_triangle(player, board, i, j)
        ]
