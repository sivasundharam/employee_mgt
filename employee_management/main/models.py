from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config_by_name
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import Nested
#from server import *

app = Flask(__name__)
app.config.from_object(config_by_name['dev'])
db = SQLAlchemy(app)
db.init_app(app)
ma = Marshmallow(app)
#db = SQLAlchemy()




conn = db.Table('conn',
	db.Column('emp_no',db.Integer,db.ForeignKey('Employee.emp_no')),
	db.Column('role_name',db.Integer,db.ForeignKey('Role.role_name'))
	)



class Employee(db.Model):
	__tablename__ = "Employee"
	emp_no = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50))
	last_name = db.Column(db.String(50))
	gender = db.Column(db.String(10))
	roles = db.relationship('Role',secondary=conn,backref=db.backref("Employee", lazy= 'joined'))


	def __init__(self,emp_no,first_name,last_name,gender):
		self.emp_no = emp_no
		self.first_name = first_name
		self.last_name = last_name
		self.gender = gender
	def validator(keys):
		li = ["emp_no","first_name","last_name","gender"]
		temp = 0
		for i in li:
			if i in keys:
				pass
			else:
				temp = 1
				break
		if temp == 1:
			return "not valid"
		else:
			return "valid"



class Role(db.Model):
	__tablename__ = "Role"
	#rl_id = db.Column(db.Integer)
	role_name = db.Column(db.String(50), primary_key=True)
	


	def __init__(self,name):
		self.role_name = name

class RoleSchema(ModelSchema):

	class Meta:
		model = Role

class EmployeeSchema(ModelSchema):

	

	class Meta:
		model = Employee

	roles = Nested(RoleSchema,many=True)


