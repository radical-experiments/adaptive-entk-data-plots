import radical.analytics as ra
import radical.utils as ru
import radical.pilot as rp
import pprint
import json
import glob

if __name__ == '__main__':

    tasks=2048
    cores=[256,512,1024,2048,4096]

    f = open('strong-profiles.csv','w')
    f.write('tasks, cores, execution time\n')

    for cnt in range(len(cores)):
        src = 'set_t2048_c%s'%(cores[cnt])
        sid=glob.glob('./%s/*.json'%(src))[0].split('/')[2][:-5]
        session = ra.Session(sid, 'radical.pilot', src=src)

        units = session.get(etype='unit')

        units = session.filter(etype='unit', inplace=False)
        exec_time = units.duration(state=[rp.AGENT_EXECUTING, rp.AGENT_STAGING_OUTPUT_PENDING])
        
        f.write('%s, %s, %s\n'%(tasks, cores[cnt], exec_time))

    f.close()
