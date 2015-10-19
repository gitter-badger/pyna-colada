import os, json
from pynacolada.base.display import Display

display = Display()
display.log('Clean begin.')

# Clean Json files
json_files = [f for f in os.listdir() if '.json' in f]
if len(json_files) > 0:
    display.warn('Purging {0} JSON files'.format(len(json_files)))
    for f in json_files:
        os.remove(f)

# Clean node list
display.warn('Cleaning nodes.json')
with open('config/nodes.json','w') as nodelistconfig:
	json.dump({"nodes": []}, nodelistconfig)

display.log('Clean complete.\n')
