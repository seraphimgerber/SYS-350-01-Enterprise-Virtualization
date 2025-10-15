menu = {}
menu['1']=""
menu['2']=""
menu['3']=""
menu['4']=""
while True:
    options=menu.keys()
    options.sort()
        for entry in options:
            print entry, menu[entry]

        selection=raw_input("Please select:")
        if selection == '1':
            print ""
        elif selection == '2':
            print ""
        elif selection == '3':
            print ""
        elif selection == '4':
            break
        else:
            print "Unknown Option Selected!"