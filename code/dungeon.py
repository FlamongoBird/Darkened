
# Most of the generator itself I shamelessly stole from http://www.roguebasin.com/index.php/A_Simple_Dungeon_Generator_for_Python_2_or_3
# and then tweaked to fit my liking.

from __future__ import print_function
import random

CHARACTER_TILES = {'stone': '.',
                   'floor': ' ',
                   'wall': '#'}


# I'm going to be honest, just don't touch this class
# unless you really understand the code.
# I've got it working how it needs to and everytime I
# change a little thing it breaks. It's really finicky about
# certain stuff ig.


class Generator():
    def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5,
                 max_room_xy=10, rooms_overlap=False, random_connections=1,
                 random_spurs=3, tiles=CHARACTER_TILES):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = CHARACTER_TILES
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.tiles_level = []

    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0

        w = random.randint(self.min_room_xy, self.max_room_xy)
        h = random.randint(self.min_room_xy, self.max_room_xy)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))

        return [x, y, w, h]

    def room_overlapping(self, room, room_list):
        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]

        for current_room in room_list:

            # The rectangles don't overlap if
            # one rectangle's minimum in some dimension
            # is greater than the other's maximum in
            # that dimension.

            if (x < (current_room[0] + current_room[2]) and
                current_room[0] < (x + w) and
                y < (current_room[1] + current_room[3]) and
                    current_room[1] < (y + h)):

                return True

        return False

    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type == 'either' and set([0, 1]).intersection(
                    set([x1, x2, y1, y2])):

                join = 'bottom'
            elif join_type == 'either' and set([self.width - 1,
                                                self.width - 2]).intersection(set([x1, x2])) or set(
                    [self.height - 1, self.height - 2]).intersection(
                    set([y1, y2])):

                join = 'top'
            elif join_type == 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join == 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif join == 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])

        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1

        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1

        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # no overlap
        else:
            join = None
            if join_type == 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join == 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join == 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_level(self):

        # build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['stone'] * self.width)
        self.room_list = []
        self.corridor_list = []

        max_iters = self.max_rooms * 5

        for a in range(max_iters):
            tmp_room = self.gen_room()

            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]

                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)

            if len(self.room_list) >= self.max_rooms:
                break

        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        # do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # do the spurs
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(
                2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'

        # paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = 'floor'

            if len(corridor) == 3:
                x3, y3 = corridor[2]

                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'

        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'

                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'

                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'

                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'

                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'

                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'

                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'

                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'

    def gen_tiles_level(self):

        final = []

        for row_num, row in enumerate(self.level):
            tmp_tiles = []

            for col_num, col in enumerate(row):
                if col == 'stone':
                    tmp_tiles.append(self.tiles['stone'])
                if col == 'floor':
                    tmp_tiles.append(self.tiles['floor'])
                if col == 'wall':
                    tmp_tiles.append(self.tiles['wall'])

            final.append(tmp_tiles)

        return final


def build_dungeon():
    """Generates a Random Dungeon"""

    # These are the settings for the generator.
    # You can mess with them however you like, just
    # keep in mind that if you increase the width and
    # height of the dungeon too much the game will
    # run a little choppy.

    gen = Generator(
        width=100,
        height=100,
        max_rooms=30,
        min_room_xy=10,
        max_room_xy=10,
        rooms_overlap=False,
        random_connections=0,
        random_spurs=0
    )
    gen.gen_level()

    dungeon_raw = gen.gen_tiles_level()

    # This code below converts the # symbols
    # to | --- or a corner symbol depending
    # on their position relative to other wall
    # symbols. It might look a little complicated
    # but it really isn't once you understand it

    dungeon = []

    # We need to cycle through each character of
    # the dungeon to convert the walls from # to
    # the correct character

    for y in range(0, len(dungeon_raw)-1):
        row = dungeon_raw[y]
        new_row = []

        for x in range(0, len(row)-1):

            # If the character is not a wall character
            # we can skip over it.

            if dungeon_raw[y][x] != "#":
                new_row.append(dungeon_raw[y][x])

            # If it is a wall character, we check if
            # there are wall characters above, below, and
            # to the left and right of the character

            else:
                right = False
                left = False
                top = False
                bottom = False

                if dungeon_raw[y][x+1] == "#":
                    right = True
                if dungeon_raw[y][x-1] == "#":
                    left = True
                if dungeon_raw[y-1][x] == "#":
                    top = True
                if dungeon_raw[y+1][x] == "#":
                    bottom = True

                # The jumbled mess below is just a lot
                # of if statements to check what position
                # the wall character is in.

                HOR = "═"
                VER = "║"
                TRC = "╗"
                TLC = "╔"
                BRC = "╝"
                BLC = "╚"
                HLU = "╩"
                HLD = "╦"
                VLR = "╠"
                VLL = "╣"
                ALL = "╬"
                HLU = "╩"
                HLD = "╦"

                # Check if it is a horizontal wall character
                if right and left and not top and not bottom:
                    new_row.append(HOR)

                # check if it is a vertical wall character
                elif top and bottom and not left and not right:
                    new_row.append(VER)

                # bottom right corner
                elif left and top and not right and not bottom:
                    new_row.append(BRC)

                # bottom left corner
                elif not left and top and right and not bottom:
                    new_row.append(BLC)

                # top right corner
                elif left and not top and not right and bottom:
                    new_row.append(TRC)

                # top left corner
                elif not left and not top and right and bottom:
                    new_row.append(TLC)

                # vertical wall wall ending up
                elif top and not left and not right and not bottom:
                    new_row.append(HLU)

                # vertical wall ending down
                elif bottom and not top and not left and not right:
                    new_row.append(HLD)

                # horizontal wall ending right
                elif left and not top and not bottom and not right:
                    new_row.append(VLL)

                # horizontal wall ending left
                elif right and not top and not bottom and not left:
                    new_row.append(VLR)

                # all join
                elif left and right and top and bottom:
                    new_row.append(ALL)

                # special case ending vertical wall
                elif not top and not bottom and not right and not left:
                    new_row.append(VER)

                # right vertical join
                # elif right and top and bottom and not left:
                #   new_row.append(VLR)

                # left vertical join
                # elif left and top and bottom and not right:
                #   new_row.append(VLL)

                # up horizontal wall join
                # elif top and left and right and not bottom:
                #   new_row.append(HLU)

                # down horizontal wall join
                # elif bottom and not top and left and right:
                #   new_row.append(HLD)

                # single width horizontal wall
                elif right and left:
                    new_row.append(HOR)

                # single width vertical wall
                elif top and bottom:
                    new_row.append(VER)

                # default value
                else:
                    new_row.append("#")
        dungeon.append(new_row)

    # This finds a good spawn position for the player
    # it is not very efficient and if you make the
    # dungeon too big (think 1000x1000) it will take
    # a noticable pause to find a good spawn

    spawnY = 0
    spawnX = 0

    while True:
        spawnY = random.randint(0, len(dungeon)-1)
        if " " in dungeon[spawnY]:
            while True:
                spawnX = random.randint(0, len(dungeon[spawnY])-1)
                if dungeon[spawnY][spawnX] == " ":
                    return [dungeon, (spawnX, spawnY)]
