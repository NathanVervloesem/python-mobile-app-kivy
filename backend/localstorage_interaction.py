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
        Save all items to JSON file, inefficient because loop over all outputcontent list instead of checking for changes 
        but fine for now
    '''
    with open(DATA_FILE_ITEMS, "r") as f:
        items = []
        # for j in range(1, 4):
        #     outputcontent = getattr(myapp.rw, f'outputcontent{i}')
        for i in myapp.rw.outputcontent1.items:
            item = { 
                'name': str(i),
                'store': 'Lidl'
            }                 
            items.append(item)
        for i in myapp.rw.outputcontent2.items:
            item = { 
                'name': str(i),
                'store': 'Aldi'
            }                 
            items.append(item) 
        for i in myapp.rw.outputcontent3.items:
            item = { 
                'name': str(i),
                'store': 'Carrefour'
            }                 
            items.append(item)
        for i in myapp.rw.outputcontent4.items:
            item = { 
                'name': str(i),
                'store': 'Allerlei'
            }                 
            items.append(item)
    with open(DATA_FILE_ITEMS, "w") as f:
        json.dump(items, f, indent=2)
        print('Saved to local file')