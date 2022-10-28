from .gameobject import GameObject

class Paddle(GameObject):
    """
    The player's paddle. A set_ball method stores a reference to the ball,
    which can be moved with the ball before the game starts.
    """
    def __init__(self, canvas, x, y):
        """
        Create a Paddle instance using canvas.create_rectangle().
        :param canvas: a Tkinter.Canvas() instance
        :param x: the horizontal axis location (int)
        :param y: the vertical axis location (int)
        """
        self.width = 80
        self.height = 10
        self.ball = None

        # item will be int ref num returned by create_rectangle()
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='blue')
        # call parent class now with our require item argument
        GameObject.__init__(self, canvas, item)

    def set_ball(self, ball):
        """Store a reference to a ball on this instance."""
        self.ball = ball

    def move(self, offset):
        """
        Move the Paddle on the Tkinter.Canvas within bounds.
        Contained here is the pre-move logic. The actual move is
        done by calling our parent GameObject.move() method.
        :param offset: integer. amount to move in pixels left or right.
        """
        coords = self.get_position()  # e.g., [int, int, int, int]
        width = self.canvas.winfo_width()
        # bounds check
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            GameObject.move(self, offset, 0)  # 0 is y-axis
            # Below happens when the game has not been started; move the ball
            if self.ball is not None:
                self.ball.move(offset, 0)  # Call Ball inherited move() method


    def hit(self):
        """Decrement hits counter. Delete instance if at 0."""
        self.hits -= 1
        if self.hits == 0:
            self.delete()  # inherited from GameObject()
        else:  # repaint next color to indicate Brick was hit
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])