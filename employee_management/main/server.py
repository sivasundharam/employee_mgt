from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api,reqparse
import json
 
from models import Employee,db,Role,EmployeeSchema,RoleSchema
from config import config_by_name





flask_bcrypt = Bcrypt()


app = Flask(__name__)
app.config.from_object(config_by_name['dev'])

flask_bcrypt.init_app(app)
#db = SQLAlchemy(app)
db.init_app(app)
api = Api(app)

parser = reqparse.RequestParser()
@app.route('/employeee', methods=['POST'])
def add_product():
	emp_no = request.json['emp_no']
	first_name = request.json['first_name']
	last_name = request.json['last_name']
	gender = request.json['gender']
	role = request.json['role']
	new_product = employee(emp_no, first_name, last_name, gender,role)
	db.session.add(new_product)
	db.session.commit()

	return jsonify(new_product)
employee_schema = EmployeeSchema(many=True)
class Employee_api(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
    	all_products = Employee.query.all()

    	result = employee_schema.dump(all_products)
    	#print(all_products)
    	return jsonify(result)
  
        #return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self):
        already_exist = 0
        success = 0
        failed = 0
        dat = request.json
        if type(dat) == list:
            for row in dat:
                val = Employee.validator(row.keys())
                if val == "valid":
                    emp_no = row['emp_no']
                    first_name = row['first_name']
                    last_name = row['last_name']
                    gender = row['gender']
                    em = Employee.query.filter_by(emp_no=emp_no).first()
                    if em:
                        already_exist += 1
                    else:
                        new_product = Employee(emp_no, first_name, last_name, gender)
                        db.session.add(new_product)
                        try:
                            db.session.commit()
                            success += 1
                        except Exception as e:
                            failed += 1
                else:
                    failed += 1
                    

            return jsonify({"title":"employee insertion","status":{"already_exist":already_exist,"success":success,\
                "failed":failed}})
        else:
            return jsonify({"error":"Unsupported format, send data in json format"})

    def delete(self):
        success = 0
        not_found = 0
        failed = 0
        dat = request.json
        if type(dat) == list:
            for row in dat:
                if "emp_no" in row.keys():
                    emp_n = row['emp_no']
                    em = Employee.query.filter_by(emp_no=emp_n).first()
                    if em:
                        db.session.delete(em)
                        db.session.commit()
                        success += 1
                    else:
                        not_found += 1
                else:
                    failed += 1
                return jsonify({"title":"Employee Deletion","status":{"success":success,\
                    "not_found":not_found,"faile":failed}})
        else:
            return jsonify({"error":"Unsupported format, send data in json format"})
role_schema = RoleSchema(many=True)
class Assign_api(Resource):

    def post(self):
        success = 0
        already_exist =0
        failed = 0
        role_not_found = 0
        employee_not_found = 0
        dat = request.json
        if type(dat) == list:
            for row in dat:
                if "role_name" in row.keys() and "emp_no" in row.keys():
                    role_name = row['role_name']
                    emp_no = row['emp_no']
                    if type(role_name) == list and type(emp_no) == list:
                        for emp in emp_no:
                            
                            empl = Employee.query.filter_by(emp_no=emp).first()
                            if empl:
                                for rl in role_name:
                                    rol = Role.query.filter_by(role_name=rl).first()
                                    if rol:
                                        role_li = []
                                        for j in empl.roles:
                                            role_li.append(j.role_name)
                                        if rl in role_li:
                                            already_exist += 1
                                        else:
                                            empl.roles.append(rol)
                                            db.session.commit()
                                            success += 1
                                    else:
                                        role_not_found += 1
                            else:
                                employee_not_found += 1
                    else:
                        failed +=  1
                else:
                    failed += 1

                return jsonify({"title":"Role Assigning","status":{"success":success,\
                    "role_not_found":role_not_found,"employee_not_found":employee_not_found,"faile":failed,"already_exist":already_exist}})
        else:
            return jsonify({"error":"Unsupported format, send data in json format"})
    def delete(self):
        pass
        success = 0
        failed = 0
        role_not_found = 0
        employee_not_found = 0
        relation_not_found = 0
        dat = request.json
        if type(dat) == list:
                for row in dat:
                        if "role_name" in row.keys() and "emp_no" in row.keys():
                                role_name = row['role_name']
                                emp_no = row['emp_no']
                                if type(role_name) == list and type(emp_no) == list:
                                        for emp in emp_no:
                                                empl = Employee.query.filter_by(emp_no=emp).first()
                                                if empl:
                                                        for rl in role_name:
                                                                rol = Role.query.filter_by(role_name=rl).first()
                                                                if rol:
                                                                        role_li = []
                                                                        for j in empl.roles:
                                                                                role_li.append(j.role_name)
                                                                        if rl in role_li:
                                                                                del_id = role_li.index(rl)
                                                                                del empl.roles[del_id]
                                                                                db.session.commit()
                                                                                success += 1
                                                                        else:
                                                                                relation_not_found += 1
                                                                else:
                                                                        role_not_found +=1
                                                else:
                                                        employee_not_found += 1
                                else:
                                        failed += 1
                        else:
                                failed += 1
                return jsonify({"title":"Role Revocation","status":{"success":success,\
                    "role_not_found":role_not_found,"employee_not_found":employee_not_found,\
                    "faile":failed,"relationship_not_found":relation_not_found}})
        else:
            return jsonify({"error":"Unsupported format, send data in json format"})

                                


class Role_api(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        all_products = Role.query.all()

        result = role_schema.dump(all_products)
        #print(all_products)
        return jsonify(result)
        #return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self):
        already_exist = 0
        success = 0
        failed = 0
        dat = request.json
        if type(dat) == list:
            for row in dat:
                if "role_name" in row.keys():
                    role_name = row['role_name']
                    rl = Role.query.filter_by(role_name=role_name).first()
                    if rl:
                        already_exist += 1
                    else:
                        new_product = Role(role_name)
                        db.session.add(new_product)
                        try:
                            db.session.commit()
                            success += 1
                        except Exception as e:
                            failed += 1
                else:
                    failed += 1
            return jsonify({"title":"Role insertion","status":{"already_exist":already_exist,"success":success,\
                "failed":failed}})
        else:
            return jsonify({"error":"Unsupported format, send data in json format"})
    def delete(self):
        success = 0
        not_found = 0
        failed = 0
        dat = request.json
        #print(json.loads(dat))
        if type(dat) == list:
            for row in dat:
                if "role_name" in row.keys():
                    role_name = row['role_name']
                    rl = Role.query.filter_by(role_name=role_name).first()
                    if rl:
                        db.session.delete(rl)
                        db.session.commit()
                        success += 1
                    else:
                        not_found+= 1
                else:
                    failed += 1
            return jsonify({"title":"Role Deletion","status":{"success":success,\
                "not_found":not_found,"faile":failed}})
        else:
            return jsonify({"error":"Unsupported format, send data in json format"})
class lis(Resource):
    def get(self):
        return jsonify({"List of avaliable resources":["/employee","/role","/role_mgt"]})

    	    	

api.add_resource(lis, '/')
api.add_resource(Employee_api, '/employee')
api.add_resource(Role_api, '/role')
api.add_resource(Assign_api,'/role_mgt')

if __name__ == '__main__':
	app.run()
