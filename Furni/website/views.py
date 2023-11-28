from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from .forms import RegisterForm, LoginForm
from .models import Users, Furni, Cart
from website import db, bcrypt, login_manager, login_user, current_user, login_required, logout_user, app



views = Blueprint('views', __name__)
login_manager.login_view="login"


@login_required
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@views.route('/')
def base():
   
    return render_template("base.html", current_user=current_user)
 


@views.route('/login', methods=['GET', 'POST'])
def login():
    Regform = RegisterForm()
    Logform = LoginForm()
    
   
    if Regform.validate_on_submit():
        name = Regform.name.data
        email = Regform.email.data
        H_password = bcrypt.generate_password_hash(Regform.password.data)
    
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email address already exists")
            return redirect(url_for("views.login"))
        else:
            register = Users(name=name, email=email, password=H_password)
            db.session.add(register)
            db.session.commit()
            flash("Login with registered email and password")
            return redirect(url_for("views.login"))
                

    if Logform.validate_on_submit():
        
        email=Logform.email.data
        password=Logform.password.data
        user_exists = Users.query.filter_by(email=email).first()

        if user_exists:
            if bcrypt.check_password_hash(user_exists.password, password):
                login_user(user_exists)
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password. Try Again")
                return redirect(url_for("views.login"))
        else:
            flash("User not found. Please register")
            return redirect(url_for("views.login"))
    
    return render_template("login.html", Rform=Regform, Lform=Logform)


@views.route('/home', methods=['GET', 'POST'])
def home():
    items = Furni.query.all()
    return render_template("home.html", items=items)

@views.route('/account', methods=['GET', 'POST'])
def account():
    return render_template("account.html", current_user=current_user)

@views.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))


@views.route('/shop')
def shop():
    items = Furni.query.all()
    return render_template("shop.html", items=items)

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/services')
def services():
    return render_template("services.html")

@views.route('/blog')
def blog():
    return render_template("blog.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")




@views.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items=Cart.query.all()
    total_price = sum(item.price*item.item_stock for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)



@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    data = request.get_json()

    # Extract item information from the request
    # item_id = data.get('id')
    item_name = data.get('name')
    item_price = data.get('price')
    item_image = data.get('image')
    item_quantity = 1
    
    existing_item = Cart.query.filter_by(name=item_name).first()
    if existing_item:
        # If the item is already in the cart, increment the quantity
        existing_item.item_stock += 1
    else:
        # If the item is not in the cart, add a new item
        cart_item = Cart(name=item_name, price=item_price, image_path=item_image, item_stock=item_quantity)
        db.session.add(cart_item)

    db.session.commit()

    
    # Return a response (you can customize the response format)
    response = {'message': 'Item added to cart successfully'}
    return jsonify(response)


@app.route('/remove_from_cart', methods=['GET','POST'])
def remove_from_cart():
    data = request.get_json()
    
    item_id = data.get('id')
    item_to_remove = Cart.query.get(item_id)

    if item_to_remove:
        db.session.delete(item_to_remove)
        db.session.commit()
        response = {'message': 'Item removed from cart successfully'}
    else:
        response = {'message': 'Item not found in the cart'}

    return jsonify(response)


@views.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/update_item_stock', methods=['GET','POST'])
def update_item_stock():
    
    data = request.get_json()
    
    item_id = data.get('id')
    item_stock = data.get('new_stock')
    
    item = Cart.query.get(item_id)
    item.item_stock = item_stock
    db.session.commit()
    
    response = {'message': 'Item stock updated successfully'}
    return jsonify(response)

# For total and subtotal values
@app.route('/get_cart_totals', methods=['GET'])
def get_cart_totals():
    # Calculate the updated cart totals
    cart_items = Cart.query.all()
    subtotal = sum(item.price * item.item_stock for item in cart_items)
    total = subtotal  # For simplicity, you can update this logic based on your requirements

    return jsonify({'subtotal': subtotal, 'total': total})

# Item Total
@app.route('/get_itemCart_totals', methods=['GET', 'POST'])
def get_itemCart_totals():
    data = request.get_json()
    item_qty = data.get('qty')
    item_price = data.get('price')

    item_total = item_qty*item_price
    return jsonify({'item_total':item_total})


with app.app_context():

    items_data = [
        {'name': 'Nordic Chair', 'price': 50.00, 'image_path': 'static/images/chair1.png', 'item_stock': 50},
        {'name': 'Auromn Chair', 'price': 35.00, 'image_path': 'static/images/chair2.png', 'item_stock': 50},
        {'name': 'Kruzo Aero Chair', 'price': 78.00, 'image_path': 'static/images/chair3.png', 'item_stock': 50},
        {'name': 'Ergonomic Chair', 'price': 43.00, 'image_path': 'static/images/chair4.png', 'item_stock': 50},
        
        
        {'name': 'KLIPPAN Sofa', 'price': 80.00, 'image_path': 'static/images/sofa1.png', 'item_stock': 50},
        {'name': 'VINLIDEN Sofa', 'price': 50.00, 'image_path': 'static/images/sofa2.png', 'item_stock': 50},
        {'name': 'VIMELLE Sofa', 'price': 78.00, 'image_path': 'static/images/sofa3.png', 'item_stock': 50},
        {'name': 'LVU Sofa', 'price': 43.00, 'image_path': 'static/images/sofa4.png', 'item_stock': 50}
        
    ]


    for item_info in items_data:
        existing_item = Furni.query.filter_by(name=item_info['name']).first()
        if not existing_item:
            item = Furni(**item_info)
            db.session.add(item)

    db.session.commit()
    
    
# @views.route('/thankyou')
# def thankyou():
#     return render_template("thankyou.html")
