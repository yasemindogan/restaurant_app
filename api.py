# # -*- coding: utf-8 -*
# import config_env
import os
from flask import Flask, request, jsonify, make_response, send_file
# from flask_cors import CORS, cross_origin
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import hashlib
from io import BytesIO

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from model import *
from datetime import date
## main screeen
@app.route('/')
def show_all():
    return render_template('show_all.html', restaurant = restaurant.query.all(), employee = employees.query.all(),user = users.query.all() )

## to add new restaurant
@app.route('/new_restaurant', methods = ['GET', 'POST'])
def new_restaurant():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         restaur = restaurant(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
         db.session.add(restaur)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new_restaurant.html')


#to list the all restaurants
def get_restaurants():
    list_restaurant = restaurant.query.all()
    for rest in list_restaurant:
        print ("rest",rest.name)
    print("list_restaurant",list_restaurant )
    return render_template('upload_menu.html')


## to add new employee
@app.route('/new_employee', methods = ['GET', 'POST'])
def new_employee():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['surname'] or not request.form['email']:
         flash('Please enter all the fields', 'error')
      else:
         employee = employees(request.form['name'], request.form['surname'],request.form['email'], request.form['phone'], request.form['company'])
         print("employee",employee)
         db.session.add(employee)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new_employee.html')


#to vote for a menu
@app.route('/new_vote', methods = ['GET', 'POST'])
def new_vote():
   if request.method == 'POST':
      today = date.today()
      if not request.form['menu_id'] or not request.form['point']:
         flash('Please enter all the fields', 'error')
      else:
         vote = votes(request.form['menu_id'],today, today, request.form['point'])
         print("vote",vote)
         db.session.add(vote)
         db.session.commit()
         flash('vote poin was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new_vote.html')


#to get the the daily   restaurant's menu votes value
@app.route('/get_daily_vote_result/<date>')
def get_daily_vote_result(date=0):
    vote_info = {}
    list_votes = votes.query.filter_by(vote_date=date).all()
    # print("list_votes",list_votes)
    sum_point=0
    message = ''
    if len(list_votes) != 0:
        
        for vote in list_votes:
            vote_detail=[]
            print ("rest",vote.point)
            print ("menu",vote.menu_id)
            vote_detail.append(int(vote.menu_id))
            vote_detail.append(int(vote.point))
            vote_info[vote.id]=vote_detail
    
    vote_value = list(vote_info.values())

    sum_vote=0
    vot_val = {}

    for j in range(len(vote_value)-1):
        print("j",j)
        
        # for i in range(len(vote_value[j])):
        if vote_value[j+1][0] == vote_value[j][0]:
            
            sum_vote = sum_vote + vote_value[j][1]  
            vot_val['menu_id_'+str(vote_value[j][0])] = sum_vote
    message = "vote result"+str(vot_val)+"sonuc" 
    # return render_template('vote_result.html')
    return message


#create new userr
@app.route('/new_user', methods = ['GET', 'POST'])
def new_user():
   if request.method == 'POST':
      hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
      print("hashed_password",hashed_password)
      if not request.form['name'] or not request.form['surname'] or not request.form['email'] or not request.form['password']:
         flash('Please enter all the fields', 'error')
      else:
         user = users(request.form['name'], request.form['surname'],request.form['email'], hashed_password)
         db.session.add(user)
         db.session.commit()
         flash('User was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new_user.html')


## list all users
@app.route('/get_user')
def get_user():
   return render_template('show_user.html',user = users.query.all())


# Route for handling the login page logic ##basic login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # auth = request.authorization
    # print("authhhhhh", auth)
    error = None
    if request.method == 'POST':
        user = users.query.filter_by(name=request.form['name']).first()
        if not user:
            error = 'Invalid Credentials. Please try again.'

        if  hashlib.sha256(request.form['password'].encode('utf8')).hexdigest() == user.password:
            flash('you loged in successfully')
            return redirect(url_for('show_all'))
        else:
            error = 'Invalid Credentials. Please try again.'
            
    return render_template('login.html', error=error)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

### upload menu the (i test with .png)
@app.route('/upload_menu', methods=['GET', 'POST'])
def upload_menu():
    today = date.today()
    get_restaurants()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            newFile = menu(name=filename, restaurant_id=1, created_date=today, menu_detail=file.read())
            db.session.add(newFile)
            db.session.commit()
            flash('Menu image  is successfully added')
            return redirect(url_for('show_all'))

    return render_template('upload_menu.html')


## download/ show the menu whih menu is wanted
@app.route('/download_menu/menu_id')
def download_menu(menu_id=0):

    menu_downloaded = menu.query.filter_by(id=menu_id).first() 

    return send_file(BytesIO(menu_downloaded.menu_detail), attachment_filename='flask.png', as_attachment=True)


#list the all menus name to vote part can be use or to see the menu
@app.route('/get_menu_name')
def get_menu_name():
    menus = menu.query.all()

    menu_info={}

    for men in menus:
            menu_detail=[]
            menu_detail.append(men.name)
            menu_info[men.id] = menu_detail
    return render_template('new_menu.html')


#Create a new menu with detail if there is need to use instead of upload
@app.route('/new_menu', methods = ['GET', 'POST'])
def new_menu():
   if request.method == 'POST':
      today = date.today()
      if not request.form['name'] or not request.form['restaurant_id'] :
         flash('Please enter all the fields', 'error')
      else:
         menus = menu(request.form['name'], request.form['restaurant_id'],today, request.form['menu_detail'])
         db.session.add(menus)
         db.session.commit()
         flash('Menu was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new_menu.html')


#### get the current day menu
#### for example you download an png of menu and give the date like the example
# it will downlaod as  png fromat which the date is given http://localhost:5000/get_current_day_menu/2019-06-25
@app.route('/get_current_day_menu/<from_date>')
def get_current_day_menu(from_date=0):
    today_menu = menu.query.filter_by(created_date=from_date).first() 

    return send_file(BytesIO(today_menu.menu_detail), attachment_filename='menu.png', as_attachment=True)


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
