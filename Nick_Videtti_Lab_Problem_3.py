print('\n'+'PROBLEM 1:'+'\n'+'Write a Python function to multiply all the numbers in a list.'+'\n')
print('List1 = [-7,3,2,1,5,6,7,9,2,3,-77]')
print('List2 = [-7,3,2,1,5,6,7,9,2,3,-77,0,3,4,2,1,1,1,3,2,1,-87654]')
print('List3 = [1,1,1,1,1,1,1,1,1,1,2.8]')
print('List4 = [1,"string",3]')
print('\n'+'The function below will return the product of all items in a list.')
print('def multiply_list(list):'+'\n'+'    '+'returnval = 1'+'\n'+'    '+'count = 0'+'\n'+'    '+'for item in list:')
print('        '+'if str(item).isnumeric(): returnval *= item;    count += 1'+'\n'+'        '+'else:')
print('            '+"print('Invalid argument. \"list\" argument in multiply_list(list) must be a list with all numeric items.')")
print('            '+'break'+'\n'+'    '+'if count == len(list): return returnval')
def multiply_list(list):
    returnval = 1
    count = 0
    for item in list:
        if type(item) == int or type(item) == float:
            returnval *= item
            count += 1
    if count == len(list): return returnval
    else: return 'Invalid argument. "list" argument in multiply_list(list) must be a list with all numeric items.'
List1 = [-7,3,2,1,5,6,7,9,2,3,-77]
List2 = [-7,3,2,1,5,6,7,9,2,3,-77,0,3,4,2,1,1,1,3,2,1,-87654]
List3 = [1,1,1,1,1,1,1,1,1,1,2.8]
List4 = [1,"string",3]
print('\n'+'multiply_list(List1):', multiply_list(List1))
print('\n'+'multiply_list(List2):', multiply_list(List2))
print('\n'+'multiply_list(List3):', multiply_list(List3))
print('\n'+'multiply_list(List4):', multiply_list(List4)+'\n')

print('\n'+'PROBLEM 2:'+'\n'+'Write a Python function that accepts a string and calculate the number of upper case letters and lower case letters. '+'\n')
print("String1 = 'teststring'")
print("String2 = 'UPPERlower'")
print("String3 = 'ALLUPPERSOHBOY'")
print("String4 = 103"+'\n')
String1 = 'teststring'
String2 = 'UPPERlower'
String3 = 'ALLUPPERSOHBOY'
String4 = 103
print('The following function will count the number of upper case and lower case letters in a string.')
print('def case_counts(string):')
print('    '+'lowercount = 0'+'\n'+'    '+'uppercount = 0'+'\n'+'    '+'if type(string) == str:')
print('        '+'for letter in string:'+'\n'+'            '+'if letter.islower(): lowercount += 1')
print('            '+'if letter.isupper(): uppercount += 1'+'\n'+'        '+"print('Total Letters:', len(string))")
print('        '+"print('Uppercase Letters:', uppercount)"+'\n'+'        '+"print('Lowercase Letters:', lowercount)")
print('    '+'else:'+'\n'+'        '+"print('That isn\'t a string! That\'s a', str(type(string))+'!', 'Please enter a string instead.')")
def case_counts(string):
    lowercount = 0
    uppercount = 0
    if type(string) == str:
        for letter in string:
            if letter.islower(): lowercount += 1
            if letter.isupper(): uppercount += 1
        print('Total Letters:', len(string))
        print('Uppercase Letters:', uppercount)
        print('Lowercase Letters:', lowercount)
    else:
        print('That isn\'t a string! That\'s a', str(type(string))+'!', 'Please enter a string instead.')
print('\n'+'case_counts(String1):') 
case_counts(String1)
print('\n'+'case_counts(String2):')
case_counts(String2)
print('\n'+'case_counts(String3):')
case_counts(String3)
print('\n'+'case_counts(String4):')
case_counts(String4)
print()