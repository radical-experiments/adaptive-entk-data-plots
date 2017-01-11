import radical.analytics as ra
import radical.utils as ru
import pprint
import json

sid='rp.session.js-172-77.jetstream-cloud.org.vivek91.017175.0015'
src='./'
session = ra.Session(sid, 'radical.pilot', src=src)
units = session.get(etype='unit')

json_file = sid + '.json'
json = ru.read_json(json_file)

states = units[0].states.keys()

f = open('prof-%s.csv'%sid,'w')

header = 'uid, cores, executable,'
for state in states:
    header += ' ' + str(state) + ','
f.write(header +'\n')

print states

print '-----------------------------------------------------------'

for u1 in units:
    uid = u1.uid

    for u2 in json['unit']:
        if uid == u2['_id']:            
            cores = u2['description']['cores']
            executable = u2['description']['executable']
            break

    line = str(uid) + ', ' + str(cores) + ', ' + executable

    for state in states:
        print state
        line += ', ' + str(u1.states[state]['time']) 

    line = line + '\n'

    f.write(line)

f.close()

#pprint.pprint(units[0].states)
