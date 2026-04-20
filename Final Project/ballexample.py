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

done_saving = pygame.USEREVENT + 1 # Make a new user event
saving = False #initialize global saving for ball_math
total_impulse = [0,0]
class RigidAirSimulation(object):
    """
    This class implements a simulation of air on a rotating or static ball.
    Air starts on one side, and travels to the other with an initial velocity determined by its random position.
    Outputs to console (for now) when air interacts with the large central ball.
    """

    def __init__(self) -> None:
        # Space
        self._space = pymunk.Space()

        # Physics
        # Time step
        self._dt = (0.5) / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 4

        #Important collision handling
        self._space.on_collision(1,2,begin=self._ball_show,post_solve=self._ball_math)

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((300, 600))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_SHAPES

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
            self._clock.tick(60)
            fps = self._clock.get_fps()
            pygame.display.set_caption("fps: " + f"{fps:.2f}")
    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (0, 320), (300, 320), 0.0),
            pymunk.Segment(static_body, (0, 100), (300, 100), 0.0)
        ]
        for line in static_lines:
            line.elasticity = 0.01
            line.friction = 0.01
        self._space.add(*static_lines)
    
    def _add_golf_ball(self) -> None:
        """SON D:"""
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = 150,210
        body.angular_velocity = 2*np.pi
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                saving = True #flag for saving frames 
                pygame.time.set_timer(done_saving,10000) # set timer for event to trigger in 10000 ms
                print("Saving next 10000ms") 
            elif event.type == done_saving:
                saving = False #update flag
                force = np.array(total_impulse) / 10000
                print("Save complete")
                print(f"Force is {force[0]:.2e} m/s? in x-direction.\nForce is {force[1]:.2e} m/s? in y-direction.")
                pygame.time.set_timer(done_saving, 0) # is this necessary? ideally the timer should stop automatically, since set_timer was called with loops=0.
    def _update_balls(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            i = 1
            while i < 40: #create 40 air "molecules" per tick
                self._create_ball()
                i += 1
            self._ticks_to_next_ball = 1
        # Remove balls that move farther than bounding box horizontally
        balls_to_remove = [ball for ball in self._balls if (ball.body.position.x > 300 or ball.body.position.x < 10)]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def _create_ball(self) -> None:
        """
        Create a ball.
        :return:
        """
        mass = 5.3E-9  # in kg
        radius = 1 # in mm
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia) #testing 0 moment
        x = 10
        y = random.randint(101,600-281)
        body.position = x, y
        body.velocity = -(1/169.8)*(y-((319+101)/2))**2+70, 0
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
            print("It matters! It does matter!!")



def main():
    game = RigidAirSimulation()
    game.run()

start_sim_time = time.perf_counter()

if __name__ == "__main__":
    main()