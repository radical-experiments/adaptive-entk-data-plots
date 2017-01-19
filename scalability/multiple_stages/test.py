import radical.analytics as ra
import radical.utils as ru
import radical.pilot as rp
import pprint
import json
import glob

if __name__ == '__main__':

    tasks = 128
    cores = 256
    stages = [2,3,4,5]

    f = open('multi-stage-profiles.csv','w')
    f.write('tasks, cores, execution time\n')

    for cnt in range(len(stages)):
        src = 'stages_%s'%(stages[cnt])
        sid=glob.glob('./%s/*.json'%(src))[0].split('/')[2][:-5]
        session = ra.Session(sid, 'radical.pilot', src=src)

        units = session.get(etype='unit')

        units = session.filter(etype='unit', inplace=False)
        exec_time = units.duration(state=[rp.AGENT_EXECUTING, rp.AGENT_STAGING_OUTPUT_PENDING])
        
        f.write('%s, %s, %s\n'%(tasks, cores, exec_time))

    f.close()
