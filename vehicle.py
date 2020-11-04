
class Vehicle:
    def __init__(self, root, orientation, length, colour):
        self.root = root
        self.orientation = orientation
        self.length = length
        self.colour = colour

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def __len__(self):
        return self.length

    def co_ordinates(self):
        x_root, y_root = self.root
        dx = int(self.orientation == "lr")
        dy = int(self.orientation == "ud")
        return [(x_root + i * dx, y_root + i * dy) for i in range(self.length)]

    def create_shifted(self, shift):
        x_root, y_root = self.root
        x_root += shift * int(self.orientation == "lr")
        y_root += shift * int(self.orientation == "ud")
        return Vehicle((x_root, y_root), self.orientation, self.length, self.colour)

    def __hash__(self):
        return hash((self.root, self.orientation, self.length, self.colour))

    def __repr__(self):
        return f"({self.colour}, {self.root}, {self.orientation})"
