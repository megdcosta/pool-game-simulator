import phylib;
import sqlite3; 
import os;
import math;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
 "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
 xmlns="http://www.w3.org/2000/svg"
 xmlns:xlink="http://www.w3.org/1999/xlink">
 <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;

DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;

MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

# A3 constants
FRAME_INTERVAL = 0.01;

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg( self ):
        if(BALL_COLOURS[self.obj.still_ball.number]=="WHITE"):
            return """ <circle id="cue-ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
    
################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y) as
        velocity and acceleration as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc,
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg( self ):
        if(BALL_COLOURS[self.obj.rolling_ball.number]=="WHITE"):
            return """ <circle id="cue-ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
    
################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball position (x,y) as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
    
################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires y as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;


    # add an svg method here
    def svg(self):
        y = -25 if self.obj.hcushion.y == 0 else 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)

   
    
################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires x as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        x = -25 if self.obj.vcushion.x == 0 else 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)
    

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1; 
        if self.current < MAX_OBJECTS:   
            return self[ self.current ]; 

        self.current = -1;   
        raise StopIteration; 

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        svg_content = HEADER
        
        for obj in self:
            if obj is not None:
                svg_content += obj.svg()
        
        svg_content += FOOTER 
        return svg_content
    

    def roll(self, t):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                new_ball = RollingBall(ball.obj.rolling_ball.number,
                                    Coordinate(0, 0),
                                    Coordinate(0, 0),
                                    Coordinate(0, 0))
                # compute where it rolls to
                phylib.phylib_roll(new_ball, ball, t)
                # add ball to table
                new += new_ball
            if isinstance(ball, StillBall):
                new_ball = StillBall(ball.obj.still_ball.number,
                                    Coordinate(ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y))
                # add ball to table
                new += new_ball
        # return table
        return new
    
    def createCueBall(self, xvel, yvel):
        for ball in self:
            if ((isinstance(ball, StillBall) and ball.obj.still_ball.number == 0) or
                (isinstance(ball, RollingBall) and ball.obj.rolling_ball.number == 0)):
                self.processBall(ball, xvel, yvel)

    def processBall(self, ball, xvel, yvel):
        
        isStillBall = isinstance(ball, StillBall) and ball.obj.still_ball.number == 0
        if isStillBall:
            # convert still ball to rolling
            pos = Coordinate(ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)
            ball.type = phylib.PHYLIB_ROLLING_BALL
            ball.obj.rolling_ball.pos = pos
            ball.obj.rolling_ball.num = 0

        ball.obj.rolling_ball.vel = Coordinate(xvel, yvel)
        
    
        speed_squared = xvel**2 + yvel**2
        speed = math.sqrt(speed_squared)

        if speed > VEL_EPSILON:
            xacc = -xvel / speed * DRAG
            yacc = -yvel / speed * DRAG
        else:
            xacc = yacc = 0

        ball.obj.rolling_ball.acc = Coordinate(xacc, yacc)

        

# Functions for A3
class Database():

    def __init__( self, reset=False ):
        self.db_path = "phylib.db"

        if reset and os.path.exists(self.db_path): # if reset is true, it deleted the file and new databse is created
            os.remove(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.createDB()
        
        
    # creates the database tables    
    def createDB( self ):
        cur = self.conn.cursor()
        #ball table
        cur.execute('''CREATE TABLE IF NOT EXISTS Ball (
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT)''')
        
        # TTable table
        cur.execute('''CREATE TABLE IF NOT EXISTS TTable (
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT,
            TIME FLOAT NOT NULL)''')
        
        # BallTable table
        cur.execute('''CREATE TABLE IF NOT EXISTS BallTable (
            BALLID INTEGER NOT NULL,
            TABLEID INTEGER NOT NULL,
            FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID))''')

        # Shot table
        cur.execute('''CREATE TABLE IF NOT EXISTS Shot (
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID))''')

        # TableShot table
        cur.execute('''CREATE TABLE IF NOT EXISTS TableShot (
            TABLEID INTEGER NOT NULL,
            SHOTID INTEGER NOT NULL,
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID),
            FOREIGN KEY(SHOTID) REFERENCES Shot(SHOTID))''')

        # Game table
        cur.execute('''CREATE TABLE IF NOT EXISTS Game (
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT,
            GAMENAME VARCHAR(64) NOT NULL)''')

        # Player table
        cur.execute('''CREATE TABLE IF NOT EXISTS Player (
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID))''')
        
        self.conn.commit()

    
    def readTable(self, tableID):
        
        cur = self.conn.cursor()

        balls = cur.execute('''SELECT Ball.*, TTable.TIME FROM Ball
            JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
            WHERE TTable.TABLEID = ?;''', (tableID+1,)).fetchall()

        if len(balls) == 0:
            cur.close()
            return None

        table = Table()
        #sets the time from first row
        table.time = balls[0][-1]  

        for row in balls:    
            phy_ball = self.create_ball(ballNum=row[1], xpos=row[2], ypos=row[3], xvel=row[4], yvel=row[5])
            table += phy_ball
        
        return table

    def create_ball(self, ballNum, xpos, ypos, xvel, yvel):
        if xvel is None and yvel is None:
            return StillBall(ballNum, Coordinate(xpos, ypos))
        else:
            xacc = 0
            yacc = 0
            speed_squared = xvel**2 + yvel**2
            speed = math.sqrt(speed_squared)
            if speed > VEL_EPSILON:
                xacc = (-xvel / speed) * DRAG
                yacc = (-yvel / speed) * DRAG
            return RollingBall (ballNum, Coordinate(xpos, ypos), Coordinate(xvel, yvel), Coordinate(xacc, yacc) )


    def writeTable(self, table):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO TTable (TIME) VALUES (?)''', (table.time,))
        tableID = cur.lastrowid

        for ball in table:
            if isinstance(ball, StillBall):
                self.insertStillBallIntoTable(cur, ball, tableID)
            elif isinstance(ball, RollingBall):
                self.insertRollingBallIntoTable(cur, ball, tableID)
        
        self.conn.commit()
        return tableID - 1  

    
    def insertStillBallIntoTable(self, cur, ball, tableID):
        ball_data = (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)
        insert_ball_query = '''INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)'''
        cur.execute(insert_ball_query, ball_data)
        ballId = cur.lastrowid
        cur.execute('''INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)''', (ballId, tableID))

    def insertRollingBallIntoTable(self, cur, ball, tableID):
        ball_data = (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y)
        insert_ball_query = '''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)'''
        cur.execute(insert_ball_query, ball_data)
        ballId = cur.lastrowid
        cur.execute('''INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)''', (ballId, tableID))

 
    def close ( self ):
        self.conn.commit()
        self.conn.close()
        
        
    def last_game (self):
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(GAMEID) FROM GAME")
        gameID = cur.fetchone()[0]
        cur.close()
        return gameID - 1

    def last_table(self):
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(TABLEID) FROM TTABLE")
        tableID = cur.fetchone()[0]
        cur.close()
        return tableID - 1
    
      
class Game(): 
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.db = Database() 
        
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            cur = self.db.conn.cursor()
            cur.execute('''SELECT GAMENAME FROM Game WHERE GAMEID = ?''', (gameID+1,))
            result = cur.fetchone()
            if result:
                self.gameName = result[0]

            cur.execute('''SELECT PLAYERNAME FROM Player WHERE GAMEID = ? ORDER BY PLAYERID ASC''', (gameID+1,))
            players = cur.fetchall()

            if players:
                self.player1Name = players[0][0]
                self.player2Name = players[1][0] if len(players) > 1 else None

            self.gameID = gameID+1
        elif gameID is None and all([gameName, player1Name, player2Name]):
            # Creating a new game
            cur = self.db.conn.cursor()
            cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
            self.gameID = cur.lastrowid

            for player in [player1Name, player2Name]:
                cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (self.gameID, player))
            
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            self.db.conn.commit()
        else:
            raise TypeError("Arguments are Invalid")


    def shoot(self, gameName, playerName, table, xvel, yvel):
        table.createCueBall(xvel, yvel)
        
        cur = self.db.conn.cursor()
        playerID = cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?", (playerName, self.gameID)).fetchone()
        if playerID is None:
            return

        shotID = cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID[0], self.gameID)).lastrowid

        svgFileCounter = 0
        while table:
            segmentStartTime = table.time
            segmentNext = table.segment()

            if segmentNext is None:
                break

            frameTotal = math.floor((segmentNext.time - segmentStartTime) / FRAME_INTERVAL)

            for frameIndex in range(frameTotal):
                frameTime = FRAME_INTERVAL * frameIndex
                segmentUpdatedTable = table.roll(frameTime)
                segmentUpdatedTable.time = segmentStartTime + frameTime
                    
                tableID = self.db.writeTable(segmentUpdatedTable)
                create_svg_file(segmentUpdatedTable, svgFileCounter)
                svgFileCounter +=1

                cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableID, shotID))
            table = segmentNext

        cur.close()
        self.db.conn.commit()

        
def create_svg_file(table, index):
    if table is None:
        return
    ind = index
    svg_content=table.svg()
    filename=f"table-{ind}.svg"
    ind+=1
    with open (filename, 'w') as fptr:
        fptr.write(svg_content)