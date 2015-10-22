import os, json
from pyna.base.Display import Display

Display.log('Clean begin.')

# Clean Json files
json_files = [f for f in os.listdir() if '.json' in f]
if len(json_files) > 0:
    Display.warn('Purging {0} JSON files'.format(len(json_files)))
    for f in json_files:
        os.remove(f)

# Remove keys
json_files = [f for f in os.listdir('config/keys/') if '.pyna' in f]
if len(json_files) > 0:
    Display.warn('Purging {0} Pyna Key files'.format(len(json_files)))
    for f in json_files:
        os.remove('config/keys/{0}'.format(f))

# Clean node list
Display.warn('Cleaning nodes.json')
with open('config/nodes.json','w') as nodelistconfig:
	json.dump({"nodes": []}, nodelistconfig)

# Clean users list
Display.warn('Cleaning users.json')
with open('config/users.json','w') as users:
	json.dump({}, users)

# Clean log
Display.warn('Cleaning log file')
try:
    os.remove('log.log')
except: pass

Display.log('Clean complete.\n')
