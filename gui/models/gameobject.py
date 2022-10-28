class GameObject():
    """Base class for game entities on a Tkinter.Canvas()."""
    def __init__(self, canvas, item):
        """
        Stores the canvas and item parameters as properties of this instance
        for reference.
        :param canvas: a Tkinter.Canvas instance
        :param item: an entity/shape, e.g. a Canvas.create_oval reference
        """
        self.canvas = canvas
        self.item = item

    def get_position(self):
        """
        Returns bounding coordinates of instance's item property.
        :rtype: list of integers
        """
        return self.canvas.coords(self.item)

    def move(self, x, y):
        """
        Move the instance's item property by x horizontally, and y vertically.
        :param x: distance to move self.item horizontally in pixels
        :param y: distance to move self.item vertically in pixels
        """
        self.canvas.move(self.item, x, y)

    def delete(self):
        """Remove instance's self.item."""
        self.canvas.delete(self.item)