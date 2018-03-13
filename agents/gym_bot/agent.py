# Author: Xichen Ding
# Ported by: Jonathan Beaulieu
from typing import List

from envs.util import gomoku_util

from .. import Agent
from gym_gomoku import GomokuState


class Random(Agent):
    def start_game(self, action_space: List[int]) -> None:
        self.last_state = None
        self.other_move = None

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        if self.last_state:
            (self.other_move,) = state.others - self.last_state.others
        self.last_state = state
        return self.beginner_policy(state, self.other_move)

    def defend_policy(self, curr_state: GomokuState):
        '''Return the action Id, if defend situation is needed
        '''
        b = curr_state.board
        player_color = curr_state.color
        opponent_color = player_color.other

        # List all the defend patterns
        pattern_four_a = [0] + [opponent_color.value] * 4  # [0,1,1,1,1]
        pattern_four_b = [opponent_color.value] * 4 + [0]  # [1,1,1,1,0]
        pattern_three_a = [0] + [opponent_color.value] * 3 + [0]  # [0,1,1,1,0]
        pattern_three_b = [opponent_color.value] * 2 + [0] + [opponent_color.value] * 1  # [1,1,0,1]
        pattern_three_c = [opponent_color.value] * 1 + [0] + [opponent_color.value] * 2  # [1,0,1,1]
        patterns = [pattern_four_a, pattern_four_b, pattern_three_a, pattern_three_b, pattern_three_c]

        for p in patterns:
            action = self.connect_line(b, p)
            if action:  # Action is not none, pattern is found, place stone
                return action

        # No defend pattern found
        return None

    def fill_box(self, board, coord):
        ''' check the box area around the previous coord, if there is empty place in the empty area
            Return:
                action for within the box if there is empty
                random action if the box if full
        '''
        all_legal_moves = board.get_legal_move()
        if coord[0] >= 0:  # last move coord should be within the board
            box = [(i, j) for i in range(coord[0] - 1, coord[0] + 2) for j in
                   range(coord[1] - 1, coord[1] + 2)]  # 3x3 box
            legal_moves = []
            for c in box:
                if c in all_legal_moves:
                    legal_moves.append(c)
            if len(legal_moves) == 0:
                # all the box is full
                next_move = all_legal_moves[self.np_random.choice(len(all_legal_moves))]
                return board.coord_to_action(next_move[0], next_move[1])
            else:
                next_move = legal_moves[self.np_random.choice(len(legal_moves))]
                return board.coord_to_action(next_move[0], next_move[1])
        else:
            next_move = all_legal_moves[self.np_random.choice(len(all_legal_moves))]
            return board.coord_to_action(next_move[0], next_move[1])

    def connect_line(self, board, pattern):
        ''' Check if pattern exist in board_state, Fill one empty space to connect the dots to a line
            Return: Action ID
        '''
        empty_idx = []
        for id, val in enumerate(pattern):
            if val == 0:
                empty_idx.append(id)

        lines, starts = gomoku_util.check_pattern_index(board.board_state, pattern)
        if len(starts) >= 1:  # At least 1 found
            line_id = self.np_random.choice(len(lines))  # randomly choose one line
            line = lines[line_id]  # [(x1,y1), (x2,y2), ...]
            start_idx = starts[line_id]
            # Choose next_move among all the available the empty space in the pattern
            next_idx = start_idx + empty_idx[self.np_random.choice(len(empty_idx))]
            next_move = line[next_idx]
            return board.coord_to_action(next_move[0], next_move[1])
        else:
            return None

    def strike_policy(self, curr_state, prev_action):
        player_color = curr_state.color

        # List all the strike patterns
        pattern_four_a = [0] + [player_color.value] * 4  # [0,1,1,1,1]
        pattern_four_b = [player_color.value] * 4 + [0]  # [1,1,1,1,0]
        pattern_three_a = [0] + [player_color.value] * 3 + [0]  # [0,1,1,1,0]
        pattern_three_b = [player_color.value] * 2 + [0] + [player_color.value] * 1  # [1,1,0,1]
        pattern_three_c = [player_color.value] * 1 + [0] + [player_color.value] * 2  # [1,0,1,1]
        pattern_two = [0] + [player_color.value] * 2 + [0]  # [0,1,1,0]
        patterns = [pattern_four_a, pattern_four_b, pattern_three_a, pattern_three_b, pattern_three_c, pattern_two]

        for pattern in patterns:
            action = self.connect_line(curr_state.board, pattern)
            if action:  # Action is not none, pattern is found
                return action

        # no other strike pattern found, place around the box within previous move
        if prev_action:
            action = self.fill_box(curr_state.board, curr_state.action_to_coord(prev_action))
            return action

    def beginner_policy(self, curr_state: GomokuState, prev_action):
        b = curr_state.board

        # If defend needed
        action_defend = self.defend_policy(curr_state)
        if action_defend is not None:
            return action_defend

        # No Defend Strategy Met, Use Strike policy B to connect a line
        action_strike = self.strike_policy(curr_state, prev_action)
        if action_strike is not None:
            return action_strike

        # random choose legal actions
        legal_moves = b.get_legal_move()
        next_move = legal_moves[self.np_random.choice(len(legal_moves))]
        return b.coord_to_action(next_move[0], next_move[1])
