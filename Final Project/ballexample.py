#SOME OF THIS IS COPIED FROM https://github.com/viblo/pymunk/blob/master/pymunk/examples/bouncing_balls.py !!!

__docformat__ = "reStructuredText"

# Python imports
import random
import time
import sys

# Library imports
import pygame
import numpy as np

# pymunk imports
import pymunk
import pymunk.pygame_util
from sympy import fps

xlim = (0,700)
done_saving = pygame.USEREVENT + 1 # Make a new user event
saving = False #initialize global saving for ball_math
total_impulse = [0,0]
#initialize some global variables.

class RigidAirSimulation(object):
    """
    This class implements a simulation of air on a rotating or static ball.
    Air starts on one side, and travels to the other with an initial velocity determined by its random position.
    Outputs to console (for now) when air interacts with the large central ball.
    """

    def __init__(self) -> None:
        # Space
        self._space = pymunk.Space()

        self._space.use_spatial_hash(2.1,200000)
        # Physics
        # Time step
        self._dt = 1 / 120
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 4
        global v_mult
        v_mult = 1/(self._physics_steps_per_frame/(self._dt) * (1/1000) * (1/2.34))

        #Important collision handling
        self._space.on_collision(1,2,begin=self._ball_show,post_solve=self._ball_math)

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((xlim[1], 400))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        # use this for actually performing simulations for data
        self._draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_CONSTRAINTS
        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()
        # Static/rotating golf ball that the balls hit.
        self._add_golf_ball()
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
            print(f"Number of balls: {len(self._balls)}")
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(60)
            fps = self._clock.get_fps()
            frame += 1
            pygame.display.set_caption("fps: " + f"{fps:.2f}")
    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (xlim[0], 322), (xlim[1], 322), 0.0),
            pymunk.Segment(static_body, (xlim[0], 98), (xlim[1], 98), 0.0)
        ]
        for line in static_lines:
            line.elasticity = 0.01
            line.friction = 0.01
        self._space.add(*static_lines)
    
    def _add_golf_ball(self) -> None:
        """SON D:"""
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = 300,210
        body.angular_velocity = 103*np.pi
        shape = pymunk.Circle(body,50)
        shape.elasticity = 0.95
        shape.friction = 0.25
        shape.collision_type = 2 #golf ball...
        self._space.add(body,shape)

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                saving = True #flag for saving frames
                save_start_frame = frame
                save_time = time.time()
                print(f"Saving next {int(1/(2*self._dt)):.0f} frames.") 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self._draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_SHAPES
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                self._draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_CONSTRAINTS
            if saving == True and frame >= int(1/(2*self._dt))+save_start_frame:
                saving = False #update flag
                force = -1 * 2 * np.array(total_impulse) / (2.34 * 1000)
                curr_time = time.time() - save_time
                print(f"Save complete in {curr_time:.2f} seconds.")
                print(f"Force is {force[0]:.2e}N in x-direction.\nForce is {force[1]:.2e}N in y-direction.")

        
    def _update_balls(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            i = 1
            while i < 220: #create 120 air "molecules" per tick
                self._create_ball()
                i += 1
            self._ticks_to_next_ball = 1
        # Remove balls that move farther than bounding box horizontally
        balls_to_remove = [ball for ball in self._balls if 
                           (ball.body.position.x > xlim[1] or
                            ball.body.position.x < 10+xlim[0] or
                            ball.body.position.y < 98 or
                            ball.body.position.y > 322)]
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
        y = random.randint(101,600-281)
        body.position = x, y
        body.velocity = v_mult*(-(1/169.8)*(y-((319+101)/2))**2+70), 0
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
        Add impulse (equals $\Delta p$) to total momentum change, 
        """
        global total_impulse
        if saving == True:
            old_total_impulse = pymunk.vec2d.Vec2d(*total_impulse)
            total_impulse = list(arbiter.total_impulse + old_total_impulse)
            #print("It matters! It does matter!!")



def main():
    game = RigidAirSimulation()
    game.run()

start_sim_time = time.perf_counter()

if __name__ == "__main__":
    main()
pygame.display.quit()
pygame.quit()
sys.exit()