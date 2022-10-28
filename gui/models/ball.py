from .gameobject import GameObject
from .brick import Brick

class Ball(GameObject):
    """
    Ball that bounces off solid objects on screen. Stores information
    about speed, direction, and radius of the ball.
    """
    def __init__(self, canvas, x, y):
        """Creates ball shape using canvas.create_oval()."""
        self.radius = 10
        self.direction = [1, -1]  # right and up
        self.speed = 5

        # self.item value will be an integer, which is ref num returned by method
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        # now call parent constructor with our required item
        GameObject.__init__(self, canvas, item)

    def update(self):
        """Logic for changing Ball direction based on collisions."""

        # ---------------------------------------------------------
        # BOUNDS COLLISIONS
        # ---------------------------------------------------------
        ball_coords = self.get_position()
        width = self.canvas.winfo_width()

        if ball_coords[0] <= 0 or ball_coords[2] >= width:
            self.direction[0] *= -1  # reverse x vector
        if ball_coords[1] <= 0:
            self.direction[1] *= -1  # reverse y vector
        x = self.direction[0] * self.speed  # scale by Ball's speed
        y = self.direction[1] * self.speed
        self.move(x, y)  # inherited method


    def collide(self, game_objects):
        """
        Handles the outcome of collision with one or more objects.
        :param game_objects: list of colliding objects.
        Code Explanation:
        # First get center x of Ball
        # x0, y0 is top left corner, x1, y1 is bottomright corner
        ball_coords = self.get_position() # -> [x0, y0, x1, y1]
        # we add the start and end x positions and * 0.5 to get midx
        ball_center_x = (ball_coords[0] + coords[2]) * 0.5  # center
        brick_coords = brick.get_position() # -> [x0, y0, x1, y1]
        # if ball_center is greater than lower right of brick, meaning
        # ball center is to right of right side of brick during collision
        if ball_center_x > brick_coords[2]:
            self.direction[0] = 1  # ball x to right
        # check is ball center is left of the left side of brick
        # during collision
        elif ball_center_x < brick_coords[0]:
            self.direction[0] = -1  # ball x to the left
        # else case means ball_center is between left and right x of brick
        # which means a top/bottom hit, so we just reverse y-vector of ball
        else:
            self.direction[1] *= -1
        Above is valid for when ball hits the paddle or a single brick. But
        if we hit two bricks at the same time things get hairy. We simplify
        by assuming multiple brick collisions can only happen from above or
        below. That means that we change the y-axis direction of the ball
        without calculating the position of the colliding bricks.
        So what we do is guard all of the above by checking how many
        colliding objects we have, in the argument game_objects, and if it
        is two or more we can just flip the y-axis on the ball and be done.
        If not, we have to do more investigation and do all of the above.
        """
        ball_coords = self.get_position()
        ball_center_x = (ball_coords[0] + ball_coords[2]) * 0.5  # same as / 2

        if len(game_objects) > 1:  # 2+ collisions, just flip y-axis and done
            self.direction[1] *= -1
        elif len(game_objects) == 1:  # investigate more if just one collision
            game_object = game_objects[0]
            coords = game_object.get_position()
            if ball_center_x > coords[2]:
                self.direction[0] = 1
            elif ball_center_x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        # Do below regardless of how many collisions came in
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()  # decrement hit counter, etc. in Brick class
