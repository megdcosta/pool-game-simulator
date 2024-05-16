#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

//Constants (subject to change, hahaha – include these in your .h file)
#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2 * PHYLIB_BALL_RADIUS)

#define PHYLIB_HOLE_RADIUS (2 * PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH / 2.0) // mm

#define PHYLIB_SIM_RATE (0.0001) // s
#define PHYLIB_VEL_EPSILON (0.01) // mm/s

#define PHYLIB_DRAG (150.0) // mm/s^2
#define PHYLIB_MAX_TIME (600) // s

#define PHYLIB_MAX_OBJECTS (26)


// Polymorphic object types defined as enum (include this in your .h file)
typedef enum
{
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;
//enums are like grouped constants


//Class representing a vector in 2 dimensions (include this in your .h file)
typedef struct
{
    double x;
    double y;
} phylib_coord;


//(Child) Classes representing objects on the table (include these in your .h file)

//First, a ball that is not in motion (i.e. still). It has a number (cue ball is 0) and a position on the table. 
typedef struct
{
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;


// Next, a ball that is rolling (i.e. not still). It has a number (cue ball is 0) and a position on the
// table. It also has a velocity and a (negative) acceleration (due to friction).
typedef struct
{
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

// Next, one of the 6 holes on the table. It has a position
typedef struct
{
    phylib_coord pos;
} phylib_hole;


// Next, a horizontal cushion (i.e. a cushion along either of the two the short sides of the table). It
// has only a y-coordinate
typedef struct
{
    double y;
} phylib_hcushion;


// Rather predictably, a vertical cushion (i.e. a cushion along either of the two the long sides of the
// table). It has only an x-coordinate.
typedef struct
{
    double x;
} phylib_vcushion;


// Polymorphic Parent Class of objects on the table (include these in your .h file)
// First, we need a C union that can store any of the above classes/structure in the same space.
typedef union
{
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;


// While this union can store an object of any of the above classes/structures, it cannot identify
//what the class of the object is, so we need another structure for that.
typedef struct
{
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

// Here, the type is the enum indicating the class of the object, and obj is the object itself.
// We can now use phylib_object to represent a generic object in the billiards world.


typedef struct
{
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

// As the game proceeds there will be multiple table configurations at different points in time, so
// each table “knows” its time. There can be a maximum of 26 objects on the table: 15 numbered
// balls, 1 cue ball, 4 cushions, and 6 holes.


//Part I Functions
phylib_object *phylib_new_still_ball(unsigned char number,
                                     phylib_coord *pos);
// This function will allocate memory for a new phylib_object, set its type to
// PHYLIB_STILL_BALL and transfer the information provided in the function parameters into the
// structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
// return NULL (before trying to store the function parameters in the (non-existent) structure)


phylib_object *phylib_new_rolling_ball(unsigned char number,
                                       phylib_coord *pos,
                                       phylib_coord *vel,
                                       phylib_coord *acc);


phylib_object *phylib_new_hole(phylib_coord *pos);

phylib_object *phylib_new_hcushion(double y);
phylib_object *phylib_new_vcushion(double x);

// These functions will do the same thing as the phylib_new_still_ball function for their
// respective structures.

phylib_table *phylib_new_table(void);

// This function will allocate memory for a table structure, returning NULL if the memory
// allocation fails. The member variable, time, will be set to 0.0. It will then assign the values of
// its array elements to pointers to new objects created by the phylib_new_* functions provided
// above. Specifically, it will add elements in this order:
// 1) a horizontal cushion at y=0.0;
// 2) a horizontal cushion at y=PHYLIB_TABLE_LENGTH;
// 3) a vertical cushion at x=0.0;
// 4) a vertical cushion at x=PHYLIB_TABLE_WIDTH;
// 5) 6 holes: positioned in the four corners where the cushions meet and two more
// midway between the top holes and bottom holes.
// The remaining pointers will all be set to NULL


//Part II Functions
void phylib_copy_object( phylib_object **dest, phylib_object **src );

phylib_table *phylib_copy_table( phylib_table *table );

void phylib_add_object( phylib_table *table, phylib_object *object );

void phylib_free_table( phylib_table *table );

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );

double phylib_length( phylib_coord c );

double phylib_dot_product( phylib_coord a, phylib_coord b );

double phylib_distance( phylib_object *obj1, phylib_object *obj2 );

//Part III Functions
void phylib_roll( phylib_object *new, phylib_object *old, double time );

unsigned char phylib_stopped( phylib_object *object );

void phylib_bounce( phylib_object **a, phylib_object **b );

unsigned char phylib_rolling( phylib_table *t );

phylib_table *phylib_segment( phylib_table *table );

///A2 Functions
char *phylib_object_string( phylib_object *object );
