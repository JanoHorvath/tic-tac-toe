

class MinMax:
    """ Locates empty spots, calculates their values and picks the one with the highest value. """

    def __init__(self, symbol):
        self.free_spots = {}
        if symbol:
            self.symbol = symbol
        else:
            self.symbol = 'O'

    def move(self, board, check_field):
        self.check = check_field

        self.free_spots = {}
        self.find_empty_spots(board)

        self.assign_values()

        return self.find_max_value()

    def render(self, canvas):
        pass
        # for field in self.free_spots:
        #     value = self.free_spots[field]
        #     color = 'grey'
        #     canvas.create_text(field[0]*10+250, field[1]*10+250, text=value, fill=color)

    def find_empty_spots(self, board):
        for field in board:
            if field == 'last_move':
                pass
            else:
                for i in range(-1, 2):
                    for j in range(-1,  2):

                        x = field[0]+i
                        y = field[1]+j

                        if self.check(x, y) is None:
                            self.free_spots[(x, y)] = 0  # by default, value of the field is 0

    def assign_values(self):
        def check_horizontal(x, y):
            sequence = ""

            for i in range(-4, 5):  # horizontal
                if i is 0:
                    value = self.symbol
                else:
                    value = self.check(x + i, y)

                if value is None:
                    sequence += " "
                elif value == self.symbol:
                    sequence += "1"
                else:
                    sequence += "0"

            return compute_value(sequence)

        def check_vertical(x, y):  # vertical
            sequence = ""

            for i in range(-4, 5):
                if i is 0:
                    value = self.symbol
                else:
                    value = self.check(x, y + i)

                if value is None:
                    sequence += " "
                elif value == self.symbol:
                    sequence += "1"
                else:
                    sequence += "0"

            return compute_value(sequence)

        def check_diagonalU(x, y):  # diagonal /
            sequence = ""

            for i in range(-4, 5):
                if i is 0:
                    value = self.symbol
                else:
                    value = self.check(x + i, y + i)

                if value is None:
                    sequence += " "
                elif value == self.symbol:
                    sequence += "1"
                else:
                    sequence += "0"

            return compute_value(sequence)

        def check_diagonalD(x, y):  # diagonal \
            sequence = ""

            for i in range(-4, 5):
                if i is 0:
                    value = self.symbol
                else:
                    value = self.check(x - i, y + i)

                if value is None:
                    sequence += " "
                elif value == self.symbol:
                    sequence += "1"
                else:
                    sequence += "0"

            return compute_value(sequence)

        def compute_value(sequence):

            if '11111' in sequence:
                # five in a row = win
                return 100

            elif '1111' in sequence:
                if '011110' in sequence:
                    return 0
                elif '01111' in sequence:
                    return 50
                elif '11110' in sequence:
                    return 50
                else:
                    return 90

            # where necessary, slices the string so that only the subsequence with the x,y in question is matched
            #  e.g 111010110 will therefore not match 111

            elif '111' in sequence[2: -2]:
                if '01110' in sequence:
                    return 0
                elif '0111' in sequence[1: -1]:
                    return 10
                elif '1110' in sequence[1: -1]:
                    return 10
                else:
                    return 40

            elif '11' in sequence[3: -3]:
                if '0110' in sequence[1: -1]:
                    return 0
                elif '011' in sequence[2: -2]:
                    return 5
                elif '110' in sequence[2: -2]:
                    return 5
                else:
                    return 10

            else:
                return 0

        for field in self.free_spots:
            x = field[0]
            y = field[1]

            value_h = check_horizontal(x, y)
            value_v = check_vertical(x, y)
            value_u = check_diagonalU(x, y)
            value_d = check_diagonalD(x, y)

            value = value_h + value_v + value_u + value_d

            self.free_spots[field] = value

    def find_max_value(self):
        max_value = -1
        for spot in self.free_spots:
            value = self.free_spots[spot]
            if value > max_value:
                max_coordinates = spot
                max_value = value
        print "Found the biggest value {0} at: {1}".format(self.free_spots[max_coordinates], max_coordinates)
        return max_coordinates

