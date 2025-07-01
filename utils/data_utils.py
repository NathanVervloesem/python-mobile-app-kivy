
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

def increase_amount(text):
    if text.endswith('x)'):
        splitting_str = text.rsplit(' (')
        print(f"String: {splitting_str}")

        str_amount = splitting_str[1]
        amount = str_amount.rsplit('x')
        number = int(amount[0]) + 1
        new_amount = '(' + str(number) + 'x)'

        new_text = splitting_str[0] + ' ' + new_amount
    else:
        new_text = text + ' (2x)'
        
    return new_text


def convert_expenses_data(data):
    return f'{data["id"]}. {data["merchant_name"]} {data["date_of_purchase"]} {data["total_amount"]}euro'

def get_expense_id(text):
    split_str = text.rsplit('.')
    return split_str[0]

def get_month(expense):
    text = expense["date_of_purchase"]
    split_date = text.rsplit('/')
    if len(split_date) == 3:
        return split_date[1] + '/' + split_date[2]
    else:
        print('Date of purchase not in correct format')
        return None