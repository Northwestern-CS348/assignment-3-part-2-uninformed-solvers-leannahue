
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # Mark this move as explored
        self.visited[self.currentState] = True

        # Get move to make
        movables = self.gm.getMovables()
        # print("EXPLORING GAME STATE " + str(self.gm.getGameState()) + "---------------------------------------------------------")
        to_move = self.currentState.nextChildToVisit # movables index
        # print("depth ", self.currentState.depth)

        # Return if done
        if self.currentState.state == self.victoryCondition:
            # print("DONE")
            return True

        while to_move < len(movables):
            # Make the move
            movable_statement = movables[to_move]
            # print("implementing move ", movable_statement)
            self.gm.makeMove(movable_statement)

            # Create a new state with this move made
            new_state = self.gm.getGameState()

            # Find out if this state has already been explored
            visited = False
            for visited_state in self.visited.keys():
                if visited_state.state == new_state:
                    visited = True

            # If the new state hasn't been visited then add it as a child then move down to this child
            if not visited:
                new_gs = GameState(new_state, self.currentState.depth + 1, movable_statement)
                new_gs.parent = self.currentState
                self.currentState.children.append(new_gs)
                self.currentState.nextChildToVisit = to_move + 1
                self.currentState = new_gs
                break

            # Else skip this state and try going to the next movable statement
            else:
                # print("SKIP THIS STATE")
                self.gm.reverseMove(movable_statement)
                to_move += 1

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
