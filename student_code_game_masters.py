from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        disks = {}
        disk = ''
        ask = [parse_input("fact: (on ?disk peg1)")]
        ask.append(parse_input("fact: (on ?disk peg2)"))
        ask.append(parse_input("fact: (on ?disk peg3)"))
        tuples = []
        for question in range(3):
            bindings = self.kb.kb_ask(ask[question])
            disks[question] = []
            if bindings:
                for b in bindings:
                    b = list(b.bindings_dict.values())[0]
                    disk = int(''.join(el for el in b if el.isdigit()))
                    disks[question].append(disk)
            tuples.append(tuple(sorted(disks[question])))

        tuples = tuple(tuples)
        return tuples

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        # Parse movable input
        disk = movable_statement.terms[0].term.element
        init_peg = movable_statement.terms[1].term.element
        init_peg_num = int(''.join(el for el in init_peg if el.isdigit()))
        new_peg = movable_statement.terms[2].term.element

        # Change what's on what
        fact = parse_input("fact: (on " + disk + " " + init_peg + ")")
        self.kb.kb_retract(fact)
        new_fact = parse_input("fact: (on " + disk + " " + new_peg + ")")
        self.kb.kb_assert(new_fact)

        # Change empties and tops for destination peg
        old_empty = parse_input("fact: (empty " + new_peg + ")")
        self.kb.kb_retract(old_empty)
        old_top_binding = self.kb.kb_ask(parse_input("fact: (top ?disk " + new_peg + ")"))
        old_top_disk = ''
        if old_top_binding:
            old_top_disk = old_top_binding[0].bindings[0].constant.element
        old_top_dst = parse_input("fact: (top " + old_top_disk + " " + new_peg + ")")
        self.kb.kb_retract(old_top_dst)
        new_top_dst = parse_input("fact: (top " + disk + " " + new_peg + ")")
        self.kb.kb_assert(new_top_dst)

        # Change empties and tops for original peg
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + init_peg + ")"))
        on_init_peg = self.getGameState()[init_peg_num - 1]
        if not on_init_peg:
            new_empty = parse_input("fact: (empty " + init_peg + ")")
            self.kb.kb_assert(new_empty)
        else:
            self.kb.kb_assert(parse_input("fact: (top disk" + str(on_init_peg[0]) + " " + init_peg + ")"))

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        tiles = {}
        tile = ''
        ask_start = "fact: (coordinate ?tile "
        tuples = []
        for xpos in range(3):
            col = "pos" + str(xpos + 1)
            tiles[xpos] = []
            for ypos in range(3):
                row = "pos" + str(ypos + 1)
                ask = parse_input(ask_start + row + " " + col + ")")
                bindings = self.kb.kb_ask(ask)
                if bindings:
                    for b in bindings:
                        b = list(b.bindings_dict.values())[0]
                        if (b == 'empty'):
                            tile = -1
                        else:
                            tile = int(''.join(el for el in b if el.isdigit()))
                        tiles[xpos].append(tile)
            tuples.append(tuple(tiles[xpos]))

        tuples = tuple(tuples)
        return tuples

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        # Parse movable input
        tile = movable_statement.terms[0].term.element
        init_x = movable_statement.terms[1].term.element
        init_x_num = int(''.join(el for el in init_x if el.isdigit()))
        init_y = movable_statement.terms[2].term.element
        dest_x = movable_statement.terms[3].term.element
        dest_y = movable_statement.terms[4].term.element

        # Retract old tile and empty spots
        old_tile_spot = parse_input("fact: (coordinate " + tile + " " + init_x + " " + init_y + ")")
        self.kb.kb_retract(old_tile_spot)
        old_empty_spot = parse_input("fact: (coordinate empty " + dest_x + " " + dest_y + ")")
        self.kb.kb_retract(old_empty_spot)

        # Change tile destination spot
        new_tile_spot = parse_input("fact: (coordinate " + tile + " " + dest_x + " " + dest_y + ")")
        self.kb.kb_assert(new_tile_spot)
        new_empty_spot = parse_input("fact: (coordinate empty " + init_x + " " + init_y + ")")
        self.kb.kb_assert(new_empty_spot)

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
