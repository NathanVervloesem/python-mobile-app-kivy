import json
from utils.data_utils import convert_expenses_data


def load_local(myapp):
    '''
        Load locally saved data
    '''
    with open(myapp.path_items, "r") as f:
        data = json.load(f)
        print('Loading local data')
    return data

def add_change_local(myapp, item_name, curr_tab, action,new_name=None):
    ''' 
        Save a change to the local changes.json
    '''
    if action == 'replace':
        data = { 
            'name': str(item_name),
            'store': curr_tab,
            'action': action,
            'new_name': new_name
        }
    else:
        data = { 
            'name': str(item_name),
            'store': curr_tab,
            'action': action
        }
    with open(myapp.path_changes, "r") as f:
        changes = json.load(f)
        changes.append(data)
    with open(myapp.path_changes, "w") as f:
        json.dump(changes, f, indent=2)
        print('Saved change to local file')


def save_local_all(myapp): 
    '''
        Save all items to JSON file.
        Inefficient in most cases because loops over all outputcontent list instead of checking for changes 
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
    with open(myapp.path_items, "w") as f:
        json.dump(items, f, indent=2)
        print('Saved to local file')


def load_local_cart(myapp):
    '''
        Load locally saved data
    '''
    with open(myapp.path_cart, "r") as f:
        data = json.load(f)
        print('Loading local cart data')

    # Convert
    itemlist = myapp.second_screen.outputcontent
    for item in data:
        itemlist.items.append(item['name'])
    
    itemlist.update()


def add_to_local_cart(myapp,item_name):
    data = {
        'name': item_name
        }
    with open(myapp.path_cart,"r") as f: 
        items = json.load(f)        
        items.append(data)
    with open(myapp.path_cart, "w") as f:
        json.dump(items, f, indent=2)
        print('Saved to cart file')  

def clear_local_cart(myapp):
    with open(myapp.path_cart, "w") as f:
        json.dump([], f)
        print('Clear cart')   



def save_receipt_data(myapp, data):
    with open(myapp.path_expenses,"r") as f:
        expenses = json.load(f)
        expenses.append(data)
    with open(myapp.path_expenses, "w") as f:
        json.dump(expenses, f, indent=2)
        print('Saved expenses to local file')


def load_local_expenses(myapp):
    '''
    Load local expenses from expenses file
    '''
    with open(myapp.path_expenses, "r") as f:
        data = json.load(f)
        print('Loading local cart data')

    # Convert
    itemlist = myapp.third_screen.expensescontent
    for item in data:
        itemlist.items.append(convert_expenses_data(item))
    
    itemlist.update()
