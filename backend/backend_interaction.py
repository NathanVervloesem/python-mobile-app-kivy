import requests
import json
from backend.localstorage_interaction import add_change_local, save_local_all, load_local
from utils.data_utils import get_data_difference, convert_data, convert_data_rem, update_outputcontent

def do_post_request(myapp, url, data):
    '''
        Do post request and save locally
    '''
    try:
        print(f'Do_post_request data:{data}')
        response = requests.post(url, json=data)
        print("Server response:", response)
        print("Server response.json():", response.json())
    except Exception as e:
        print("Error sending data:", e)
    finally:
        # Save changes locally
        save_local_all(myapp)    

def load_items(myapp):
    '''
        Load items. First try from the backend, if that doesn't work load local data. At latest display the items.
    '''

    # Doing check on outputcontent
    if not myapp.rw.outputcontent1:
        print("WARNING: outputcontent1 is None — probably called too early.")

    # GET from backend
    url = myapp.url + "items/"
    
    # Try to request data from backend
    try:
        response = requests.get(url)
        #print(f'Load items response: {response}')

        try:
            # Get the data from json
            data = response.json()
            #print(f'Data from response {data}') # for backend testing

            # If decoding error, load locally
            data_local = load_local(myapp)

            # Get the difference 
            data, data_rem_backend, data_added_backend = get_data_difference(data, data_local)
                
        except Exception as e:
            print(f"JSON decode error: {e}")

            # If decoding error, load locally
            data = load_local(myapp)

            # not comparison with local data is needed
            data_rem_backend = []
            data_added_backend = []


        finally:

            # Get the data in the correct format
            convert_data_rem(myapp, data_rem_backend)
            convert_data(myapp, data_added_backend,)
                    
            # update
            update_outputcontent(myapp)

            # Save locally 
            save_local_all(myapp)
                    
        
    except Exception as e:
        print(f"Error Unexpected status code: {e}")

        # If connection error, load locally
        data = load_local(myapp)

        # No comparison needed because only local data available

        # Convert data
        convert_data(myapp, data)

        # update display
        update_outputcontent(myapp)


def replace_item_in_backend(myapp, curr_tab, item_name, new_name):
    '''
        Change item name in the backend
    '''

    if hasattr(myapp.rw.ids.connection_status, 'connected'):
        if  myapp.rw.ids.connection_status.connected:
            url = myapp.url + "items/replace"
            data = {
                "name": item_name,
                "store": curr_tab,
                "new_name": new_name
            }                    
            try:
                print(f'Do_put_request data:{data}')
                response = requests.put(url, json=data)
                print("Server response:", response)
                print("Server response.json():", response.json())
            except Exception as e:
                print("Error sending data:", e)
            finally:
                # Save changes locally
                save_local_all(myapp)
        else:
            add_change_local(myapp, item_name,curr_tab,'replace',new_name)
    else:
        add_change_local(myapp, item_name,curr_tab,'replace',new_name)


def remove_item_in_backend(myapp, curr_tab, item_name):
    '''
       Remove an item from the backend
    '''
    if hasattr(myapp.rw.ids.connection_status, 'connected'):
        if  myapp.rw.ids.connection_status.connected:
            url = myapp.url + "items/remove"
            data = {
                "name": item_name,
                "store": curr_tab
            }
            do_post_request(myapp, url, data)
        else:
            add_change_local(myapp, item_name,curr_tab,'remove')
    else:
        add_change_local(myapp, item_name,curr_tab,'remove')


def add_to_backend(myapp, ct, item_name):
    '''
        Adding an item to the backend if possible
    '''
    if hasattr(myapp.rw.ids.connection_status, 'connected'): 
        if myapp.rw.ids.connection_status.connected:
            url = myapp.url + "items/add"
            data = { 
                "name": str(item_name),
                "store": ct
            }
            do_post_request(myapp, url, data)
        else:
            add_change_local(myapp, item_name, ct, 'add')
    else:
        add_change_local(myapp, item_name, ct, 'add')       

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
        add_change_local(myapp, '',ct,'remove tab')


def deploy_changes(myapp,changes):
    '''
        Changes to item store in changes.json are deployed to the backend
    '''
    for change in changes:
        action = change['action']
        if action == 'remove':
            remove_item_in_backend(myapp, change['store'], change['name'])
        elif action == 'add':
            add_to_backend(myapp, change['store'], change['name'])
        elif action == 'remove tab':
            clear_tab_backend(myapp, change['store'])
        elif action == 'replace':
            replace_item_in_backend(myapp, change['store'], change['name'], change['new_name'])
        else:
            print(f'Action {action} unknown')

def deploy_changes_wrapper(myapp):
    '''
        Wrapper for function deploy_changes where the changes.json is read and cleared.
    '''
    with open(myapp.path_changes, "r") as f:
        # Load changes
        changes = json.load(f)
        if len(changes) == 0:
            #print('No changes')
            pass
        else:
            # Deploy changes
            deploy_changes(myapp, changes)
        
            # When all changes are deployed, clear the json file
            with open(myapp.path_changes, "w") as f:
                json.dump([], f)