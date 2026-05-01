This is the instruction manual to our simulation.

Collaborators:
Matrim Cirullo-Nesbitt
Abhishek Vilekar
Andrew Gabaldon

Before running the file, make sure you have either a python shell you can access (like conda) or python added to your PATH.
The file is run via the command line, with arguments.
(obviously, you must `cd` to the directory the `golfsimulator.py` lies in)
The command to run the file in powershell or cmd is as such:
python golfsimulator.py --num1 v_max --num2 particles_per_tick --num3 omega

--num1
This argument accepts an integer value of the maximum velocity of the air particles that are spawned in the sim.
This is adjusted for m/s, so put in a value in m/s (preferrably between 1 and 70).
Required, defaults to 70.

--num2
This argument accepts an integer value of the number of air particles spawned each frame.
This number should be about 10-20 greater than the number used for initial velocity, rounded to the nearest 5.
Required, defaults to 90

--num3
This argument accepts an float value of the constant angular velocity of the golf ball.
This number should be between -2pi and 2pi, in radians/sec. Higher values can work, but may give unexpected results.
Optional, defaults to 1.0

--save
This argument accepts a single-character string, case-sensitive, which dicates whether each frame of the simulation will be saved to images on the save keypress.
Don't turn this on, unless you have a folder named "golfsimulator_images", and are trying to make a .gif file out of the images.
Specifically accepts "Y" for true, and disregards any other string.
Optional, defaults to "N"


Once the file is running, there will be a screen that pops up, this is referred to as the game window.
It is captioned with the FPS of the simulation and the real-time percentage (RTP) that the simulation is running at. Importantly the sim is balanced around 120fps being real-time.
With the game window as the active window there are a few keybinds that do important things.

"D"
Pressing the "D" key will show all objects currently in the simulation, i.e. will give a visualization.
This is very useful to qualitatively determine the state of the simualation.
Turning on "rendering" however, is very performance intensive, so expect the framerate and RTP to drop by half or more.
This doesn't influence the physics of the simulation, rather just shows a visualization.

"C"
Pressing the "C" key will stop showing all objects in the simulation.
This is very useful when letting the simulation equalize to a "long-term" state where are not large areas of 'vacuum'.
This generally increases performance over showing the objects, and is thus the default mode for the simulation to appear in.

"S"
Pressing the "S" key will initialize the process of saving the forces on the central golf ball.
The "save" will last for 60 frames, and once complete will output to console with the forces, a timestamp, and a completion message.
It will also save all relevant parameters of the simulation (and forces) to the `force.csv` file.
When the key is pressed multiple times before the save is finished, it will output a message to console, and restart the save for the next 60 frames.
Generally, dont press this until the simulation looks how you would expect the airflow around a ball to look like. This will occur at "long-range" so likely at least 20 seconds real time.

One can press "Esc" or click the x in the corner of the window to close the simulation.

