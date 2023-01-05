import data.board as db
import data.constants as dc


class Map:
    def __init__(
        self,
        boards: [],
        init_pos: (int, int),
    ):
        self.boards = boards
        self.height = len(boards)
        self.width = 0 if self.boards is None else len(boards[0])
        self.curr_x, self.curr_y = init_pos

        self.convert_map()

    def convert_map(self):
        for iy in range(self.height):
            for ix in range(self.width):
                if self.boards[iy][ix] is not None:
                    self.boards[iy][ix] = db.Board(self.boards[iy][ix])

    def draw(self, screen):
        self.boards[self.curr_y][self.curr_x].draw(screen)

    def move(self, delta_x: int, delta_y: int, x: int, y: int) -> (int, int):
        """
        Changes current screen by delta_x and delta_y amount if that amount
            is a defined screen.
        Returns new coordinates for the player on the new current board.
        """
        if not (0 <= self.curr_x+delta_x < self.width and
                0 <= self.curr_y+delta_y < self.height):
            # happens if try to move to screen that doesn't exist
            return (x, y)  # don't move

        board = self.boards[self.curr_y+delta_y][self.curr_x+delta_x]
        if board is not None:
            self.curr_x += delta_x
            self.curr_y += delta_y

            return (
                x - delta_x * (dc.TILES_WIDE-1),
                y - delta_y * (dc.TILES_TALL-1),
            )

    def update_animations(self):
        """
        Updates the animations for the tiles that have animations on the
        current board.
        """
        self.boards[self.curr_y][self.curr_x].update_animations()

    def get_tile(self, x: int, y: int):
        """
        Gets the specified tile on the current board.
        """
        return self.boards[self.curr_y][self.curr_x].get_tile(x, y)

    def is_talkable(self, x: int, y: int):
        """
        Returns if the specified tile on the current board is talkable
        """
        return self.boards[self.curr_y][self.curr_x].is_talkable(x, y)

    def is_walkable(self, x: int, y: int):
        """
        Returns if the specified tile on the current board is walkable
        """
        return self.boards[self.curr_y][self.curr_x].is_walkable(x, y)

    def amount_offscreen(self, x: int, y: int):
        """
        Returns the amount you are offscreen from the current board.
        """
        return self.boards[self.curr_y][self.curr_x].amount_offscreen(x, y)

    # TODO abstract above methods
    # def on_current_board(self, func, args: ()):
    #     return self.boards[self.curr_y][self.curr_x].func(*args)
