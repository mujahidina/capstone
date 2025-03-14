from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from models import db, User
from flask_talisman import Talisman


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
Talisman(app)


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = str(data.get("password"))
        age = data.get("age")

        if not password or len(password) < 8:
            return {"error": "Password must be at least 8 characters long."}, 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already in use."}, 400
        
        
        hashed_password = bcrypt.generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            age=age,
            password=hashed_password
        )
        # new_user.set_password(password) 

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "id":"new_user.id",
            "username":"new_user.username",
        })

api.add_resource(UserRegister,"/user/register")        


class Users(Resource):
    def get(self):
        users = [user.to_dict(only=('id', 'name', 'email',"age")) for user in User.query.all()]
        return make_response(jsonify(users),200)

api.add_resource(Users, "/users")


class UserByID(Resource):

    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        return make_response(jsonify(user.to_dict(only=("id", "name", "email", "age"))), 200)


    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()

        for attr in data:
            setattr(user, attr, data.get(attr))

        db.session.commit()
        return make_response(user.to_dict(), 200)

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return make_response("", 204)

api.add_resource(UserByID, "/users/<int:id>")


if __name__ == "__main__":
    app.run(debug=True)
