# breakout.py
# YOUR NAME(S) AND NETID(S) HERE: Zachary Bamberger (zeb3) and Ingrid Libman (iml29)
# DATE COMPLETED HERE: 12/11/2015
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY:
    
        _time [Hidden attribute used in Countdown] is a number >= 0:
                used to determine the amount of time elapsed in STATE_COUNTDOWN
        
        _is_paused [hidden attribute used in _pause_if_escaped(self, validity = False),
                will be a Boolean]: used to determine whether or not the screen should
                be paused. Initially False, true if escape is pressed. Becomes False
                again if any key is pressed.
                
        _stats [hidden attribute] [Glabel or None]:
                displays the player's score in the game.
                
        _keysinlastframe [hidden attribute] an int >= 0.
                        used to determine how many keys were pressed
                        in last frame.
    """
    

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME 
        
        #create opening text:
        initial_text = 'Press any Key to play!!!'
        initial_font_size = 36
        initial_font_name = 'TimesBoldItalic.ttf'
        initial_bold = True
        initial_halign = 'center'
        initial_valign = 'middle'
        
        self._time = 0.0
        self._is_paused = False
        self._keysinlastframe = 0
        
        self._state = STATE_INACTIVE
        self._game = None
        self._mssg = GLabel(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,text = initial_text,
                                font_size = initial_font_size,
                                font_name = initial_font_name,
                                bold = initial_bold, halign = initial_halign,
                                valign = initial_valign)
        self._stats = None
                                 
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_INT_PAUSED: The application switches to this state if the state was
        STATE_ACTIVE in the preview frame, and the player pressed 'escape' to pause
        the game intentionally. 
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        STATE_COMPLETE: The application switches to this state if the state was STATE_ACTIVE
        in the previous frame, the ball was lost, and there are no lives remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        
        #from STATE_INACTIVE to STATE_NEWGAME:
        if self._state == STATE_INACTIVE and self._from_inactive_to_newgame():
            self._state = STATE_NEWGAME
            self._game = Play()
            self._updateScoreMssg()
        
        #from STATE_NEWGAME to STATE_COUNTDOWN:
        elif self._state == STATE_NEWGAME:
            self._in_STATE_NEWGAME()
            
        #from STATE_COUNTDOWN to STATE_ACTIVE    
        elif self._state == STATE_COUNTDOWN:
            self._Countdown(self._time)

        #from STATE_ACTIVE
        elif self._state == STATE_ACTIVE and self._is_paused == False:
            self._in_STATE_ACTIVE()

        elif self._state == STATE_ACTIVE and self._is_paused == True:
            self._state = STATE_INT_PAUSED
            self._is_paused = False
            
        elif self._state == STATE_INT_PAUSED:
            if self.input.is_key_down('spacebar'):
                self._state = STATE_ACTIVE
                
        elif self._state == STATE_PAUSED and self._from_inactive_to_newgame():
            self._state = STATE_COUNTDOWN
            self._game.setBall(None)
            
        elif self._state == STATE_COMPLETE and self._from_inactive_to_newgame():
            self._state = STATE_NEWGAME
                
                
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        assert isinstance(self.view, GView) or self.view == None, 'view is not an instance of GView or None'
        
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE: 
            self._mssg.draw(self.view)
        elif self._state == STATE_NEWGAME:
            self._game._drawme(self.view)
        elif self._state == STATE_COUNTDOWN:
            self._mssg.draw(self.view)
            self._stats.draw(self.view)
            self._game._drawme(self.view)
            self._game._updatePaddle(self.input)
        elif self._state == STATE_ACTIVE:
            self._stats.draw(self.view)
            self._game._drawme(self.view)
            self._game._updatePaddle(self.input)
        elif self._state == STATE_INT_PAUSED:
            self._mssg.draw(self.view)
            self._stats.draw(self.view)
            self._game._drawme(self.view)
        elif self._state == STATE_PAUSED:
            self._mssg.draw(self.view)
            self._stats.draw(self.view)
            self._game._drawme(self.view)
        elif self._state == STATE_COMPLETE:
            self._mssg.draw(self.view)
            self._stats.draw(self.view)
            self._game._drawme(self.view)
            
    
    
    # HELPER METHODS FOR THE STATES GO HERE
    def _from_inactive_to_newgame(self):
        """Returns: True if a key has been pressed and no key was pressed in previous frame, False otherwise.
        
        implemented on the basis of Walker White's "State" module, written on Movember 17, 2015. Worked around notion
        of checking the number of frames in both the current and previous screen. Implemented the idea that we should
        only consider instances in which a new key is pressed in the current frame, but none were in the previous one.
        """
        
        
        #change occurs if at least one key is being pressed and the amount of keys pressed in the last frame was 0
        assert isinstance(self._keysinlastframe, int), '_keysinlastframe is not an int'
        assert self._keysinlastframe >= 0, '_keysinlastframe is not >= 0.'
        
        new_keys = self.input.key_count
        #print 'old_keys is ' + str(old_keys)
        #print 'new_keys is ' + str(new_keys)
        validity = new_keys > 0 and self._keysinlastframe == 0
        self._keysinlastframe = new_keys
        return validity
    
                
    def _Countdown(self, time):
        """During STATE_COUNTDOWN, Counts down from 3 to 0 on the screen and then switches to STATE_ACTIVE.
        
        There are 62.5 frames per second assuming update goes through one fram every 16 miliseconds. Therefore,
        every second we will change the text that is to be displayed on the screen. Once three seconds have gone by,
        we will change the state to active
        
        Parameter time: The amount of time which has passed since self._State has become STATE_COUNTDOWN
        Precondition: time is a number >= 0"""
        assert isinstance(time, int) or isinstance(time, float), 'time is not a valid number'
        assert time >=0, 'time is not >= 0'
        
        #print 'state is countdown'
        if time < 62.5:
            text = '3'
            #print 'text = 3'
            #print 'time = ' + str(time)
        elif time >= 62.5 and time < 125.0:
            text = '2'
            #print 'text = 2'
            #print 'time = ' + str(time)
        elif time >= 125.0 and time < 187.5:
            text = '1'
            #print 'text = 1'
            #print 'time = ' + str(time)
        else:
           self._state = STATE_ACTIVE
           text = 'LAUNCH!!!'
        self._mssg.text = text
        self._mssg.font_size = 36
        
        self._time += 1.0
            
    def _int_pause(self): 
        """If the espace key is pressed, self._state becomes STATE_INT_PAUSED. Go back to STATE_ACTIVE if any key is pressed afterwards.
        One can also reach STATE_PAUSED by losing the losing a "life" (what occurs when the ball hits the bottom of the screen).
        If this is the case, we will display a message on the screen displaying the amount of lives remaining and/or whether the players has
        won or lost the game. If the player has tries left, the game will serve the ball and go to STATE_ACTIVE upon the player hitting the
        next key"""
        
        if self.input.is_key_down('escape') and self._is_paused == False:
            self._is_paused = True
            self._mssg.text = 'Game is paused. Press spacebar to unpause.'
            self._mssg.font_size = 24
            
            
    def _tryagain(self):
        """Changes the state to STATE_PAUSED and displays how many lives remain.
        To exit this state, the user will have to press the spacebar."""
        self._mssg.text = 'You lost a life. Balls Remaining: '+ str(self._game.getTries())
        self._mssg.font_size = 20
        self._time = 0
        self._state = STATE_PAUSED
        
    
    def _game_lost(self):
        """Changes the state to STATE_COMPLETE and changes the message to a
        losing message. Pressing any key will start a new game."""
        self._mssg.text = 'You have lost. Your Score: ' \
                          + str(self._game.getBrickScore()) \
        +'. Press any Key to play again!'
        self._mssg.font_size = 18
        self._state = STATE_COMPLETE
        
    
    def _game_won(self):
        """Changes the state to STATE_COMPLETE and changes the message to a
        winning message. Pressing any key will start a new game."""
        self._mssg.text = 'You have won! Your Score: ' \
                          + str(self._game.getBrickScore()) \
        +'. Press any Key to play again!'
        self._updateScoreMssg()
        self._mssg.font_size = 18
        self._state = STATE_COMPLETE
        
    def _updateScoreMssg(self):
        """This helper function updates attribute _stats to a Glabel object that
        displays the player's score.
        If self._stats is None, it creates a new GLabel. Otherwise, this function
        changes the text attribute of the existing GLabel to the new brick score.
        """
        
        if not self._stats:
            self._stats = GLabel(x = GAME_WIDTH - GAME_WIDTH / 3,
                             y = GAME_HEIGHT - BRICK_Y_OFFSET / 2,
                             text = 'Current Score: ' + str(self._game.getBrickScore()),
                             font_size = 18, font_name = 'TimesBold.ttf',
                             bold = True, halign = 'center',
                             valign = 'middle')
        else:
            self._stats.text = 'Current Score: ' + str(self._game.getBrickScore())
            
    def _in_STATE_ACTIVE(self):
        """This is a helper function that calls all the updates that are needed
        during each frame in STATE_ACTIVE."""
        
        self._game.serveBall()
        self._updateScoreMssg()
        update_ball = self._game.updateBall()
        if update_ball == 'anothertry':
            self._tryagain()
        elif update_ball == 'lostgame':
            self._game_lost()
        elif update_ball == 'wongame':
            self._game_won()
        self._int_pause()
        
    def _in_STATE_NEWGAME(self):
        """This is a helper function that calls all the updates that are needed
        during each frame in STATE_NEWGAME."""
        self._time = 0.0
        self._game = Play()
        self._updateScoreMssg()
        self._state = STATE_COUNTDOWN
    
    
        
    
        
        
    
    
            
    






