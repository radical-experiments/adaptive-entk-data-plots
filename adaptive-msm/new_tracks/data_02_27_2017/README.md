# New tracks

## Track 0

* Plot the trajectories generated (in the simulation phase) in phi-psi space. The phi-psi space is discretized into multiple bins. Depending on the (phi, psi) value of the trajectories, the respective bin's count is incremented.
* Check if the values occupy only two quadrants in phi-psi space.
* If they don't, there is a mistake in the clustering phase. Change Kmeans to Kcenters clustering.

Note: The plot represents the number of trajectories (count) in phi-psi space.

## Track 1

* Let S<sub>i</sub> be the stationary probability of the i<sup>th</sup> macrostate. Each microstate m<sub>j</sub> assigned to this macrostate has the stationary probability: S<sub>i</sub> / Total number of microstates within this macrostate.
* Hence, each macrostate has an associated (phi,psi) value from its configuration and stationary probability. 
* Use the probability to determine the free energy associated with that microstate, plot it in phi-psi space.

Note: The plot represents the free energy values in phi-psi space. 

## Track 2 

* Randomly sample N<sub>x</sub> configurations from each macrostate.
* Each of these configurations will have a (phi, psi) value.
* Discretize the psi, phi space into multiple bins. Iterate through all the (psi,phi) values from the configurations and increment the respective bin's count.

Note: The plot represents the number of trajectories in phi-psi space.
