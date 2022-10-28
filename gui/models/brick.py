from .gameobject import GameObject

class Brick(GameObject):
    """Ball objects destroy these canvas rectangle built objects when hit."""
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        """
        Initialize a Brick object.
        :param canvas: a Tkinter.Canvas() instance
        :param x: Where to place it on horizontal x axis
        :param y: Where to place it on the vertical x axis
        :param hits: number of hits Brick can take before 'breaking'
        """
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]  # hits arg must be int 1,2, or 3

        # tags keyword is so we can reference it easy on canvas
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        # now call parent class with our require item
        GameObject.__init__(self, canvas, item)

    def hit(self):
        """Decrement hits counter. Delete instance if at 0."""
        self.hits -= 1
        if self.hits == 0:
            self.delete()  # inherited from GameObject()
        else:  # repaint next color to indicate Brick was hit
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])