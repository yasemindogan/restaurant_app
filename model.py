
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class restaurant(db.Model):
   id = db.Column('restaurant_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))

   def __init__(self, name, city, addr,pin):
    self.name = name
    self.city = city
    self.addr = addr
    self.pin = pin

class employees(db.Model):
   id = db.Column('employee_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   surname = db.Column(db.String(50))
   email = db.Column(db.String(200)) 
   phone = db.Column(db.String(10))
   company = db.Column(db.String(10))


   def __init__(self, name, surname, email,phone,company):
    self.name = name
    self.surname = surname
    self.email = email
    self.phone = phone
    self.company = company
    

class users(db.Model):
   id = db.Column('user_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   surname = db.Column(db.String(50))
   email = db.Column(db.String(200)) 
   password = db.Column(db.String(10))

   def __init__(self, name, surname, email,password):
    self.name = name
    self.surname = surname
    self.email = email
    self.password = password

class menu(db.Model):
   id = db.Column( db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   restaurant_id = db.Column(db.String(50))
   created_date = db.Column(db.String(200))
   menu_detail = db.Column(db.LargeBinary)

   def __init__(self, name, restaurant_id, created_date,menu_detail):
    self.name = name
    self.restaurant_id = restaurant_id
    self.created_date = created_date
    self.menu_detail = menu_detail

class votes(db.Model):
   id = db.Column('vote_id', db.Integer, primary_key = True)
   menu_id = db.Column(db.String(100))
   vote_date = db.Column(db.String(50))
   created_date = db.Column(db.String(200))
   point = db.Column(db.Text(500))

   def __init__(self, menu_id, vote_date, created_date,point):
    self.menu_id = menu_id
    self.vote_date = vote_date
    self.created_date = created_date
    self.point = point
