import os, json
from pynacolada.base.display import Display

Display.log('Clean begin.')

# Clean Json files
json_files = [f for f in os.listdir() if '.json' in f]
if len(json_files) > 0:
    Display.warn('Purging {0} JSON files'.format(len(json_files)))
    for f in json_files:
        os.remove(f)

# Remove keys
#json_files = [f for f in os.listdir('config') if '.pyna' in f]
#if len(json_files) > 0:
#    Display.warn('Purging {0} Pyna Key files'.format(len(json_files)))
#    for f in json_files:
#        os.remove(f)

# Clean node list
Display.warn('Cleaning nodes.json')
with open('config/nodes.json','w') as nodelistconfig:
	json.dump({"nodes": []}, nodelistconfig)

Display.log('Clean complete.\n')
