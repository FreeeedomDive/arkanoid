import block


class Map:

    def __init__(self, filename):
        self.map_in_text = open(filename)
        self.map = []
        self.blocks = []
        self.create_map_from_file()
        self.map_in_text.close()

    def create_map_from_file(self):
        self.map = []
        for line in self.map_in_text:
            self.map.append(line)
        self.blocks = []
        i = j = 0
        for row in self.map:
            for col in row:
                if col.isdigit():
                    b = block.Block(i * 20 + 10, j * 20 + 10, int(col))
                    self.blocks.append(b)
                i += 1
            i = 0
            j += 1
