import requests
from backend.localstorage_interaction import add_change_local, save_local_all


def do_post_request(myapp, url, data):
    '''
        Do post request and save locally
    '''
    try:
        response = requests.post(url, json=data)
        print("Server response:", response.json())
    except Exception as e:
        print("Error sending data:", e)
    finally:
        # Save changes locally
        save_local_all(myapp)    

def remove_item_in_backend(myapp, curr_tab, item_name):
    '''
       Remove an item from the backend
    '''
    if  myapp.rw.ids.connection_status.connected:
        url = myapp.url + "items/remove"
        data = {
            "name": item_name,
            "store": curr_tab
        }
        do_post_request(myapp, url, data)
    else:
        add_change_local(item_name,curr_tab,'remove')

def add_to_backend(myapp, ct, item_name):
    '''
        Adding an item to the backend if possible
    ''' 
    if myapp.rw.ids.connection_status.connected:
        url = myapp.url + "items/add"
        data = { 
            "name": str(item_name),
            "store": ct
        }
        do_post_request(myapp, url, data)
    else:
        add_change_local(item_name,ct,'add')

def clear_tab_backend(myapp, ct):
    '''
        Clear a complete tab in the backend
    '''
    if myapp.rw.ids.connection_status.connected:
        url = myapp.url + "items/clear_tab"
        data = {
            "name": "item",
            "store": ct
        }
        do_post_request(myapp, url, data)
    else:
        add_change_local('',ct,'remove tab')