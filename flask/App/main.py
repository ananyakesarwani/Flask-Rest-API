
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

users_path = 'flask/App/data/users.csv'

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {'result':data}, 200
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", required=True, type = str)
        parser.add_argument("name", required = True, type = str)
        parser.add_argument("city", required = True, type = str)
        parser.add_argument("locations", required = True, type = str)
        args = parser.parse_args()
        data = pd.read_csv(users_path)
        if args['userId'] in list(data['userId']):
            return {
                'message': f"{args['userId']} already exists"
            }
        else: 
            new_data = {
                'userId': args['userId'],
                'name':args['name'],
                'city':args['city'],
                'locations':args['locations']
            }
            result = data.append(new_data, ignore_index=True)
            result.to_csv(users_path, index=False)
            return {
                "data":result.to_dict(),
                "message" : "data added successfully"
            }, 200
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", required=True, type = str)
        args = parser.parse_args()
        data = pd.read_csv(users_path)
        if args['userId'] not in list(data['userId']):
            return {
                'message': f"{args['userId']} does not exists"
            }, 404
        else: 
            data = data.loc[data['userId']!=args['userId']]
            data.to_csv(users_path, index=False)
            return {
                "data":data.to_dict(),
                "message" : "data deleted successfully"
            }, 200
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", required=True, type = str)
        parser.add_argument("name", required = False, type = str)
        parser.add_argument("city", required = False, type = str)
        parser.add_argument("locations", required = False, type = str)
        args = parser.parse_args()
        data = pd.read_csv(users_path)
        if args['userId'] not in list(data['userId']):
            return {
                'message': f"{args['userId']} does not exists"
            }, 404
        else: 
            print(args, type(args))
            name = args['name'] if args['name']!=None else list(data.loc[data['userId']==args['userId']]['name'])[0]
            city = args['city'] if args['city']!=None else list(data.loc[data['userId']==args['userId']]['city'])[0]
            locations = args['locations'] if args['locations']!=None else list(data.loc[data['userId']==args['userId']]['locations'])[0]
            data.loc[data['userId']==args['userId'], ["name","city","locations"]] = [name,city,locations]
            data.to_csv(users_path, index=False)
            return {
                "data":data.to_dict(),
                "message" : "data updated successfully"
            }, 200



api.add_resource(Users,'/users')

if __name__ == "__main__":
    app.run(debug=True)