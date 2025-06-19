import json

DATA_FILE_ITEMS = 'items.json'
DATA_FILE_CHANGES = 'changes.json'

def load_local():
    '''
        Load locally saved data
    '''
    with open(DATA_FILE_ITEMS, "r") as f:
        data = json.load(f)
        print('Loading local data')
    return data

def add_change_local(item_name, curr_tab, action):
    ''' 
        Save a change to the local changes.json
    '''
    data = { 
        'name': str(item_name),
        'store': curr_tab,
        'action': action
    }
    with open(DATA_FILE_CHANGES, "r") as f:
        changes = json.load(f)
        changes.append(data)
    with open(DATA_FILE_CHANGES, "w") as f:
        json.dump(changes, f, indent=2)
        print('Saved change to local file')


def save_local_all(myapp): 
    '''
        Save all items to JSON file.
        Inefficient because loop over all outputcontent list instead of checking for changes 
        but fine for now.
    '''
    items = []
    for i in range(1, myapp.rw.number_of_tabs+1):
        outputcontent = getattr(myapp.rw, f'outputcontent{i}')
        for j in outputcontent.items:
            item = { 
                'name': str(j),
                'store': outputcontent.label
            }                 
            items.append(item)
    with open(DATA_FILE_ITEMS, "w") as f:
        json.dump(items, f, indent=2)
        print('Saved to local file')


