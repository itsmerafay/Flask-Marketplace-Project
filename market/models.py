from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin, current_user # it will provide some powerful built-in methods 

# login_manager # is used to tell Flask-Login how to load a user object from the database based on the user ID stored in the session . This decorator should be applied to a function that accepts a user_id as an argument and returns a user object.
# The load_user function that you've shown is the function that you define to be used as the user loader. It's used to retrieve a user object from the database based on the provided user_id. The function should query the database and return the corresponding user object.
# When a user logs in, Flask-Login stores the user ID in the session. When you need to access the current user, Flask-Login uses the load_user function to retrieve the user object based on the stored user ID. This enables you to access the current user's data in a convenient and secure manner throughout your application
@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    email_address = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(60), nullable = False)
    budget = db.Column(db.Integer(), nullable = False, default = 1000)

    @property # get
    def prettier_budget(self):
        magnitude = len(str(self.budget)) # 1000
    
        if magnitude >= 7:  # Million or greater
            return f"{self.budget // 1000000} million $"
        elif magnitude >= 4:  # Thousand or greater
            formatted_budget = f"{self.budget:,}"  # Use Python's built-in comma formatting
            return f"{formatted_budget} $"
        else:
            return f"{self.budget}$"
    # Backref : Back-referrence to tha

    # Backref : Back-referrence to that user model.
    # In the scenario we've to check an iphone item and it's own user so we'll grap the item object and access it by the attr of owned user . It will allow us to check the owner of the specific item 
    # lazy = True, bcz without this, the sqlalchemy won't recognize all the objects of items 
    
    items = db.relationship('Item', backref = 'owned_user', lazy = True) 

# Using getter and setter function 
# In Python, getters and setters are methods used to control access to class attributes, providing a way to encapsulate and manage attribute access and modification. 
# A getter is a method that's used to retrieve the value of an attribute. It provides controlled access to the attribute by performing additional actions or validations before returning the value. Getters are often used to implement computed properties or to ensure that the returned value adheres to certain rules.

# @property decorator to define a getter for the password attribute. However, the attribute you're getting is actually password_hash.

    @property # getter
    def password(self):
        return self.password

# The @password.setter method is a setter method associated with the password attribute. When you assign a value to user.password, this setter method is invoked. It receives the plain-text password as an argument, performs the hashing using bcrypt, and then stores the hashed value in the password_hash attribute.
# In contrast, the getter method is defined using @property to provide access to the value of the password_hash attribute. This getter method is unrelated to the setter method. It allows you to access the hashed password value using the user.password syntax.
    @password.setter # setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password)

# It means that self.password_hash is first checked by setter fn and then it checks the password_hash with the attempted_user
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password) # If we use if condition then it will return true or false so we make it return fn so that in routes we can call it out
    

    def can_purchase(self,item_obj): # boolean value
        return self.budget>=item_obj.price # will return true or false

    # If this item_obj is in the items (db) 

    def can_sell(self,item_obj):
        return item_obj in self.items # return boolean

# A relationship of one to many is maintained between the user and the items. 

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True)
    price = db.Column(db.Integer(), nullable = False)
    barcode = db.Column(db.String(12), nullable = False, unique = True )
    description = db.Column(db.String(1024),nullable = False, unique = True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    
    
    # use for displaying the meaningful info about the object 
    # returns a formatted string that includes the name of the item.

    def __repr__(self):
        return f"Item : {self.name}"

    def can_sell():
        pass

    def buy(self,item_obj):
        self.owner = current_user.id
        current_user.budget -= self.price
        db.session.commit() 
    
    def sell(self,item_obj):
        self.owner = None # make ownership to none
        current_user.budget += self.price
        db.session.commit()