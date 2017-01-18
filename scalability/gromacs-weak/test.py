import radical.analytics as ra
import radical.utils as ru
import radical.pilot as rp
import pprint
import json
import glob

task=16


src = 'ensemble-%s-core-%s'%(task,task)
sid=glob.glob('./%s/*.json'%(src))[0].split('/')[2][:-5]
session = ra.Session(sid, 'radical.pilot', src=src)

#units = session.get(etype='unit')

'''
states = units[0].states.keys()

f = open('./%s/prof-%s.csv'%(src,sid),'w')

header = 'uid, '
for state in states:
    header += str(state) + ', '
f.write(header +'\n')

print states

print '-----------------------------------------------------------'

for u1 in units:

    line = '%s, '%(u1.uid)

    for state in states:
        line += str(u1.states[state]['time']) + ', '

    line = line + '\n'

    f.write(line)

f.close()
'''

f = open('data.txt','w')
units = session.filter(etype='unit', inplace=False)
print units.duration([rp.AGENT_EXECUTING, rp.DONE])
#pprint.pprint(units[0].states)
