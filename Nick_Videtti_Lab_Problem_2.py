'''Dictionaries: You may wish to write the code for parts a–d in one Python file.
Consider the following two dictionaries: 

stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15}
prices = {"banana": 4, "apple": 2, "orange": 1.5, "pear": 3}'''

'''a. Show the expression that gets the value of the stock dictionary at the key ‘orange’. Show a
statement that adds an item to the stock dictionary called ‘cherry’ with some integer value
and that adds ‘cherry’ to the prices dictionary with a numeric value. (Or pick your own fruit
name.)'''

stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15}
print('\n'+'stock:', str(stock))
print('\n'+'PART A'+'\n'+"The expression that gets the value of the stock dictionary at the key ‘orange’ is stock['orange'].")
print("stock['orange'] =", str(stock['orange'])+'\n')
print("The following statement will add an item to the stock dictionary called ‘cherry’ with some integer value and that adds ‘cherry’ to the prices dictionary with a numeric value:")
print("stock['cherry'] = 2")
stock['cherry'] = 2
print('\n'+'Now let\'s check our results...'+'\n'+'print(stock): '+str(stock)+'\n'+'Looks good!'+'\n')



#b. Write the code for a loop that iterates over the stock dictionary and prints each key and value.
print('\n'+'PART B')
print('This code will loop through each key in the stock dictionary and then print that key with its corresponding value.')
print('for item in stock:'+'\n'+'    '+"print(item+': '+str(stock[item]))"+'\n')
for item in stock:
    print(item+': '+str(stock[item]))



'''c. Suppose that we have a list:
groceries = [‘apple’, ‘banana’, ‘pear’]
Write the code that will sum the total number in stock of the items in the groceries list.'''

print('\n'+'\n'+'PART C'+'\n'+'This code will sum the total number in stock of the items in the groceries list.'+'\n')
print("Given groceries = [‘apple’, ‘banana’, ‘pear’], the code would be:")
print('stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15, "cherry": 2}'+'\n'+"groceries = ['apple', 'banana', 'pear']"+'\n'+'total_in_stock = 0')
print('for grocery in stock:'+'\n'+'    '+'if grocery in groceries: total_in_stock += stock[grocery]'+'\n'+'print(total_in_stock)'+'\n')
print('Let\'s test it out...'+'\n'+'total_in_stock:')
stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15, "cherry": 2}
groceries = ['apple', 'banana', 'pear']
total_in_stock = 0
for grocery in stock:
    if grocery in groceries: total_in_stock += stock[grocery]
print(total_in_stock)
print('\n'+'Looks good!'+'\n'+'\n')



'''d. Write the code that can print out the total value in stock of all the items. This program can
iterate over the stock dictionary and for each item multiply the number in stock times the price
of that item in the prices dictionary. (This can include the items for ‘cherry’ or not, as you
choose.) '''

print('PART D'+'\n'+'Total value in stock of all items:'+'')
stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15, "cherry": 2}
prices = {"banana": 4, "apple": 2, "orange": 1.5, "pear": 3, "cherry": 5}
total_value = 0
for item in stock:
    total_value += prices[item]*stock[item]
print('$'+'%.2f' % total_value)
print('\n'+'Code Used:')
print('stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15, "cherry": 2}'+'\n'+'prices = {"banana": 4, "apple": 2, "orange": 1.5, "pear": 3, "cherry": 5}')
print('total_value = 0'+'\n'+'for item in stock:'+'\n'+'    '+'total_value += prices[item]*stock[item]'+'\n'+"print('$'+'%.2f' % total_value))"+'\n')