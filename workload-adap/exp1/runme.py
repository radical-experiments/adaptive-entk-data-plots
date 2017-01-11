__author__    = "Vivek Balasubramanian <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2016, http://radical.rutgers.edu"
__license__   = "MIT"

from radical.entk import EoP, AppManager, Kernel, ResourceHandle

from grompp import grompp_kernel
from mdrun import mdrun_kernel
from randomize_kernel import random_kernel

import argparse

ENSEMBLE_SIZE=16
PIPELINE_SIZE=3
ITER=[1 for x in range(1, ENSEMBLE_SIZE+1)]
TOTAL_ITERS=1
SUM=0

class Test(EoP):

    def __init__(self, ensemble_size, pipeline_size):
        super(Test,self).__init__(ensemble_size, pipeline_size)

    def stage_1(self, instance):

        k1 = Kernel(name='grompp')
        k1.arguments = [  "--mdp=PLCpep7_run.mdp",
                                "--conf=PLCpep7.gro",
                                "--ndx=PLCpep7.ndx",
                                "--top=PLCpep7.top",
                                "--out=PLCpep7.tpr"
                            ]        
        k1.cores=1


        k1.copy_input_data = [
                              '$SHARED/PLCpep7.ndx',
                              '$SHARED/PLCpep7.top'
                            ]


        global ITER

        if (ITER[instance-1]==1):
            k1.copy_input_data += ['$SHARED/PLCpep7_run.mdp'.format(instance), '$SHARED/PLCpep7.gro']
        else:
            k1.copy_input_data += ['$ITER_{1}_STAGE_4_TASK_{0}/PLCpep7_run.mdp'.format(instance, ITER[instance-1]-1),
                                   '$ITER_{1}_STAGE_3_TASK_{0}/PLCpep7.gro'.format(instance, ITER[instance-1]-1)]

        return k1


    def stage_2(self, instance):

        #global SUM
        global ITER

        k2 = Kernel(name="mdrun")
        k2.arguments = [
                            "--tag=PLCpep7",
                            "--out=PLCpep7_dhdl.xvg"
                        ]
        if ITER[instance-1] == 1:
            k2.cores = 8
            k2.arguments = [
                            "--tag=PLCpep7",
                            "--out=PLCpep7_dhdl.xvg",
                            "--nt=8"
                        ]

        else:
            f = open('output_%s.txt'%instance,'r')
            line = f.readlines()
            cores = int(line[0].strip())
            k2.cores = cores
            k2.arguments = [
                            "--tag=PLCpep7",
                            "--out=PLCpep7_dhdl.xvg",
                            "--nt=%s"%cores
                        ]
            f.close()
            

        k2.copy_input_data = ['$STAGE_1_TASK_{0}/PLCpep7.tpr'.format(instance)]

        return k2


    def stage_3(self, instance):

        k3 = Kernel(name="random")
        k3.arguments = [    "--min=1",
                            "--max=8"
                        ]

        k3.cores = 1
        k3.copy_input_data = ['$SHARED/rand_num_gen.py']
        k3.download_output_data = ['output.txt > output_%s.txt'%instance]

        return k3

    def branch_3(self, instance):

        if ITER[instance-1] <= 2:
            self.set_next_stage(stage=1)
            ITER[instance-1]+=1

        


if __name__ == '__main__':

    # Create pattern object with desired ensemble size, pipeline size
    pipe = Test(ensemble_size=ENSEMBLE_SIZE, pipeline_size=PIPELINE_SIZE)

    # Create an application manager
    app = AppManager(name='Expanded_Ensemble', on_error='exit')

    # Register kernels to be used
    app.register_kernels(grompp_kernel)
    app.register_kernels(mdrun_kernel)
    app.register_kernels(random_kernel)

    # Add workload to the application manager
    app.add_workload(pipe)

    parser = argparse.ArgumentParser()
    parser.add_argument('--resource', help='target resource label')
    args = parser.parse_args()
    
    if args.resource != None:
        resource = args.resource
    else:
        resource = 'local.localhost'


    res_dict = {

        'xsede.stampede': {'cores': '64', 'project': 'TG-DPP160003', 'queue': 'development', 'path': '/home/vivek91/repos/exp1'},
        'xsede.comet': {'cores': '288', 'project': 'unc101', 'queue': 'compute', 'path': '/home/vivek/expanded-ensemble'}
    }

    # Create a resource handle for target machine
    res = ResourceHandle(resource=resource,
                cores=res_dict[resource]['cores'],
                username='vivek91',
                project = res_dict[resource]['project'],
                queue= res_dict[resource]['queue'],
                walltime=120,
                database_url='mongodb://rp:rp@ds055555.mlab.com:55555/db_ee4',
                access_schema='gsissh'
                )



    # Shared data
    res.shared_data = [ '{0}/PLCpep7.gro'.format(res_dict[resource]['path']),
                        '{0}/PLCpep7.ndx'.format(res_dict[resource]['path']),
                        '{0}/PLCpep7.top'.format(res_dict[resource]['path']),
                        '{0}/PLCpep7_run.mdp'.format(res_dict[resource]['path']),
                        '{0}/rand_num_gen.py'.format(res_dict[resource]['path'])
                    ]


    try:
        # Submit request for resources + wait till job becomes Active
        res.allocate(wait=True)

        # Run the given workload
        res.run(app)

    except Exception, ex:
        print 'Error, ',ex

    finally:
        # Deallocate the resource
        res.deallocate()
    
