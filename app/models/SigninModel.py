""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class SigninModel(Model):
    def __init__(self):
        super(SigninModel, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """
    def create_user(self, info):
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        errors = []
        # Some basic validation
        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 4:
            errors.append('Name must be at least 3 characters long')
        if not info['username']:
            errors.append('Username cannot be blank')
        elif len(info['username']) < 4:
            errors.append('Username must be at least 3 characters long')        
        if not info['regpassword']:
            errors.append('Password cannot be blank')
        elif len(info['regpassword']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['regpassword'] != info['regconfpassword']:
            errors.append('Password and confirmation must match!')
        if not info['date_hired']:
            errors.append('Date of hire cannot be blank')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['regpassword']
        # bcrypt is now an attribute of our model
        # we will call the bcrypt functions similarly to how we did before
        # here we use generate_password_hash() to generate an encrypted password
            username = info['username']
            user_query = "SELECT * FROM users WHERE username = :username LIMIT 1"
            query_data = { 'username': username }
            user = self.db.query_db(user_query, query_data)
            if user != []:
                errors.append("An account is already associated with that username, please login instead")
                return {"status": False, "errors": errors}
            else:
                hashed_pw = self.bcrypt.generate_password_hash(password)
                create_query = "INSERT INTO users (name, username, password, date_hired, created_at) VALUES (:name, :username, :password, :date_hired, NOW())"
                create_data = {'name': info['name'], 'username': info['username'], 'password': hashed_pw, 'date_hired': info['date_hired']}
                self.db.query_db(create_query, create_data)# Code to insert user goes here...
            # Then retrieve the last inserted user.
                get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
                users = self.db.query_db(get_user_query)
                return { "status": True, "user": users[0] } 
    def login_user(self, info): 
        errors=[]
        if not info['loginusername']:
            errors.append('Username cannot be blank')
        elif len(info['loginusername']) < 4:
            errors.append('Username must be at least 3 characters long')
        if not info['loginpassword']:
            errors.append('Password cannot be blank')
        elif len(info['loginpassword']) < 8:
            errors.append('Password must be at least 8 characters long')
        if errors:
            return {"status": False, "errors": errors}
        else:              
            user_query = "SELECT * FROM users WHERE username = :username LIMIT 1"
            user_data = {'username': info['loginusername']}
            user = self.db.query_db(user_query, user_data)
        if user:
           # check_password_hash() compares encrypted password in DB to one provided by user logging in
            if self.bcrypt.check_password_hash(user[0]['password'], info['loginpassword']):
                return {"status": True, "user": user[0]}
        errors.append('User was not found in database. Please try a different username/password combination or register instead')
        # Whether we did not find the email, or if the password did not match, either way return False
        return {"status": False, "errors": errors}  
    
    def add_item(self, item_info):
        errors = []
        # Some basic validation
        if not item_info['itemname']:
            errors.append('Item cannot be blank')
        elif len(item_info['itemname']) < 4:
            errors.append('Item name must be at least 3 characters long')
        if errors:
            return {"status": False, "errors": errors}
        else:
            item_name = item_info['itemname']
            users_id = item_info['user_id']
            add_query = "INSERT INTO items (item_name, addedby_userid, created_at) VALUES (:item_name, :addedby_userid, NOW())"
            add_data = {'item_name': item_info['itemname'], 'addedby_userid': item_info['user_id']}
            self.db.query_db(add_query, add_data)# Code to insert user goes here...
            # Then retrieve the last inserted user.
            #get_quote_query = "SELECT * FROM quotablequotes ORDER BY id DESC LIMIT 1" 
            #quotablequotes = self.db.query_db(get_quote_query)
            return { "status": True }    
    
    def add_into_user_item_status(self, item_info):
        get_items_query = "SELECT * FROM items ORDER BY id DESC LIMIT 1" 
        items = self.db.query_db(get_items_query)
        item_id=items[0]['id']
        insert_query = "INSERT INTO user_item_status(user_id, item_id, isfavorite) VALUES (:user_id, :item_id, :isfavorite)"
        insert_data = {'user_id': item_info['user_id'] , 'item_id': item_id, 'isfavorite': 1}
        self.db.query_db(insert_query, insert_data)

    def get_my_wishlist(self, user_id):
        my_wishlist_query = "SELECT user_item_status.item_id, items.item_name, items.created_at, users.name, items.addedby_userid from user_item_status join items on items.id = user_item_status.item_id join users on items.addedby_userid = users.id WHERE isfavorite = 1 and user_item_status.user_id = :user_id ORDER BY items.created_at DESC"
        my_wishlist_data = {'user_id': user_id}
        return self.db.query_db(my_wishlist_query, my_wishlist_data)

    def get_otherswishlist(self, user_id):
        my_wishlist_query = "SELECT user_item_status.item_id, items.item_name, items.created_at, users.name, items.addedby_userid from user_item_status join items on items.id = user_item_status.item_id join users on items.addedby_userid = users.id WHERE isfavorite = 1 and user_item_status.user_id != :user_id ORDER BY items.created_at DESC"
        my_wishlist_data = {'user_id': user_id}
        tempotherswishlist = self.db.query_db(my_wishlist_query, my_wishlist_data)
        my_wishlist_query = "SELECT user_item_status.item_id, items.item_name, items.created_at, users.name, items.addedby_userid from user_item_status join items on items.id = user_item_status.item_id join users on items.addedby_userid = users.id WHERE isfavorite = 1 and user_item_status.user_id = :user_id ORDER BY items.created_at DESC"
        my_wishlist_data = {'user_id': user_id}
        mywishlist =self.db.query_db(my_wishlist_query, my_wishlist_data)
        list_myitems_ids=[]
        for element in mywishlist:
            list_myitems_ids.append(element['item_id'])
        list_others_wishlist=[]
        for element in tempotherswishlist:
            if element['item_id'] not in list_myitems_ids:
                list_others_wishlist.append(element)
        return list_others_wishlist



    def addtowishlist(self, data):
        addtowishlist_query="INSERT into user_item_status (user_id, item_id, isfavorite) VALUES (:user_id, :item_id, 1)"
        self.db.query_db(addtowishlist_query, data)
        return "" 
    def removefromwishlist(self, data):
        removefromwishlist_query="UPDATE user_item_status SET isfavorite =0 WHERE (user_id=:user_id) AND (item_id=:item_id)"
        self.db.query_db(removefromwishlist_query, data)
        print 'this is remove'
        return "" 
    def delete(self, data):
        removefromdb_query="DELETE from items WHERE id=:item_id"
        removefromwishlist_query="DELETE from user_item_status WHERE item_id=:item_id"
        self.db.query_db(removefromdb_query, data)
        self.db.query_db(removefromwishlist_query, data)
        print 'this is delete'
        return "" 

    def wish_items(self,data):
        query="SELECT users.name, items.item_name from user_item_status join users on users.id=user_item_status.user_id join items on items.id=item_id where item_id=:item_id AND user_item_status.isfavorite=1"
        result=self.db.query_db(query,data)
        return result  
             


