#include "phylib.h"

// PART I FUNCTIONS

// This function will allocate memory for a new phylib_object - still ball
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {

    phylib_object *newObj = malloc (sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    } 
    else {
        newObj -> type = PHYLIB_STILL_BALL;
        newObj -> obj.still_ball.number = number;
        newObj -> obj.still_ball.pos = *pos;
    }
    return newObj; //return new still ball object
}


// This function will allocate memory for a new phylib_object - rolling ball
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {

    phylib_object *newObj = malloc (sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    else {
        newObj ->type = PHYLIB_ROLLING_BALL;
        newObj -> obj.rolling_ball.number = number;
        newObj -> obj.rolling_ball.pos = *pos;
        newObj -> obj.rolling_ball.vel = *vel;
        newObj -> obj.rolling_ball.acc = *acc;
    }
    return newObj;
}


// This function will allocate memory for a new phylib_object - hole
phylib_object *phylib_new_hole(phylib_coord *pos) {

    phylib_object *newObj = malloc (sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    else {
        newObj -> type = PHYLIB_HOLE;
        newObj -> obj.hole.pos = *pos;
    }
    return newObj;
}


// This function will allocate memory for a new phylib_object - hcushion
phylib_object *phylib_new_hcushion(double y) {
    phylib_object *newObj = malloc (sizeof(phylib_object));
    if(newObj == NULL) {
        return NULL;
    }
    else {
        newObj -> type = PHYLIB_HCUSHION;
        newObj -> obj.hcushion.y = y;
    }
    return newObj;
}

// This function will allocate memory for a new phylib_object - vcushion
phylib_object *phylib_new_vcushion(double x) {
    phylib_object *newObj = malloc (sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }

    else {
        newObj -> type = PHYLIB_VCUSHION;
        newObj -> obj.vcushion.x = x;
    }
    return newObj;
}

// This function will allocate memory for a table structure
phylib_table *phylib_new_table(void) {
    phylib_table *new_table =malloc(sizeof(phylib_table));

    if (new_table == NULL) {
        return NULL; // return NULL if the memory allocation failed
    }

    phylib_coord pos;

    // time will be set to 0.0
    new_table->time = 0.0;
    

    // assign values of array elements to pointers to new objects by using the above functions
    
    // horizontal cushion at y=0.0 and y=PHYLIB_TABLE_LENGTH
    new_table->object[0] = phylib_new_hcushion(0.0); 
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); 

    // vertical cushion at x=0.0 and x=PHYLIB_TABLE_WIDTH
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //6 holes positioned in the four corners where the cushions meet and two more midway between the top holes and bottom holes
    pos.x = 0.0;
    pos.y = 0.0;
    new_table->object[4] = phylib_new_hole(&pos);

    pos.x = 0.0;
    pos.y = PHYLIB_TABLE_WIDTH;
    new_table->object[5] = phylib_new_hole(&pos);

    pos.x = 0.0;
    pos.y = PHYLIB_TABLE_LENGTH;
    new_table->object[6] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH;
    pos.y = 0.0;
    new_table->object[7] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH;
    pos.y = PHYLIB_TABLE_WIDTH;
    new_table->object[8] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH;
    pos.y = PHYLIB_TABLE_LENGTH;
    new_table->object[9] = phylib_new_hole(&pos);
    
    // set the remaining pointers to NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; ++i) {
        new_table->object[i] = NULL;
    }
    return new_table;

}

// PART II FUNCTIONS


// This function allocates new memory for a phylib_object, save address f object at location pointed to by dest and copy over the contents object from src
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {

    if (*src == NULL) {
        *dest = NULL;
    }
    else {
        *dest = malloc (sizeof(phylib_object));

        if (*dest != NULL) {
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    }

}

// This function allocates memory for a new phylib_table 
phylib_table *phylib_copy_table( phylib_table *table ) {

    phylib_table *new_table = malloc(sizeof(phylib_table));

    if (new_table == NULL) {
        return NULL; //return NULL if malloc fails
        
    } 
    else{
        new_table->time = table->time;

        for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
            phylib_copy_object(&new_table->object[i], &table->object[i]);
        }
    }
    return new_table; 
}


void phylib_add_object( phylib_table *table, phylib_object *object ){

    for ( int i=0; i< PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) { // iterate over the object array in the table until it finds a NULL pointer 
            table->object[i] = object; // assign that pointer to be equal to the address of object
            break;
        }
    }

}


void phylib_free_table( phylib_table *table ) {

    for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            free(table->object[i]); //free every non-NULL pointer in the object array of table
        }
    }
    free(table); // then free the table as well

}

// This function returns the difference between c1 and c2
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {

    phylib_coord coordinate;

    coordinate.x = c1.x - c2.x; // x value
    coordinate.y = c1.y - c2.y; // y value

    return coordinate;

}

// Return the length of the vector/coordinate c
double phylib_length( phylib_coord c ){

    return sqrt((c.x*c.x) + (c.y*c.y)); // calculate length using pythagorean theorem

}

// This function computes the dot-product between two vectors
double phylib_dot_product( phylib_coord a, phylib_coord b ) {

    return ( (a.x*b.x) + (a.y*b.y) );

}

// This function calculates the distance between two objects, pbj1 and obj2
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {

    // obj1 must be a PHYLIB_ROLLING_BALL
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0; // if it is not then return -1.0
    }

    if (obj1 == NULL || obj2 == NULL) {
        return -1.0; 
    }

    double distance = 0.0;
    phylib_coord coordinate;
    phylib_coord centre1 = obj1->obj.rolling_ball.pos; //centre of obj1

    switch (obj2->type) {

    // If obj2 is a rolling ball, compute distance between the centres of two balls and subtract ball diameter (PHYLIB_BALL_DIAMETER)
    case PHYLIB_ROLLING_BALL:
        coordinate = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        distance = phylib_length(coordinate);
        return distance - PHYLIB_BALL_DIAMETER;

    // If obj2 is a still ball, compute distance between the centres of two balls and subtract ball diameter (PHYLIB_BALL_DIAMETER)
    case PHYLIB_STILL_BALL: 
        coordinate= phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
        distance = phylib_length(coordinate);
        return distance - PHYLIB_BALL_DIAMETER;

    // If obj2 is a hole, then compute the distance between the centre of the ball and the hole and subtract HOLE_RADIUS
    case PHYLIB_HOLE: 
        distance = sqrt(((centre1.x - obj2->obj.hole.pos.x) * (centre1.x-obj2->obj.hole.pos.x)) + ((centre1.y - obj2->obj.hole.pos.y) * (centre1.y - obj2->obj.hole.pos.y)));
        return distance - PHYLIB_HOLE_RADIUS;

    //if obj2 is a cushion, calculate the distance between the centre of the ball and the cushion and subtract the BALL_RADIUS
    case PHYLIB_HCUSHION: 
        return fabs(centre1.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;

    case PHYLIB_VCUSHION: 
        return fabs(centre1.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;

    //return -1.0 if obj2 isn't any valid type
    default: 
        return -1.0;
    }
}

// PART III FUNCTIONS

// This function updates a new phylib_object that represents a the old phylib_object after it has rolled or a period of time
void phylib_roll( phylib_object *new, phylib_object *old, double time) {
    phylib_coord newPos; // temp variable to store new position
    phylib_coord newVelocity; // temp variable to store new velocity
    phylib_coord newAcc; // temp variable to store new acceleration

    if ( (old->type == PHYLIB_ROLLING_BALL) && (new->type == PHYLIB_ROLLING_BALL) ) {

        double newVelx = new->obj.rolling_ball.vel.x;
        double newVely = new->obj.rolling_ball.vel.y;

        newPos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + ((0.5) * old->obj.rolling_ball.acc.x * time * time);
        new->obj.rolling_ball.pos.x = newPos.x; 

        newVelocity.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
        new->obj.rolling_ball.vel.x = newVelocity.x;

        newPos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + ((0.5) * old->obj.rolling_ball.acc.y * time * time);
        new->obj.rolling_ball.pos.y = newPos.y;

        newVelocity.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;
        new->obj.rolling_ball.vel.y = newVelocity.y;

        if ((newVelx * newVelocity.x) < 0) {
            newVelocity.x = 0.0;
            new->obj.rolling_ball.vel.x = newVelocity.x;
            newAcc.x = 0.0;
            new->obj.rolling_ball.acc.x = newAcc.x;
            
        }

        if ((newVely * newVelocity.y) < 0) {
            newVelocity.y = 0.0;
            new->obj.rolling_ball.vel.y = newVelocity.y;
            newAcc.y = 0.0;
            new->obj.rolling_ball.acc.y = newAcc.y;
            
        }
    }
}

// This function checks whether ROLLING_BALL has stopped, and if it has, will convert it to a STILL_BALL
unsigned char phylib_stopped( phylib_object *object ) {

    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {

        object->type = PHYLIB_STILL_BALL;
        unsigned char ballNumber = object->obj.rolling_ball.number;
        phylib_coord ballPos = object->obj.rolling_ball.pos;
        object->obj.still_ball.number = ballNumber;
        object->obj.still_ball.pos = ballPos;
        return 1; // return 1 if it converts the ball
    }
    
    return 0; // return 0 if it does not convert the ball
}

void phylib_bounce(phylib_object **a, phylib_object **b) {

    if ((*b)->type == PHYLIB_HCUSHION) {
        // If it's a horizontal cushion, reverse the y-velocity and y-acceleration of object 'a'
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
    }
    else if ((*b)->type == PHYLIB_VCUSHION) {
        // If it's a vertical cushion, reverse the x-velocity and x-acceleration of object 'a'
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
    }
    else if ((*b)->type == PHYLIB_HOLE) {
        // If it's a hole, free the memory of object 'a' and set it to NULL
        free(*a);
        *a = NULL;
        return;
    }
    else if ((*b)->type == PHYLIB_STILL_BALL) {
        // If it's a still ball, extract number and position, and convert it into a rolling ball
        double num = (*b)->obj.still_ball.number;
        phylib_coord pos = (*b)->obj.still_ball.pos;

        (*b)->type = PHYLIB_ROLLING_BALL;
        (*b)->obj.rolling_ball.number = num;
        (*b)->obj.rolling_ball.pos = pos;
        (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.acc.x = (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y = 0.0;
        (*b)->obj.rolling_ball.acc.y = (*b)->obj.rolling_ball.acc.y = 0.0;

    }

    //if 'b' is a rolling ball, perform collision response
    if ((*b)->type == PHYLIB_ROLLING_BALL) {

        phylib_coord r_ab;  
        phylib_coord v_rel;
        phylib_coord n;     
        double v_rel_n;

        //calculate relative position and velocity between 'a' and 'b'
        r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
        v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);


        //calculate normal vector and relative velocity along the normal
        n.x = r_ab.x / phylib_length(r_ab);
        n.y = r_ab.y / phylib_length(r_ab);
        v_rel_n = phylib_dot_product(v_rel, n);


        //update velocities for elastic collision
        (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
        (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

        (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
        (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

        // Calculate speeds and apply drag forces
        double speedA = phylib_length((*a)->obj.rolling_ball.vel);
        double speedB = phylib_length((*b)->obj.rolling_ball.vel);

        if (speedA > PHYLIB_VEL_EPSILON) {
            (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / speedA) * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / speedA) * PHYLIB_DRAG;
        }

        if (speedB > PHYLIB_VEL_EPSILON) {
            (*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x / speedB) * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y / speedB) * PHYLIB_DRAG;
        }
    }
}


unsigned char phylib_rolling( phylib_table *t ) {
    unsigned char numberOfBalls = 0;

    for ( int i = 0; i<PHYLIB_MAX_OBJECTS; i++) {
        if ( (t->object[i] != NULL ) && (t->object[i]->type == PHYLIB_ROLLING_BALL) ) {
            numberOfBalls++; //increments the number of balls
        }
    }
    return numberOfBalls;
}


phylib_table *phylib_segment(phylib_table *table) {

    double passedTime = 0.0;

    if (phylib_rolling(table) == 0) {
        return NULL; //if no rolling balls, return NULL
    }

    //create new table as a copy of input table
    phylib_table *new_table = phylib_copy_table(table);
    if (new_table == NULL) {
        return NULL; //if unable to create a new table, return NULL
    }

    //simulation loop
    while(passedTime <= PHYLIB_MAX_TIME){
        passedTime += PHYLIB_SIM_RATE; // increment the passedTime

        //loop through each object in the table
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL){
                phylib_roll(new_table->object[i], table->object[i], passedTime); // simulate rolling motion of the rolling ball

                //check if rolling ball has stopped
                //unsigned char isStopped = phylib_stopped(new_table->object[i]);
            }
        }
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL){
                if (phylib_stopped(new_table->object[i]) == 1){
                    new_table->time += passedTime; //update total time if rolling ball has stopped
                    return new_table; 
                }

                //check for collisions with other objects in the table
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                    double distance = phylib_distance(new_table->object[i], new_table->object[j]);
                    if (new_table->object[j] != NULL && i != j && distance < 0.0){ //if other object exists, there is a collision
                        phylib_bounce(&new_table->object[i], &new_table->object[j]); //if there is collission, bounce the rolling ball off the other object
                        //update time and return new table
                        new_table->time += passedTime;
                        return new_table;
                    }
                }
            }
        }
    }
    //return final state of table after simulation
    return new_table;
}

//A2 Function(s)
char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80, "HOLE (%6.1lf,%6.1lf)", object->obj.hole.pos.x, object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,"HCUSHION (%6.1lf)", object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80, "VCUSHION (%6.1lf)", object->obj.vcushion.x );
            break;
    }
    return string;
}
