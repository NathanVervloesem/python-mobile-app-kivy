
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

def get_itemlist(myapp,tab):
    # Return the itemlist for a specified tab
    if tab == 'Lidl':
        itemlist = myapp.rw.outputcontent1
    elif tab == 'Aldi':
        itemlist = myapp.rw.outputcontent2
    elif tab == 'Carrefour':
        itemlist = myapp.rw.outputcontent3 
    elif tab == 'Allerlei':
        itemlist = myapp.rw.outputcontent4 
    else:
        print('Error: tab not found')

    return itemlist

def get_input(myapp, tab):
    # Return the inputcontent for a specified tab
    if tab == 'Lidl':
        input = myapp.rw.inputcontent1
    elif tab == 'Aldi':
        input = myapp.rw.inputcontent2
    elif tab == 'Carrefour':
        input = myapp.rw.inputcontent3 
    elif tab == 'Allerlei':
        input = myapp.rw.inputcontent4 
    else:
        print('Error: tab not found')

    return input    

def convert_data(myapp, data):
    for item in data:
        itemlist = get_itemlist(myapp, item['store'])
        itemlist.items.append(item['name'])
 

def convert_data_rem(myapp, data):
    for item in data:
        itemlist = get_itemlist(myapp, item['store'])
        itemlist.items.remove(item['name'])

def update_outputcontent(myapp):
    myapp.rw.outputcontent1.update()
    myapp.rw.outputcontent2.update()
    myapp.rw.outputcontent3.update()
    myapp.rw.outputcontent4.update()