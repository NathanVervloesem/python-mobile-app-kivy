
def get_data_difference(list_backend, list_local):
    diff = []
    diff_rem_backend = []
    diff_added_backend = []
    if list_backend != list_local:
        for item in list_backend:
            #print('looping list_backend')
            if item not in list_local:
                diff.append(item)
                diff_added_backend.append(item)
        for item in list_local:
            #print('looping list2')
            if item not in list_backend:
                diff.append(item)
                diff_rem_backend.append(item)
    else:
        print('Backend and local are identical')

    return diff, diff_rem_backend, diff_added_backend

def get_itemlist(myapp):
    ct = myapp.curr_tab
    if ct == 'Lidl':
        itemlist = myapp.rw.outputcontent1
    elif ct == 'Aldi':
        itemlist = myapp.rw.outputcontent2
    elif ct == 'Carrefour':
        itemlist = myapp.rw.outputcontent3 
    elif ct == 'Allerlei':
        itemlist = myapp.rw.outputcontent4 
    else:
        print('Error: tab not found')

    return itemlist