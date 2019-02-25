
from solver import *
from collections import deque

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

        # Went all the way down to a leaf, backtrack
        if (to_move >= len(movables)):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.gs_queue = deque()
        self.visited_states = deque() # added to make faster

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
        # Mark this move as explored
        self.visited[self.currentState] = True
        self.visited_states.append(self.currentState.state)

        # Get move to make
        movables = self.gm.getMovables()
        # print("EXPLORING GAME STATE " + str(self.gm.getGameState()) + "---------------------------------------------------------")
        to_move = self.currentState.nextChildToVisit # movables index
        # print("depth ", self.currentState.depth)

        # Return if done
        if self.currentState.state == self.victoryCondition:
            # print("DONE")
            return True

        # If current state has no children, make children
        if not self.currentState.children:
            for movable_statement in movables:
                # Make the move
                # print("implementing move ", movable_statement)
                self.gm.makeMove(movable_statement)

                # Create a new state with this move made
                new_state = self.gm.getGameState()
                # print ("new state ", new_state)

                # If the new state hasn't been visited and isn't in the queue then add it as a child and to the queue
                if (new_state not in self.visited_states):
                    new_gs = GameState(new_state, self.currentState.depth + 1, movable_statement)
                    new_gs.parent = self.currentState
                    self.currentState.children.append(new_gs)
                    self.currentState.nextChildToVisit = to_move + 1
                    self.visited[new_gs] = True
                    self.visited_states.append(new_state)
                    self.gs_queue.append(new_gs)

                self.gm.reverseMove(movable_statement)

        # Return false if no more to explore
        if not self.gs_queue:
            return False

        # Revert to state at when current and next start to change
        root_curr = self.currentState
        self.currentState = self.gs_queue.popleft()
        root_new = self.currentState

        # Backtrack to when current node and new node start to diverge
        if root_new.depth == root_curr.depth:
            while root_curr.state != root_new.state:
                self.gm.reverseMove(root_curr.requiredMovable)
                root_curr = root_curr.parent
                root_new = root_new.parent
        else:
            while root_curr.requiredMovable:
                self.gm.reverseMove(root_curr.requiredMovable)
                root_curr = root_curr.parent

        # Return game master to state that we are exploring
        # Find path between root and current state
        path = []
        currNode = self.currentState
        while currNode != root_curr:
            path.append(currNode.requiredMovable)
            currNode = currNode.parent

        # Created backwards path, now make moves from root to current state
        path.reverse()
        for movable_statement in path:
            self.gm.makeMove(movable_statement)

        return False
