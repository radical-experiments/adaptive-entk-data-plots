import radical.pilot as rp
import radical.analytics as ra
import radical.utils as ru
import os 
import glob
import pprint

src = './'
json_files = glob.glob('%s/rp*.json' % src)
json_file = json_files[0]
json      = ru.read_json(json_file)
sid = os.path.basename(json_file)[:-5]

print sid

session =  ra.Session(sid, 'radical.pilot', src=src)

#print session.list()
#print session.list('uid')
#print session.get(etype='unit')



#print pnames


#print 'Printing the units:'
#units = session.get(etype='unit')
#print units

#print 'Print the pilots'
#pilots = session.get(etype='pilot')
#print pilots

unit = session.get(etype='unit', uid='unit.000000')
pprint.pprint(unit)


states = unit[0].states
pprint.pprint(states)

timestamp = unit[0].states[rp.NEW]['time']
pprint.pprint(timestamp)
