## Exercise 0
 **Contributors:**

 Matrim Cirullo-Nesbitt

 Abhishek Vilekar

 Andrew Gabaldon

***
***
### 0a.)
 Review your project status. What have you been able to accomplish so far? What were you unable to do in the time you had? Be honest in your evaluation of your progress. You will not be penalized for not reaching your milestones. What does that mean you need to prioritize in the coming weeks? (at least 150 words)
***
For our project, to be clear and to have this in writing, we are trying to figure out the effect of dimples on the trajectory of a golf ball, via analysis of the velocity and spin-dependent magnus effect. Our project status is best summarized as such: we have our general plan completed, we know the complexities and difficulties associated with the project, and we have some preliminary work on the easier parts of the project done. I would say, our status is "out of the planning stage, and ready for real research and work". A big milestone we achieved as a part of this (only like two days ago) is figuring out the process that our computation and analysis will have to take. I will explain here:

First, we must set up a sort of wind-tunnel simulation, and sweep through velocities to do a boundary-layer analysis of a dimpled golf ball (and an undimpled sphere for comparison), more specifically, on the surface elements of the ball; we then decompose the forces acting on the total ball into drag(which is one-dimensional here, so analytical), gravity, and the magnus effect force (which is what's left). We then decompose the magnus force into the cross product of angular velocity and velocity, multiplied by some scalar. We mark this scalar in a table corresponding to the velocity. Once the analysis is complete (i.e. we have swept through our velocity values) we interpolate a function from our scalar table, $S(v)$. We then do a very similar analysis as we completed in exercise 1 of Midterm 1, to integrate EoM and acquire a trajectory. We check this trajectory against real ones, and more specifically, our result from exercise 1.

$%after talking with danny, I came to the idea that for the force decomposition, for each velocity step, we could take two cases, of our surface to be spinning, and then of our surface to be stationary, and take the subtraction of the force of the stationary case from the spinning case to be the force of the magnus effect (since the other forces are not spin-dependent and the magnus effect is 0 iff spin is zero). Additionally, Danny brought up the idea that in the boundary layer analysis, a way we can probe the forces on the ball (as a particle method) is by examining the change in momentum vector of some section of air (that we know the properties of) after collision with the surface.$

### 0b.)
 What problems have you encountered in doing you research? What questions came up and how did you resolve them? Are there any unresolved questions? (at least 150 words)
***
### 0c.)
 Provide an **updated** artifact from your project. This could be a plot, a code snippet, a data set, or a figure. Explain what this artifact is and how it fits into your project. (at least 150 words)
***
### 0d.)
 Update your project timeline and milestones. How will you adjust your timeline to account for the work you have done and the work you have left to do? (at least 150 words)
***