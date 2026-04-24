#SOME OF THIS IS COPIED FROM https://github.com/viblo/pymunk/blob/master/pymunk/examples/bouncing_balls.py !!!

__docformat__ = "reStructuredText"

# Python imports
import random
import time
import sys
import csv
import argparse
from PIL import Image

# Library imports
import pygame
import numpy as np
import pandas as pd

# pymunk imports
import pymunk
import pymunk.pygame_util
import pymunk.autogeometry


xlim = (0,700)
ylim = (100,500)
done_saving = pygame.USEREVENT + 1 # Make a new user event
saving = False #initialize global saving for ball_math
total_impulse = [0,0]
golf_ball_omega = 1 #rad / s
save_img_bool = False

v_max = 70 # default, changed with args
count_per_tick = 40 # default, changed with args

#initialize some global variables.
def vel_scaling(y,v_max):
    f = v_max / ( (ylim[0] - np.average(ylim))**2 )
    return -f * (y-np.average(ylim))**2 + v_max #gives a scaling velocity curve to the spawned air.


img = Image.open('GolfBallSmall.png')
img_bw = img.convert('L')
img.close()
img_array = np.array(img_bw)
#Get our golf ball!
def sampler(point) -> float:
    x = int(point[0])
    y = int(point[1])
    return 1 - img_array[x,y] / 255

pl_set = pymunk.autogeometry.march_soft(
    pymunk.BB(0,0,100,100),1000,1000,threshold=1/255,sample_func=sampler)

class RigidAirSimulation(object):
    """
    This class implements a simulation of air on a rotating or static ball.
    Air starts on one side, and travels to the other with an initial velocity determined by its random position.
    Outputs to console (for now) when air interacts with the large central ball.
    """

    def __init__(self) -> None:
        # Space
        self._space = pymunk.Space()

        self._space.use_spatial_hash(2.1,300000)
        # Physics
        # Time step
        self._dt = 1 / 120
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 4
        global v_mult
        v_mult = 1/(1/(self._dt) * (1/1000) * (2.34))
        # parentheses should be frames / second * m / mm * mm / unit = (frames * m )/(second * unit)
        # then, reciprocal is (second * unit) / (frames * m), which multiplied by m / s gives, unit / frame

        #Important collision handling
        self._space.on_collision(1,2,begin=self._ball_show,post_solve=self._ball_math)

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((xlim[1], ylim[1]+10))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        # use this for actually performing simulations for data
        self._draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_CONSTRAINTS
        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()
        # Static/rotating golf ball that the balls hit.
        #self._add_golf_ball()
        self._add_good_golf_ball()

        # Balls that exist in the world
        self._balls: list[pymunk.Circle] = []
        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 1

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        global frame
        frame = 0
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._process_events()
            self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(240)
            fps = self._clock.get_fps()
            frame += 1
            #print(f"Number of balls: {len(self._balls)}, frame #: {frame}.")
            pygame.display.set_caption("fps: " + f"{fps:.2f}")
    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_boxes = [
            pymunk.Poly(self._space.static_body, [(xlim[0],ylim[1]),
                                                  (xlim[1],ylim[1]),
                                                  (xlim[1],ylim[1]+2),
                                                  (xlim[0],ylim[1]+2)]),
            pymunk.Poly(self._space.static_body, [(xlim[0],ylim[0]),
                                                  (xlim[1],ylim[0]),
                                                  (xlim[1],ylim[0]-2),
                                                  (xlim[0],ylim[0]-2)])
        ]
        
        for box in static_boxes:
            box.elasticity = 1
            box.friction = 0.01
        self._space.add(*static_boxes)
    
    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        global saving
        global save_start_frame
        global save_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                total_impulse[0],total_impulse[1] = 0,0
                if saving:
                    print("Save interrupted! Restarting save.")
                saving = True #flag for saving frames
                save_start_frame = frame
                save_time = time.time()
                print(f"Saving next {int(1/(2*self._dt)):.0f} frames.") 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self._draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_SHAPES
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                self._draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_CONSTRAINTS
        if saving == True and save_img_bool == True:
            pygame.image.save(self._screen, f"golfsimulator_images/simcap_frame_{frame}_date_{time.time()}.png")
        if saving == True and frame >= int(1/(2*self._dt))+save_start_frame:
            saving = False #update flag
            force_mag = 1000 * np.array(total_impulse) / (2*2.34)
            force = [-force_mag[0],-force_mag[1]] # negates impulse on the air particles to give the impulse on the ball.
            total_impulse[0],total_impulse[1] = 0,0
            curr_time = time.time() - save_time
            print(f"Save complete in {curr_time:.2f} seconds.")
            force_data = [v_max, 
                          force[0],
                          force[1],
                          count_per_tick,
                          int(curr_time),
                          time.ctime(),
                          golf_ball_omega]
            filename = 'force_output.csv'
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(force_data)
                file.close()
            print(f"Force is {force[0]:.2e}N in x-direction.\nForce is {force[1]:.2e}N in y-direction.")

        
    def _update_balls(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            i = 0
            while i < count_per_tick: #create 219 air "molecules" per tick
                self._create_ball()
                i += 1
            self._ticks_to_next_ball = 1
        # Remove balls that move farther than bounding box horizontally
        balls_to_remove = [ball for ball in self._balls if 
                           (ball.body.position.x > xlim[1] or
                            ball.body.position.x < 10+xlim[0] or
                            ball.body.position.y < ylim[0]-2 or
                            ball.body.position.y > ylim[1]+2)]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def _create_ball(self) -> None:
        """
        Create a ball.
        :return:
        """
        mass = 6.87E-8  # in kg
        radius = 1 # in mm ( 2.34301780694 units/mm. )
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia) #testing 0 moment
        x = 10
        y = random.randint(ylim[0]+1,ylim[1]-1)
        body.position = x, y
        body.velocity = v_mult*vel_scaling(y,v_max), 0
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 1
        shape.friction = 0
        shape.collision_type = 1
        self._space.add(body, shape)
        self._balls.append(shape)

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)
    def _ball_show(self,arbiter,space,data):
        """
        Say beginning of collision. Test. \n
        Returns True
        """
        hit_end_time = time.perf_counter()
        hit_time = hit_end_time - start_sim_time
        #print(f"Collision occured with golf ball at {hit_time:.2f} seconds!")
        return True
    def _ball_math(self,arbiter,space,data) -> None:
        """
        Access impulse on ball due to collision (post_solve).
        Add impulse (equals $\\Delta p$) to total momentum change, 
        """
        global total_impulse
        if saving == True:
            old_total_impulse = pymunk.vec2d.Vec2d(*total_impulse)
            total_impulse = list(arbiter.total_impulse + old_total_impulse)
            #print("It matters! It does matter!!")
    def _add_good_golf_ball(self):
        body1 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body1.position = 220,np.average(ylim)
        body1.angular_velocity = golf_ball_omega
        self._space.add(body1)
        for polyline in pl_set:
            simple = pymunk.autogeometry.simplify_curves(polyline,0.5)

            for i in range(len(simple)-1):
                #print(str(list(simple[i])) + str(list(simple[i+1])))
                point1 = pymunk.vec2d.Vec2d(
                        simple[i][0] - 50,
                        simple[i][1] - 50
                )
                point2 = pymunk.vec2d.Vec2d(
                        simple[i+1][0] - 50,
                        simple[i+1][1] - 50
                    )
                #point1 = simple[i]
                #point2 = simple[i+1]
                shape = pymunk.Segment(body = body1,a = point1, b = point2,radius=1) #change radius? run it!
                shape.elasticity = 1
                shape.friction = 0.25
                shape.collision_type = 2
                #print(f"We are line number {i}!")
                self._space.add(shape)
    def _add_golf_ball(self) -> None:
        """SON D:"""
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = 220,np.average(ylim)
        body.angular_velocity = 2#41*np.pi #about 240pi rad/s just showing the rotation
        shape = pymunk.Circle(body,50)
        shape.elasticity = 1
        shape.friction = 0.25
        shape.collision_type = 2 #golf ball...
        self._space.add(body,shape)



def main():
    game = RigidAirSimulation()
    game.run()

start_sim_time = time.perf_counter()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that runs a simulation of airflow on a ball."
    )
    parser.add_argument("--num1", required=True, type=int, help=
                        "Velocity maximum of air in simulation.")
    parser.add_argument("--num2", required=True, type=int,help=
                        "Number of air \"molecules\" spawned per frame. Use lower count for lower max velocity, max at 90.")
    parser.add_argument("--num3", required=False, type=float, default=1.0, help=
                        "Radial velocity of the golf ball in rad/s. Change to mess with parameters, don't change for testing suite. Defaults to 1 rad/s")
    parser.add_argument("--save", required=False, type=str, default="N", help=
                        "Input \'Y\'/\'N\' - Whether to save a series of images to disk upon hitting the 's' key. Defaults to \'N\'. Case sensitive.")
    args = parser.parse_args()
    v_max = args.num1
    count_per_tick = args.num2
    golf_ball_omega = args.num3
    save = args.save
    if save == "Y":
        save_img_bool = True
    main()
print(f"Exiting at {time.ctime()}.")
pygame.display.quit()
pygame.quit()
sys.exit()