from market import app
from flask import render_template, url_for, redirect, request, flash ,get_flashed_messages, request
from market.models import Item, User
from market import db, login_manager
from market.forms import RegisterForm,LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, current_user, login_required, current_user # flask_login has many built-in functions like it stores current_user so by using jinja we will access the current user by current_user  


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    # Purchase Item Logic
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):   
                p_item_object.buy(p_item_object)
                flash(f"Congratulation! You purchased {p_item_object.name} for {p_item_object.price}$", category="success")
            else:
                flash(f"Unfortunately , You don't have enough credit to purchase {p_item_object.name}$", category = "danger")
    
    # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name = sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(sold_item)
                flash(f"You've successfully sell back the item {s_item_object.name} and you got back it's {s_item_object.price}$" , category = "success")
            else:
                flash(f"Unfortunately !! Something went wrong while selling back the item to the market .", category="danger")
                return redirect(url_for('market_page'))
            
        return redirect(url_for('market_page'))
            
            

    if request.method == "GET":
        items = Item.query.all()
        owned_items = Item.query.filter_by(owner=current_user.id) # Handles the get request : it queries the database for all the available items that are owned by the current user
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods = ['GET','POST'])
def register_page():
    form = RegisterForm()
    if request.method == "POST": 
        # At some extend level auth
        if form.validate_on_submit():
            # form here calling it for User's instance 
            user_to_create = User(username = form.username.data,
                                email_address = form.email_address.data,
                                password = form.password1.data) # here the password is the hashed passwor we get from models.py through getter 
            db.session.add(user_to_create)
            db.session.commit()  
            login_user(user_to_create)
            flash(f" You're registered succesfully {user_to_create.username}", category='success')
            return redirect(url_for('home_page'))
        
        # When we got error
        elif form.errors != {}: 
            # We will iterate over it so that if one then it's ok and if many then it will get us all the errors:
            # As it is a dict so , the values part contains the error msg
            for error_msg in form.errors.values():
                flash(f'There was an error while creating a user : {error_msg}', category='danger')
    return render_template('register.html', form=form)  

@app.route('/login',methods = ['GET','POST'])
def login_page():
    form = LoginForm() # This is the login-form class defined in models.py such that when it reaches to the /login then it will go to forms.py and check for every validations that is applied on the forms.py and then go on routes.py for further problems

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()  # username is a variable containing user name of the user and we are making it equal to the user's entered username if corrected then we will move forward    
        if attempted_user:
            if attempted_user.check_password_correction(attempted_password = form.password.data):
                login_user(attempted_user)
                flash(f"Congratulation !! You're successfully logged In {attempted_user.username}", category='success') # attempted_user contains username value so to access the current username we will write attempted_user and then fetch by .username 
                return redirect(url_for('market_page')) 
            else:
                flash("Danger !! Username Or Password is incorrect .", category='danger')
        else:
            flash(f"User not registered. Please register yourself first !!" ,category='danger')
            return redirect(url_for('register_page'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You've been logged out !! ", category="info")
    return redirect(url_for("home_page"))