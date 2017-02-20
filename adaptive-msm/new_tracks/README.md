# New tracks

## Track 0

* Plot the trajectories generated (in the simulation phase) in psi-phi space. Check if they occupy only two quadrants in psi-phi space.
* If they don't, there is a mistake in the clustering phase. Change Kmeans to Kcenters clustering.

## Track 1

* Let S<sub>i</sub> be the stationary probability of the i<sup>th</sup> macrostate. Each microstate m<sub>j</sub> assigned to this macrostate has the stationary probability: S<sub>i</sub> / Total number of microstates within this macrostate.

* Hence, each macrostate has an associated (phi,psi) value from its configuration and stationary probability. Plot it psi-phi space.

## Track 2 

* Randomly sample N<sub>x</sub> configurations from each macrostate.
* Each of these configurations will have a (phi, psi) value.
* Discretize the psi, phi space into multiple bins. Iterate through all the (psi,phi) values from the configurations and increment the respective bins.
