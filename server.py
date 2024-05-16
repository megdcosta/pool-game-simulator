import sys
import cgi
import os
import math
import Physics
import json
import glob

from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse, parse_qsl

def calculate_vel(x1, y1, x2, y2):
    dx = float(x2) - float(x1)
    dy = float(y2) - float(y1)
    return dx, dy


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #Parsing the path
        parsed  = urlparse( self.path );

        if parsed.path in [ '/startPage.html' ]:
            #Contains a form to describe a table with one StillBall and one RollingBall
            #Read html format from shoot.html
            fptr = open( '.'+self.path )
            content = fptr.read()
            fptr.close()
            #Set up the page to print the content
            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )
            fptr.close();
            
      
        elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):
            #Obtaining the SVG file
            fptr = open( '.'+self.path, 'rb' )
            content = fptr.read()
            fptr.close()
            #Set up the page to print the content
            self.send_response( 200 )
            self.send_header( "Content-type", "image/svg+xml" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( content )
            fptr.close()
        

        # this is for server to access the javascript file
        elif parsed.path.endswith('.js'):
            file_path = '.' + parsed.path
            with open(file_path, 'r') as fptr:
                content = fptr.read()
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
            fptr.close()



        elif parsed.path.endswith('.css'):
            file_path = '.' + parsed.path
            with open(file_path, 'r') as fptr:
                content = fptr.read()
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
            fptr.close()
        
        elif parsed.path == "/list-svgs":
            # Assuming you want to list SVGs from the current directory
            svg_files = glob.glob('*.svg')
            svg_files = [os.path.basename(svg) for svg in svg_files]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(svg_files).encode('utf-8'))


        else:
            #Generate 404 when having trouble finding the file
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8"))


    def do_POST(self):
        parsed  = urlparse( self.path );
        
        
        if parsed.path == "/send-data": #sending data to the backend
            lenOfContent = int(self.headers['Content-Length'])
            post_data = self.rfile.read(lenOfContent)
            data = json.loads(post_data.decode('utf-8'))
            
            
            self.send_response(200) #send success response to client
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            db = Physics.Database(reset=False)
            
            #compute vel and acc from values
            velX, velY = calculate_vel(float(data['x1']), float(data['y1']), float(data['x2']), float(data['y2']))

            tableNum = db.last_table()
            gameID = db.last_game()
            
            game = Physics.Game(gameID=gameID, gameName=None, player1Name=None, player2Name=None)
            
            table = db.readTable(tableNum)

            game.shoot(game.gameName, game.player1Name, table, velX, velY)  

            response = {"status": "success", "message": f"Velocity and acceleration computed and saved with table ID: {tableNum}."}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:

            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST','CONTENT_TYPE': self.headers['Content-Type'],} );
            
            for fptr in os.listdir(os.getcwd()): #delete svg files
                if fptr.endswith('.svg'):
                    os.remove(os.path.join(os.getcwd(), fptr))
                    
            table = Physics.Table()

            # Cue Ball
            table += Physics.StillBall(0, Physics.Coordinate(675.0, 2025.0))

            # 1-ball (yellow)
            table += Physics.StillBall(1, Physics.Coordinate(675.0, 1000.0))

            # 2-ball (blue), 3-ball (red) in the second row
            table += Physics.StillBall(2, Physics.Coordinate(640.0, 940.0))
            table += Physics.StillBall(3, Physics.Coordinate(710.0, 940.0))

            # 4-ball (purple), 8-ball (black), 6-ball (green) in the third row
            table += Physics.StillBall(4, Physics.Coordinate(605.0, 880.0))
            table += Physics.StillBall(8, Physics.Coordinate(675.0, 880.0))  # 8-ball in the middle
            table += Physics.StillBall(6, Physics.Coordinate(745.0, 880.0))

            # 7-ball (brown), 5-ball (orange), 9-ball (light yellow), 10-ball (light blue) in the fourth row
            table += Physics.StillBall(7, Physics.Coordinate(570.0, 820.0))
            table += Physics.StillBall(5, Physics.Coordinate(640.0, 820.0))
            table += Physics.StillBall(9, Physics.Coordinate(710.0, 820.0))
            table += Physics.StillBall(10, Physics.Coordinate(780.0, 820.0))

            # 11-ball (pink), 12-ball (medium purple), 13-ball (light salmon), 14-ball (light green), 15-ball (sandy brown) in the fifth row
            table += Physics.StillBall(11, Physics.Coordinate(535.0, 760.0))
            table += Physics.StillBall(12, Physics.Coordinate(605.0, 760.0))
            table += Physics.StillBall(13, Physics.Coordinate(675.0, 760.0))
            table += Physics.StillBall(14, Physics.Coordinate(745.0, 760.0))
            table += Physics.StillBall(15, Physics.Coordinate(815.0, 760.0))


            player1 = form["player1_name"].value
            player2 = form["player2_name"].value
            
            db = Physics.Database( reset=True )
            db.createDB()
            
            tableNum = db.writeTable(table)
            newGame = Physics.Game(gameName = "Pool Game", player1Name=player1, player2Name = player2)
        
            directory = os.getcwd()
            generatedSvgFiles = os.listdir(directory)

            for fptr in sorted(generatedSvgFiles): 
                if fptr.endswith('.svg'):
                    break; 
                

            fptr = open('poolTable.html')
            table = fptr.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(table))
            self.end_headers()
            self.wfile.write(bytes(table, "utf-8"))
            fptr.close()
            db.close()


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
    
