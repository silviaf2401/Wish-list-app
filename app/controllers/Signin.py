"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Signin(Controller):
    def __init__(self, action):
        super(Signin, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.
        """
        self.load_model('SigninModel')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """
        return self.load_view('main.html')

    def create(self, method ='post'):
        # gather data posted to our create method and format it to pass it to the model
        user_info = {
             "name" : request.form['name'],
             "username" : request.form['username'],
             "regemail" : request.form['regemail'],
             "regpassword" : request.form['regpassword'],
             "regconfpassword" : request.form['regconfpassword'],
             "date_hired": request.form['date_hired']
        }
        # call create_user method from model and write some logic based on the returned value
        # notice how we passed the user_info to our model method
        create_status = self.models['SigninModel'].create_user(user_info)
        if create_status['status'] == True:
            # the user should have been created in the model
            # we can set the newly-created users id and name to session
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['name']
            #session['entrypoint']= 'registered'
            # we can redirect to the users profile page here
            return redirect('/dashboard')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            # redirect to the method that renders the form
            return redirect('/main')
    def login(self, method='post'):
        user_info = {
             "loginusername" : request.form['loginusername'],
             "loginpassword" : request.form['loginpassword'],
        }
        login_status = self.models['SigninModel'].login_user(user_info)
        if login_status['status'] == True:
            session['id']=login_status['user']['id']
            session['name']= login_status['user']['name']
            return redirect('/dashboard')
        else:
            for message in login_status['errors']:
                flash(message, 'login_errors')
            # redirect to the method that renders the form
            return redirect('/main')
    
    def logoff(self):
        session.clear()
        return self.load_view('main.html')

    def dashboard(self):
        user_id=session['id']
        selfwishlist = self.models['SigninModel'].get_my_wishlist(user_id)
        otherswishlist=self.models['SigninModel'].get_otherswishlist(user_id)
        #return self.load_view('dashboard.html', selfwishlist = selfwishlist, otherswishlist=otherswishlist)
        print selfwishlist
        return self.load_view('dashboard.html', selfwishlist = selfwishlist, otherswishlist=otherswishlist)
    def add(self):
        return self.load_view('additem.html')
    def createwishlistitem(self):
        item_info = {
             "itemname" : request.form['itemname'],
             "user_id" : session['id']
        }
        additem_status = self.models['SigninModel'].add_item(item_info)
        if additem_status['status'] == True:
            ##begin test code to insert into favs table##
            insert_into_items = self.models['SigninModel'].add_into_user_item_status(item_info)
            ##end test code to insert into favs table####
            return redirect('/dashboard')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in additem_status['errors']:
                flash(message, 'item_errors')
            # redirect to the method that renders the form
            return redirect('/wish_items/create')
    def addtowishlist(self, item_id, method='post'): 
        data ={'user_id': session['id'],
                'item_id': item_id}
        self.models['SigninModel'].addtowishlist(data)
        return redirect('/dashboard')
    def removefromwishlist(self, item_id, method='post'): 
        data ={'user_id': session['id'],
                'item_id': item_id}
        self.models['SigninModel'].removefromwishlist(data)
        return redirect('/dashboard')  

    def delete(self, item_id, method ='post'):
        data ={'user_id': session['id'],
                'item_id': item_id}
        self.models['SigninModel'].delete(data)
        return redirect('/dashboard')

    def wish_items(self, item_id):
        data = {'item_id': item_id}   
        result=self.models['SigninModel'].wish_items(data)  
        return self.load_view('wish_items.html', result=result)    
      
  
   