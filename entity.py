class Entity:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        """
            Returns entity's name.
        :return: The name string.
        """
        return self.name

    def get_description(self):
        """
            Returns the object's description.
        :return: The description string.
        """
        return self.description