# play.py
# YOUR NAME(S) AND NETID(S) HERE: Zachary Bamberger (zeb3) and Ingrid Libman (iml29)
# DATE COMPLETED HERE: 12/11/2015
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left
        _paddlehits [int >= 0] : the number of times the ball hit the paddle
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTries(self):
        """Returns: the number of tries remaining."""
        
        return self._tries
    
    
    def setTries(self, val):
        """Sets the number of tries to val.
        
        Parameter val: The amount of tries the player will have.  
        Precondition: val is an int between 0 and 3 (inclusive)
        """
        assert isinstance(val, int), 'val is not an int'
        assert val >=0 or val <= 3, 'val is not between 0 and 3 (inclusive)'
        
        self._tries = val
        
    
    def getBrickScore(self):
        """Returns: A string which represents the number of bricks the player has
        destroyed."""
        
        brickscore = (BRICKS_IN_ROW * BRICK_ROWS) - len(self._bricks)
        return brickscore
    
    
    
    def setBall(self, val):
        """Sets the ball object to val.
        
        Parameter val: The new ball object in the game.
        Precondition: val is either None or an instance of Ball."""
        assert isinstance(val, Ball) or val is None, 'val is neither None nor a Ball object'
        
        self._ball = val
    
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Creates an empty list of breaks, a paddle object of type Paddle (subclass of
        GRectangle), and a ball of type None (since the ball will be created in
        serveBall(self)).
        
        The color of the bricks will draw upon the list of colors. We will use a nested
        for loop to determine the x and y coordinates of each brick."""
        
        self._bricks = []
        self._paddle = Paddle()
        self._ball = None
        self._tries = 3
        self._paddlehits = 0
        colors = [colormodel.RED, colormodel.ORANGE, colormodel.YELLOW,
                  colormodel.GREEN, colormodel.CYAN]
        for y in range(BRICK_ROWS):
            for x in range(BRICKS_IN_ROW):
                xcor = BRICK_SEP_H / 2 + BRICK_WIDTH / 2 + (x * BRICK_WIDTH + x * BRICK_SEP_H)
                ycor = GAME_HEIGHT - BRICK_Y_OFFSET - BRICK_HEIGHT / 2 - (y * BRICK_HEIGHT + y * BRICK_SEP_V)
                color = colors[(y / 2) % 5]
                self._bricks.append(Brick(xcor,ycor,color))
        
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def _updatePaddle(self, inputt):
        """This helper function assists in determining the new position of the paddle.
        
        We will move the paddle right if the right key is down and the right side of the
        paddle is not touching the right edge of the screen. We will move the paddle left
        if the left key is down and the left side of the paddle is not touching the left
        edge of the screen.
        
        Parameter inputt: the input as passed on from the Breakout class. It is an
        immutable instance of GInput and is inherited from GameApp. This is in fact the
        user input, and is used to control the paddle's position.
        
        Precondition: inputt is an instance of GInput."""
        assert isinstance(inputt, GInput), 'inputt is not an instance of GInput'
        
        xcor = self._paddle.getX()
        if inputt.is_key_down('left'):
            if xcor > PADDLE_WIDTH / 2:
                xcor = xcor - 5
                self._paddle.movePaddle(xcor)
        if inputt.is_key_down('right'):
            if xcor < GAME_WIDTH - PADDLE_WIDTH / 2:
                xcor = xcor + 5
                self._paddle.movePaddle(xcor)
    
    
    def serveBall(self):
        """This helper function will serve the ball at the beginning of STATE_ACTIVE
        after changing from STATE_COUNTDOWN.
        
        first, we will check that there is no ball, and if that is the case, we will
        create one which will go in a random direction and speed. The if statement is
        present to ensure that a new ball is not created in the center of the screen
        after every frame"""
        
        if self._ball == None:
            self._ball = Ball()
    
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def _drawme(self, view):
        """This function's purpose is to draw the bricks, paddle, and ball. The ball
        will only be drawn if it is not None. As in, the ball will only be drawn after
        STATE_COUNTDOWN where self._ball is no longer False.
        
        Parameter view: The window in which the bricks, paddle, and ball will be drawn
        in.
        Precondition: view is an instance of GView."""
        assert isinstance(view, GView), 'view is not an instance of GView'
        
        for brick in self._bricks:
            #print brick
            brick.draw(view)
        self._paddle.draw(view)
        if self._ball != None:
            self._ball.draw(view)
    
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def updateBall(self):
        """The purpose of this function is to properly update the position of the ball
        via its position and checking for collision.
        
        The position of the ball in the x axis is the current x position + velocity in
        the x direction per frame, as this function is called once per frame. The same
        method is used to determine the new y position.
        
        Additionally, this function checks whether the ball collided with the paddle and
        bricks (using the helper function, collides). If a collosion occures, the ball's
        y velocity changes sign. A collision only occures between the ball and the paddle
        if the ball's velocity is negative when hitting the paddle. The ball's y velocity
        can be either positive or negative when hitting bricks."""
        
        if self._paddle.collides(self._ball):
            self._playpaddlesound()
            self._paddlehits += 1
            self._ball.setVY(- self._ball.getVY())
            if self._paddlehits == 5:
                self._paddlehits = 0
                self._ball.setVX(1.5 * self._ball.getVX())             
        for brick in self._bricks:
            if brick.collides(self._ball):
                self._playbricksound()
                self._ball.setVY(- self._ball.getVY())
                self._bricks.remove(brick)
                if self.iswon():
                    return 'wongame'
        xspeed = self._ball.getVX()
        yspeed = self._ball.getVY()
        xcor = self._ball.getX() + xspeed
        ycor = self._ball.getY() + yspeed
        self._ball.moveBall(xcor, ycor)
        self._ball.is_Collision(xcor, ycor)
        if self._ball.waslifelost(ycor):
            self._tries = self._tries - 1
            if self._tries >= 1:
                return 'anothertry'
            else:
                return 'lostgame'
            
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def iswon(self):
        """Returns: True if there are no bricks remaining in the game (Player has
        won the game.) False otherwise."""
        
        if self._bricks == []:
            return True
        return False
    
    
    def _playpaddlesound(self):
        """Plays paddle sound when ball hits the paddle."""
        paddleSound = Sound('bounce.wav')
        paddleSound.play()
    
    def _playbricksound(self):
        """Plays a random sound from a list of brick sounds when ball hits a brick."""
        bricksounds = ['cup1.wav', 'plate1.wav', 'plate2.wav', 'saucer1.wav', 'saucer2.wav']
        brickSound = Sound(random.choice(bricksounds))
        brickSound.play()
        
    

    



