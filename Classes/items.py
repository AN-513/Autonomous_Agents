
class Item:
    def __init__(self, name:str, coordinates:tuple, points_for_collecting:float = 0):
        self.name = name
        self.blocksPassage = False
        self.isCollectible = False
        self.coordinates = coordinates
        self.pointsForCollecting = points_for_collecting

        if name == "Wall":
            self.blocksPassage = True

        # TODO: ADD MORE ITEMS


    def is_passageBlocked(self):
        return self.blocksPassage

    def is_Collectible(self):
        return not(self.blocksPassage) and  self.isCollectible

    def get_points_for_collecting(self):
        if self.is_Collectible():
            return self.pointsForCollecting
        else:
            return 0

    def get_coords(self):
        return self.coordinates