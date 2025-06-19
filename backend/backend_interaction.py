import requests


def remove_item_in_backend(myapp, curr_tab, item_name):
    # Try to communicate with backend
    if  myapp.rw.ids.connection_status.connected:
        
        try:
            url = myapp.url + "items/remove"
            response = requests.post(url, json={"name": item_name, "store": curr_tab})
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)
        finally:
            
            # Save changes locally
            myapp.rw.save_local_all()

    else:
        myapp.rw.add_change_local(item_name,curr_tab,'remove')

def add_to_backend(myapp, ct, item_name):
    # Adding an item to the backend if possible, 
    url = myapp.url + "items/add"
    data = { 
        'name': str(item_name),
        'store': ct
        }
    if myapp.rw.ids.connection_status.connected:
        try:
            response = requests.post(url, json=data)
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)
        finally:
            # pass
            # Save locally
            myapp.rw.save_local_all()
    else:
        myapp.rw.add_change_local(item_name,ct,'add')

def clear_tab_backend(myapp, ct):
    if myapp.rw.ids.connection_status.connected:
        try:
            url = myapp.url + "items/clear_tab"
            response = requests.post(url, json={"name": "item", "store": ct})
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)   
        finally:
            # Save locally
            myapp.rw.save_local_all()

    else:
        myapp.rw.add_change_local('',ct,'remove tab')