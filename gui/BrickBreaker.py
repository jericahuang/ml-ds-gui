import tkinter as tk
from models.ball import Ball
from models.brick import Brick
from models.paddle import Paddle

class Game(tk.Frame):
    """Game instance, a Tkinter.Frame subclass given to Tkinter.Tk() root."""
    def __init__(self, master):
        """Initialize parent Tkinter.Frame() and game environment."""
        # Init parent - Tkinter.Frame(Frame instance, Tk instance)
        tk.Frame.__init__(self, master)
        self.lives = 3
        self.width = 610
        self.height = 400
        # Tkinter.Canvas() will take up the Frame area, we can draw on it
        self.canvas = tk.Canvas(self, bg='#aaaaff', width=self.width,
                                height=self.height)

        # require .pack() by Tk to do actual placement
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self._paddle_y_start = 326
        self.paddle = Paddle(self.canvas, self.width / 2, self._paddle_y_start)
        # This dict will only hold canvas items that can collide with the ball
        self.items[self.paddle.item] = self.paddle

        # Create the brick layout
        for x in range(5, self.width - 5, 75):  # 75 px step
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        self.hud = None

        # set up game entities
        self.setup_game()

        # bind key events to movement methods
        self.canvas.focus_set()  # set focus to canvas to make sure we hear

        # We  use anonymouse function calls here as event handlers.
        # '_' is just placeholder to mean ignore the first parameter given
        # to us (a Tkinter event by bind()).
        # We do it this way because the bind() call requires a callback
        # argument, so we can't just put in self.paddle.move(10) because
        # it is not callable (it would evaluate .move(10) in place first
        # before calling the .bind() command!
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def setup_game(self):
        """Do all the necessary things to start the game."""
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, "Press Spacebar to start")
        # Bind only here otherwise would call start_game() each time pressed
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        """Create a Ball and store a reference in self.Paddle as well."""
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        # set the ball on top of player's paddle at start
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)  # store reference to it

    def add_brick(self, x, y, hits):
        """
        Create a Brick object.
        :param x: x-axis int location to create Brick.
        :param y: y-axis int location to create Brick.
        :param hits: int number of hits before Brick breaks.
        """
        brick = Brick(self.canvas, x, y, hits)
        # brick.item will be int that uniquely ID's that brick on canvas
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        """
        Draw text message on the canvas instance.
        :param x: int x-axix location to start text
        :param y: int y-axis location to start text
        :param text: text to draw at location
        :param size: default 40. Int size of font to use
        :rtype: int that references item uniquely on canvas
        """
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        """Displays number of lives left on canvas."""
        text = "Lives: {}".format(self.lives)
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        """Start main loop of game."""
        # unbind pressing space to call start_game()
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        """Main game loop."""
        self.check_collisions()
        # get how many Bricks left
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = None
            self.draw_text(300, 200, "You've won!")
        elif self.ball.get_position()[3] >= self.height:
            # bottom of screen, lose a life
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, "Game Over")
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()  # update position
            # use Tkinter .after() method to call game loop again
            # after(delay in ms, callback)
            self.after(50, self.game_loop)

    def check_collisions(self):
        """
        Process the ball's collisions.
        Since Ball.collide receives a list of game objects and
        canvas.find_overlapping() returns a list of colliding items
        with a given position, we use the dict of items to transform
        each canvas item into its corresponding game object.
        Game.items property will only contain canvas items that can
        collide with the ball. Therefore, we only need to pass the
        items from the Game.items dict.
        We filter the canvas items that cannot collide with the ball,
        like text objects, and then we retrieve each game objects by
        its key.
        """
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords) # list
        # list comprehension to filter down to only objects that
        # can collide with the ball
        collideables = [self.items[x] for x in items if x in self.items]
        self.ball.collide(collideables)


if __name__ == "__main__":
    # Create the root app and then create the Game instance (a tk.Frame())
    ROOT = tk.Tk()
    ROOT.title('Tkinter Breakout')
    # Frame() needs a Tk() instance as its parent, we pass our root app
    GAME = Game(ROOT)
    GAME.mainloop()