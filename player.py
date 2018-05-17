class Player:

    def __init__(self, name, levels, score):
        self.name = name
        self.levels = levels
        self.score = score

    def __str__(self):
        return "{0}/{1}/{2}".format(self.name, self.levels, self.score)
