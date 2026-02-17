from typing import Callable,Optional,Tuple
# user management system 
user_shema:dict = {
    'id': None,
    'first_name':'',
    'last_name':'',
    'email': '',
    'phone_number': None,
    'password' :'',
    'role':'', # Admin | User
    'is_active': False,
    'is_loggedin':False,
}

#Helper functions

#validate user info
def validate_user_info(password:Optional[str],first_name: Optional[str],last_name:Optional[str],phone_number:Optional[int])-> bool:

    '''
    Validate User Information Before Sign up
        This Function will return a boolean value
        Validating:
            password
            first name
            last name
            phone number
    '''
        #validate user info
    validate_password = check_length(8)
    validate_phone = check_length(10)
    validate_first_name = check_length(3)
    validate_last_name = check_length(3)
    if validate_password(password) and validate_first_name(first_name) and validate_phone(phone_number) and validate_last_name(last_name):
        return True
    else:
        return False
    
def generate_id(users_list:list[dict])-> int:
    '''
    Generate Id Function:
        Returns the maximum of ID
        ID will always be unique
        This Function handles an empty by setting the ID to 1
    '''
    if not users_list:
        return 1
    max_id = max(user.get('id',0) for user in users_list)

    return max_id+1


def check_length(valid_len:int)-> Callable:
    '''
    Function using currying to handle length checking for input
    return boolean for the condition
    '''
    def validate(text : str | list[str])-> bool:
        return len(text) >= valid_len
    return validate

database :list[dict] = []

# Login
def login(password: str,email:str) -> Tuple[bool,str]:
    '''
    Login Function:
        This Function will return a boolean value
        This Function will loop through the db
        This Function is only meant for Login Functionality
    '''
    logged_out_users = list(filter(lambda user: user['is_loggedin'] == False,database))

    for document in logged_out_users:
        #check if password or email is incorrect
        if password == document.get('password') and email == document.get("email"):
            document['is_loggedin'] = True 
            return True, 'Login Successful'
    return False,"Login Failed"
        
# Sign up
def signup(**user_info)-> Tuple[bool,str]:
    '''
    Sign Up Function:
        This Function will return a boolean
        This Function will make sure that the user is not created more than once
        This Function will add a new user to the database

    '''
    if not user_info:
        return False,'Empty Object'
    
    password: Optional[str] = user_info.get('password')
    email: Optional[str] = user_info.get('email') #UNIQUE
    phone_number: Optional[int] = user_info.get('phone_number')
    last_name: Optional[str] = user_info.get('last_name')
    first_name: Optional[str] = user_info.get('first_name')
    #validate user info
    if validate_user_info(password,first_name,last_name,phone_number):
        #if the user exists in the db 
        is_user_existant = [user for user in database if user['email'] == email]
        if not is_user_existant:
            user_copy = user_shema.copy()
            user_copy['email'] = email
            user_copy['password'] = password
            user_copy['phone_number'] = phone_number
            user_copy['first_name'] = first_name
            user_copy['last_name'] = last_name
            user_copy['is_active'] = True
            user_copy['id'] = generate_id(database)
            user_copy['role'] = 'User' if  database else 'Admin' # if db is empty create an admin else the rest will be regular users
            database.append(user_copy)
            return True,'Sign up successful'
        return False,'User Already Exists'
    return False,'Invalid Information'



# Log out
def logout(database:list[dict],email : str)-> Tuple[bool,str]:
    '''
    Log Out Function:
            Will update the is_loggedin state to False
            This Function returns a boolean value
    '''
    for user in database:
        if user['email'] == email:
            user['is_loggedin'] = False
            return True,'Log out successful'
    return False,'Log out failed'
        

# Block/Unblock
def block_unblock(user_id:int,admin_id:int)-> Tuple[bool,str]:
    '''
    Block/Unblock ADMIN Function:
            This Function will block user if not blocked
            This Function will unblock user if blocked
            This Function will return a boolean value
    '''
    if database[0].get('id') != admin_id:
        return False,'Unauthorized Access!'
    
    for user in database:
        if user['id'] == user_id:
            user['is_active'] = not user['is_active']
            return True,f'User account is {'Active' if user["is_active"] else 'Frozen'}'
    return False,'Change State Failed, possibly user does not exist'

# Is logged in
def is_loggedin(database :list[dict],user_id:int)-> Tuple[bool,str]:
    '''
    Is Logged In Function:
            This Function Will Only Check If The User Is logged in or not
            This Function will return a boolean value
    '''
    for user in database:
        if user['id'] == user_id:
            if user['is_loggedin']:
                return True,'User Logged In'
            else:
                return False,'User Is Logged Out'
    return False,'Log Out Check Failed, possibly user does not exist'



# Get User by ID
def get_user_by_id(database: list[dict],user_id:int)->dict|None:
    '''
    Function Get User By ID:
        This Function will return a dict if user is found
        This Function will return None if user is not found

    '''
    matches = list(filter(lambda u: u["id"] == user_id, database))
    return matches[0] if matches else None




# Update user info
def update_user(database: list[dict],user_id:int,admin_id:int, **kwargs)-> Tuple[bool,str]:

    '''
    Update User ADMIN Function:
        This Function will use get_user_by_id()
        This Function will update the user if found
        This Function will indicate the result by returning a boolean value
    '''
    if database[0].get('id') != admin_id:
        return False,'Unauthorized Access!'

    user = get_user_by_id(database,user_id)
    if user:
        user.update(kwargs)
        return True,'User Updated with success'
    return False,'Update User Failed, possibly user does not exist'

#Remove User by ID
def remove_user(database: list[dict], user_id: int,admin_id:int) -> Tuple[bool,str]:
    '''
    ADMIN Function Remove User:
        This Function Will Verify the caller if Admin
            If YES this function will delete the user from the db and return True
            Else this function will return False
    '''
    if database[0].get('id') != admin_id:
        return False,'Unauthorized Access!'
    
    for i, user in enumerate(database):
        if user['id'] == user_id:
            database.pop(i)
            return True,'User was removed successfuly'
        
    return False,'Failed to remove user, possibly user does not exist'

# main 
def main():
    print("\n===== USER MANAGEMENT SYSTEM =====")
    print("Available options:")
    print("1. Sign Up")
    print("2. Log In")
    print("3. Log Out")
    print("4. Block/Unblock User (Admin only)")
    print("5. Check if Logged In")
    print("6. Get User by ID")
    print("7. Update User Info (Admin only)")
    print("8. Remove User (Admin only)")
    print("9. Exit")

    choice = input("Enter your choice (1-9): ").strip()

    if choice == '1':
        # Sign up
        print("Enter sign-up details:")
        email = input("Email: ")
        password = input("Password (minimum:8): ")
        phone = input("Phone number (10 digits): ")
        first = input("First name (minimum:3): ")
        last = input("Last name (minimum:3): ")
        success, msg = signup(
            email=email,
            password=password,
            phone_number=phone,
            first_name=first,
            last_name=last
        )
        print(msg)

    elif choice == '2':
        # Log in
        email = input("Email: ")
        password = input("Password: ")
        success, msg = login(password, email)

        print(msg)

    elif choice == '3':
        # Log out
        email = input("Enter email to log out: ")
        success, msg = logout(database, email)
        print(msg)

    elif choice == '4':
        # Block/Unblock
        admin_id = int(input("Enter your Admin ID: "))
        user_id = int(input("Enter User ID to toggle block status: "))
        success, msg = block_unblock(user_id, admin_id)
        print(msg)

    elif choice == '5':
        # Is Logged In
        user_id = int(input("Enter User ID to check login status: "))
        success, msg = is_loggedin(database, user_id)
        print(msg)

    elif choice == '6':
        # Get User by ID
        user_id = int(input("Enter User ID: "))
        user = get_user_by_id(database, user_id)
        print("User found:" if user else "User not found.")
        if user:
            print(user)

    elif choice == '7':
        # Update user info
        admin_id = int(input("Admin ID: "))
        user_id = int(input("User ID to update: "))
        print("Leave field blank to skip it.")
        new_email = input("New Email: ").strip()
        new_phone = input("New Phone Number: ").strip()
        updates = {}
        if new_email:
            updates['email'] = new_email
        if new_phone:
            updates['phone_number'] = new_phone
        success, msg = update_user(database, user_id, admin_id, **updates)
        print(msg)

    elif choice == '8':
        # Remove User
        admin_id = int(input("Admin ID: "))
        user_id = int(input("User ID to remove: "))
        success, msg = remove_user(database, user_id, admin_id)
        print(msg)

    elif choice == '9':
        print("Exiting program...")
        return

    else:
        print("Invalid choice. Please try again.")

    # Recursive call to continue the loop
    main()

# Call the main function
main()