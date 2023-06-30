# This program reads a file and prints the lines and creates a list of items on the line


# open the file for reading (in the same directory as the program)

NBAfile = open ('C:/Users/nvidetti/Downloads/NBA-Attendance-1989.txt', 'r')


# iterate over the lines of the file and count the number of lines

count = 0

NBAlist = [ ]

for line in NBAfile:

    # increment adds one to the count variable

    count += 1

    # strip the newline at the end of the line (and other white space from ends)

    textline = line.strip()

    # split the line on whitespace

    items = textline.split()

    # add the list of items to the NBAlist
    
    NBAlist.append(items)
# print the number of teams read

print('Number of teams:', count)


# print the lines from the list

for line in NBAlist:
    print ('The attendance at', line[0], 'was', line[1], 'and the ticket price was $' + line[2] + '.')


NBAfile.close()
