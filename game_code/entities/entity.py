class Entity:
    """
    An entity is any object that is in the game world where they have a name and a description.
    """
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

