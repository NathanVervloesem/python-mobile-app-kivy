
def get_data_difference(list_backend, list_local):
    '''
        Get difference in backend and local data to proper updates
    '''
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
    ''' 
        Return the itemlist for a specified tab
    '''
    for i in range(1, myapp.rw.number_of_tabs+1):
        outputcontent = getattr(myapp.rw, f'outputcontent{i}')
        if tab == outputcontent.label:
            return outputcontent
    return None

def get_input(myapp, tab):
    '''
      Return the inputcontent for a specified tab
    '''
    print(f'Tab: {tab}')
    for i in range(1, myapp.rw.number_of_tabs+1):
        outputcontent = getattr(myapp.rw, f'outputcontent{i}')
        print(f'Test label: {outputcontent.label}')
        if tab == outputcontent.label:
            print(f'Test succeeded for {tab}')
            return getattr(myapp.rw, f'inputcontent{i}')
    print('Return none')
    return None    

def convert_data(myapp, data):
    for item in data:
        itemlist = get_itemlist(myapp, item['store'])
        itemlist.items.append(item['name'])
 

def convert_data_rem(myapp, data):
    for item in data:
        itemlist = get_itemlist(myapp, item['store'])
        itemlist.items.remove(item['name'])

def update_outputcontent(myapp):
    for i in range(1, myapp.rw.number_of_tabs+1):
        outputcontent = getattr(myapp.rw, f'outputcontent{i}')
        outputcontent.update()
