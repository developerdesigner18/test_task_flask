from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import flash, request, render_template, redirect, url_for

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asdf@123'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

# with app.app_context():
#     db.create_all()

@app.route("/", methods=['GET', 'POST'])
def login_post(request=request):

    if request.method == 'POST':

        username = request.form.get('uname')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.password == password:
            flash('Please check your login details and try again.')
            return redirect('/')
        
        return render_template('items_add.html')
                            
    return render_template('login.html')

@app.route("/items/add/", methods=['GET', 'POST'])
def item_add(request=request):

    if request.method == 'POST':

        iname = request.form.get('iname')
        iprice = request.form.get('iprice')

        new_item = Item(name=iname, price=iprice)
        db.session.add(new_item)
        db.session.commit()

        flash('Item Added Successfully')

        items = Item.query.all()

        item_total_price = db.session.query(func.sum(Item.price)).scalar()

        return render_template('items_add.html', data=items, total_price=item_total_price)
    
    items = Item.query.all()

    item_total_price = db.session.query(func.sum(Item.price)).scalar()
                       
    return render_template('items_add.html', data=items, total_price=item_total_price)

@app.route("/items/display/", methods=['GET'])
def item_display():

    items = Item.query.all()

    item_total_price = db.session.query(func.sum(Item.price)).scalar()

    return render_template('item_display.html', data=items, total_price=item_total_price)
    

if __name__ == '__main__':
    app.run(debug=True)
    

