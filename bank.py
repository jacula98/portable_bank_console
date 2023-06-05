from configu import startup, select_user, bank_gui, create_person, delete_person, confirmation, add_record, delete_record, update_record

# main loop


def main(last_response=None, gui=None, user_input=None, givenUser=None):
    startup()
    bank_gui(gui, user=givenUser)
    user_input = user_input
# print message if provided
    if last_response is not None:
        print(last_response)

# chosing options
    if gui is None:
        user_input = input('Decision: ')

# selecting user -> checking -> showing gui with further options
    if gui == 1 or user_input == '1':
        bank_gui(1)
        if last_response is not None:
            print(last_response)
            last_response = None
        choosen_user = input('Select user: ')
        # checking if user exist
        response = select_user(choosen_user)
        if response is False:
            main(gui=1)
        elif response == 'mainpage':
            main()
        elif response == 'user_found':
            main(gui=2, givenUser=choosen_user)
        # user not found -> show message
        elif response == 'user_not_found':
            main(last_response='No user in this name', gui=1)
        # error with checking user -> show message
        else:
            main(last_response=response, gui=1)

# adding expenses/incomes, showing history
    elif gui == 2:
        userDecision = input('Decision: ')
        if userDecision == 'q' or userDecision == 'Q':
            print('Quiting program...')
            import sys
            sys.exit(0)
        elif userDecision == 'b' or userDecision == 'B':
            main()
        elif userDecision == '1':
            recordStatus = add_record(givenUser)
            if recordStatus == 'succes':
                main(gui=3 , givenUser=givenUser, last_response=f'Added record for user {givenUser}')
            else:
                main(gui=2, last_response=recordStatus)
        elif userDecision == '2':
            main(gui=3, givenUser=givenUser)
        elif userDecision == '3':
            main(gui=4, givenUser=givenUser)
        elif userDecision == '4':
            main(gui=5, givenUser=givenUser)
        else:
            main(gui=2)


    elif gui == 3:
        decision = input('Decision: ')
        if decision == 'q' or decision == 'Q':
            print('Quiting program...')
            import sys
            sys.exit(0)
        elif decision == 'b' or decision == 'B':
            main()


    elif gui == 5:
        userDecision = input('Decision: ')
        if userDecision == 'q' or userDecision == 'Q':
            print('Quiting program...')
            import sys
            sys.exit(0)
        elif userDecision == 'b' or userDecision == 'B':
            main()
        # update record
        elif userDecision == '1':
            recordID = input('Which record(type ID) u need to change: ')
            recordStatus = update_record(recordID)
            if recordStatus == 'succes':
                main(gui=5 , givenUser=givenUser, last_response=f'Updated record {recordID}')
            else:
                main(last_response=recordStatus)
                #main(gui=2, last_response=recordStatus)
        # deleting record
        elif userDecision == '2':
            recordID = input('Which record(type ID) u need to delete: ')
            recordStatus = delete_record(recordID)
            if recordStatus == 'succes':
                main(gui=5 , givenUser=givenUser, last_response=f'Deleted record {recordID}')
            else:
                main(gui=2, last_response=recordStatus)
        else:
            main(gui=5, givenUser=givenUser)

# creating user
    elif user_input == '2':
        name = input('Username: ')
        if name == 'q' or name == 'Q':
            print('Quiting program...')
            import sys
            sys.exit(0)
        elif name == 'b' or name == 'B':
            main()
        response = create_person(name)
        if response == 'succes':
            main(last_response=f'User {name} has been created')
        else:
            main(last_response=response)

# deleting user
    elif user_input == '3':
        bank_gui(1)
        name = input('User to delete: ')
        if name == 'q' or name == 'Q':
            print('Quiting program...')
            import sys
            sys.exit(0)
        elif name == 'b' or name == 'B':
            main()
        confirm = confirmation()
        if confirm is True:
            response = delete_person(name)
            if response == 'succes':
                main(last_response=f'User {name} has been deleted')
            else:
                main(last_response=response)
        else:
            main()

# Quiting
    elif user_input == 'q' or user_input == 'Q':
        print('Quiting program...')
        import sys
        sys.exit(0)

# reload GUI
    else:
        main()


# Start loop
if __name__ == '__main__':
    main()
