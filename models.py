# models.py
# YOUR NAME(S) AND NETID(S) HERE: Zachary Bamberger (zeb3) and Ingrid Libman (iml29)
# DATE COMPLETED HERE: 12/11/2015
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """Returns: the x coordinate of the paddle.
        """
        
        return self.x
    
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self):
        """Initializer: Creates a new Paddle object.
        
        The Paddle inherits attributes from the GRectangle initializer. We will call the
        GRectangle initializer to construct an object of this class. Note that GRectangle
        is a subclass of GObject."""
        
        GRectangle.__init__(self, x = GAME_WIDTH / 2, bottom = PADDLE_OFFSET,
                            height = PADDLE_HEIGHT, width = PADDLE_WIDTH,
                            linecolor = colormodel.BLACK, fillcolor = colormodel.BLACK)
    
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def movePaddle(self,xcor):
        """Moves the paddle to the specified x coordinate (xcor)
        
        Parameter xcor: The x coordinate to which we will move the paddle
        Precondition: xcor must be a number between PADDLE_WIDTH / 2 and
        GAME_WIDTH - PADDLE_WIDTH / 2"""
        assert isinstance(xcor, int) or isinstance(xcor, float), 'xcor is not a number'
        
        self.x = xcor
        
        
    def collides(self,ball):
        """Returns: True if the ball collides with the paddle. False otherwise.
        
        Parameter ball: The ball to check
        Precondition: ball is an instance of class Ball"""
        assert isinstance(ball, Ball), 'ball is not an instance of Ball.'
        
        if ball.getVY() < 0:
            xvals = [ball.x + BALL_DIAMETER / 2, ball.x + BALL_DIAMETER / 2,
                    ball.x - BALL_DIAMETER / 2, ball.x - BALL_DIAMETER / 2]
            yvals = [ball.y + BALL_DIAMETER / 2, ball.y - BALL_DIAMETER / 2,
                    ball.y + BALL_DIAMETER / 2, ball.y - BALL_DIAMETER / 2]
            for x in range(4):
                xcor = xvals[x]
                ycor = yvals[x]
                if self.contains(xcor,ycor):
                    return True
        return False
    
    
    
class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # INITIALIZER TO CREATE A BRICK
    def __init__(self, xcor, ycor, color):
        """"Initializer: Creates a new Brick object.
        
        Parameter xcor: The x coordinate at which the brick will first appear
        Precondition: xcor is a number between 0 and GAME_WIDTH - BRICK_WIDTH / 2
        
        Parameter ycor: The y coordinate at which the brick will first appear
        Precondition: ycor is a number between 0 and GAME_HEIGHT - BRICK_Y_OFFSET -
        BRICK_HEIGHT / 2
        
        Parameter color: The color of the brick
        Precondition: color is an item within the list colors in Play.py. Color a colormodel
        object. 
        
        """
        
        GRectangle.__init__(self, x = xcor,y = ycor, width = BRICK_WIDTH,
                                height = BRICK_HEIGHT, linecolor = color,
                                fillcolor = color)
    
    
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball""" #Specification copied from assignment page
        assert isinstance(ball, Ball), 'ball is not an instance of Ball.'
        
        xvals = [ball.x + BALL_DIAMETER / 2, ball.x + BALL_DIAMETER / 2,
                ball.x - BALL_DIAMETER / 2, ball.x - BALL_DIAMETER / 2]
        yvals = [ball.y + BALL_DIAMETER / 2, ball.y - BALL_DIAMETER / 2,
                ball.y + BALL_DIAMETER / 2, ball.y - BALL_DIAMETER / 2]
        for x in range(4):
            xcor = xvals[x]
            ycor = yvals[x]
            if self.contains(xcor,ycor):
                return True
        return False
        
            

class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _livelost [Boolean]: True if the ball was lost in the previous frame. False
        otherwise.
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """Returns: the x coordinate of the ball.
        """
        return self.x
    
    
    def getY(self):
        """Returns: the y coordinate of the ball.
        """
        return self.y
    
    
    def getVX(self):
        """Returns: the velocity of the ball in the horizontal direction (self._vx).
        """
        return self._vx
    
    
    def getVY(self):
        """Returns: the velocity of the ball in the vertical direction (self._vy)
        """
        return self._vy
    
    
    def setVX(self, val):
        """Sets the velocity of the ball in the horizontal direction (self._vx) to val.
        
        Parameter val: the values to which we will set the velocity of the ball in
        the horizontal direction (self._vx)
        Precondition: val is a number"""
        assert isinstance(val, int) or isinstance(val,float), 'val is not a number'
        
        self._vx = val
        
    
    def setVY(self, val):
        """Sets the velocity of the ball in the vertical direction (self._vy) to val.
        
        Parameter val: the values to which we will set the velocity of the ball in
        the vertical direction (self._vy)
        Precondition: val is a number"""
        assert isinstance(val, int) or isinstance(val,float), 'val is not a number'
        
        self._vy = val
 
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """"Initializer: Creates a new Ball object.
        
        The Ball object will be constructed using the GEllipse initializer (which is a
        subclass of GObject). In addition, this initializer determines the ball's
        velocities in the vertical and horizontal directions. It also sets object
        attribute _livelost to False."""
        
        GEllipse.__init__(self, x=GAME_WIDTH / 2,y= GAME_HEIGHT / 2,
                          width=BALL_DIAMETER, height=BALL_DIAMETER,
                          fillcolor=colormodel.BLACK)
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._livelost = False
    
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self, xcor, ycor):
        """This helper function will move the ball to the desired x (xcor) and y
        (ycor) positions on the screen.
        
        Parameter xcor: the value to which we will set the x coordinate of the center
        of the ball.
        Precondition: xcor is a number between BALL_DIAMETER / 2 and GAME_WIDTH -
        BALL_DIAMETER / 2
        
        Parameter ycor: the value to which we will set the y coordinate of the center of
        the ball.
        Precondition: ycor is a number less than GAME_HEIGHT - BALL_DIAMETER / 2
        """
        assert isinstance(xcor, int) or isinstance(xcor, float), 'xcor is not a number'
        assert isinstance(ycor, int) or isinstance(ycor, float), 'ycor is not a number'
        
        self.x = xcor
        self.y = ycor
    
     
    def is_Collision(self, xcor, ycor):
        """This helper function determines whether or not that ball has collided with the
        sides of the screen.
        
        If the ball hits the top side of the screen, the ball will reverese velocities in
        the y direction (self._vy).
        If the ball hits either the left or right sides of the screen, the ball will
        reverse velocities in the x direction (self._vx)
        If the ball hits the bottom of the screen, then self._state in breakout becomes
        STATE_PAUSED, a message will appear on the screen
        to display how many tries (self._tries in Play) the players has left. The player
        will have to press another key once the game is paused
        in order to unpause it.
        
        Parameter xcor: the value to which we will set the x coordinate of the center of
        the ball.
        Precondition: xcor is a number
        
        Parameter ycor: the value to which we will set the y coordinate of the center of
        the ball.
        Precondition: ycor is a number.
        """
        assert isinstance(xcor, int) or isinstance(xcor, float), 'xcor is not a number'
        assert isinstance(ycor, int) or isinstance(ycor, float), 'ycor is not a number'
        assert isinstance(self._vx, int) or isinstance(self._vx, float), '_vx is not a number'
        assert isinstance(self._vy, int) or isinstance(self._vy, float), '_vy is not a number'
        
        #Sides of window
        if xcor - BALL_DIAMETER / 2 <= 0 or xcor + BALL_DIAMETER / 2 >= GAME_WIDTH:
            self._vx = -self._vx
        #Upper side of window
        if ycor + BALL_DIAMETER / 2 >= GAME_HEIGHT:
            self._vy = -self._vy
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def waslifelost(self, ycor):
        """Returns: True if the ball touched the bottom side of the game window.
        False otherwise.
        
        Parameter ycor: the y value of the ball.
        Precondition: ycor is a number"""
        assert isinstance(self._livelost, bool), '_livelost is neither True nor False.'
        assert isinstance(ycor, int) or isinstance(ycor, float), 'ycor is not a number'
        
        if ycor - BALL_DIAMETER / 2 <= 0:
            #print 'Life was lost'
            return True
        return False
