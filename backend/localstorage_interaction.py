import json
from utils.data_utils import convert_expenses_data, get_expense_id, get_month


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


def add_receipt_data(myapp, data):
    with open(myapp.path_expenses,"r") as f:
        expenses = json.load(f)
        id = len(expenses) + 1
        data['id'] = id
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
        itemlist.items.insert(0, convert_expenses_data(item))
    
    itemlist.update()
 
 
def remove_item_local_expenses(myapp, text):
    '''
    Remove expenses from local file
    '''
    
    with open(myapp.path_expenses,"r") as f:
        expenses = json.load(f)

    id = get_expense_id(text)
    for expense in expenses: 
        if str(expense["id"]) == id:
            print('Found expense to remove')
            expenses.remove(expense)

    # Change id's
    for idx, expense in enumerate(expenses):
        if str(expense["id"]) > id:
           expense["id"] -= 1 
           expense_str = myapp.third_screen.expensescontent.items[idx]
           expense_str_split = expense_str.rsplit('.')
           myapp.third_screen.expensescontent.items[idx] = str(expense["id"]) + '.' +  expense_str_split[1]

    myapp.third_screen.expensescontent.update()

    with open(myapp.path_expenses, "w") as f:
        json.dump(expenses, f, indent=2)
        print('Saved expenses to local file')
    
def get_monthly_overview(myapp):
    '''
        Overview
    '''
    months = []
    items = []
    total_amount = []
    with open(myapp.path_expenses,"r") as f:
        expenses = json.load(f)

    # Build the list of months
    for expense in expenses:
        if expense['date_of_purchase'] != 'not found':
            month = get_month(expense)
            if month not in(months):
                month_split = month.rsplit('/')
                month_num = month_split[0]
                year_num = month_split[1]
                l = len(months)
                if l > 0:
                    # Insert month in correct place
                    for idx, mon in enumerate(months):
                        # print(mon)
                        mon_split = mon.rsplit('/')
                        mon_num = mon_split[0]
                        year_id = mon_split[1]
                        if year_num < year_id and idx == (l-1):
                            months.append(month) 
                            break 
                        elif year_num == year_id:
                            if month_num > mon_num: # more recent so in front
                                months.insert(idx, month)
                                break
                            elif month_num < mon_num: # less recent so behind
                                months.insert(idx+1, month)
                                break
                        elif year_num > year_id: 
                            months.insert(idx, month)
                            break
                else:
                    months.append(month)

                start_amount = 0
                total_amount.append(start_amount)

        # print(months)

    # Get the total amount per months
    if len(months) != len(total_amount):
        print('List of months has not the same length as the list of total amount.')
        # print(months)
        # print(total_amount)
        exit()

    for idx, month in enumerate(months):
        for expense in expenses:
            mon = get_month(expense)
            if month == mon:
                total_amount[idx] += float(expense['total_amount'])

    for idx, month in enumerate(months):
        data = {
            'month': month,
            'total': total_amount[idx]
        }
        items.append(data)

    #print(items)

    return items




    
  