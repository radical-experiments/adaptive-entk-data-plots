#!/bin/sh

echo script start_script `/work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/gtod` >> /work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/unit.006988/PROF

# Change to working directory for unit
cd /work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/unit.006988
echo script after_cd `/work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/gtod` >> /work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/unit.006988/PROF
# Environment variables
export RP_SESSION_ID=rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009 RP_PILOT_ID=pilot.0000 RP_AGENT_ID=agent_0 RP_SPAWNER_ID=agent_0.AgentExecutingComponent.0.child RP_UNIT_ID=unit.006988
# Pre-exec commands
echo pre  start `/work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/gtod` >> /work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/unit.006988/PROF
module restore
module load boost
module load cxx11
module load gromacs/5.1.2
module load python
export PYTHONPATH=$PYTHONPATH:/home1/02734/vivek91/modules/adaptive-msm/tests
module load hdf5
echo pre  stop `/work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/gtod` >> /work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/unit.006988/PROF
# The command to run
python "MSMproject.py" "--micro" "100" "--macro" "10" "--reference" "reference_0.pdb" "--grpname" "Protein" "--lag" "2" "--num_sims" "10" 
RETVAL=$?
echo script after_exec `/work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/gtod` >> /work/02734/vivek91/radical.pilot.sandbox/rp.session.js-172-77.jetstream-cloud.org.vivek91.017196.0009-pilot.0000/unit.006988/PROF
# Exit the script with the return code from the command
exit $RETVAL
