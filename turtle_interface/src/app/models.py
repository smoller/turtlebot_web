import os
import json

from config import basedir

tour_path = os.path.join(basedir, 'assets/')

class Tour:
    def __init__(self, name):
        self.name = name
        self._file = os.path.join(tour_path, '{}.json'.format(self.name))

    def load_tour(self):
        with open(self._file, 'r') as f:
            return json.load(f)
        return None

    def save_tour(self, data):
        print 'Tour saved: {}'.format(self.name)
        for i, wp in enumerate(data['waypoints']):
            wp.update({'id':i})
        with open(self._file, 'wt') as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

def get_tour_list():
    return [name for name, ext in map(os.path.splitext, os.listdir(tour_path)) if ext == '.json']
