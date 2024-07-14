from flask import Flask, request, make_response, jsonify, session
from flask_restful import Api, Resource
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt_identity,
    current_user, jwt_required
)
from config import db, app
from models import User, Tenant, Payment, Property, Maintenance

app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Ideally, use environment variables
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)
api = Api(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

class Home(Resource):
    def get(self):
        return {"message": "Welcome to Maskani"}

api.add_resource(Home, '/')

class Signup(Resource):
    def post(self):
        data = request.get_json()
        full_name = data.get('full_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(full_name, email, phone_number, password)
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.id)
            return make_response({"user": user.to_dict(), 'access_token': access_token}, 201)
        else:
            return make_response({"error": "User already exists"}, 400)
    
api.add_resource(Signup, '/signup')

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()

        if user and user.authenticate(data.get('password')):
            access_token = create_access_token(identity=user)
            return make_response({"user": user.to_dict(), 'access_token': access_token}, 200)
        else:
            return make_response({'error': "Invalid email or password"}, 401)
    
api.add_resource(Login, '/login')

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        return make_response(current_user.to_dict(), 200)
     
api.add_resource(CheckSession, '/check_session')

class Logout(Resource):
    @jwt_required()
    def post(self):
        session.clear()
        return make_response({"message": "Logged out successfully"}, 200)

api.add_resource(Logout, '/logout')

class TenantResource(Resource):
    def get(self):
        tenants = [tenant.to_dict() for tenant in Tenant.query.all()]
        return make_response(jsonify(tenants), 200)

    def post(self):
        data = request.get_json()
        tenant = Tenant(
            name=data.get('name'),
            phone_number=data.get('phone_number'),
            id_number=data.get('id_number'),
            house_number=data.get('house_number'),
            user_id=data.get('user_id')
        )
        db.session.add(tenant)
        db.session.commit()
        return make_response(tenant.to_dict(), 201)

    def patch(self, id):
        tenant = Tenant.query.get_or_404(id)
        data = request.get_json()
        tenant.name = data.get('name', tenant.name)
        tenant.phone_number = data.get('phone_number', tenant.phone_number)
        tenant.id_number = data.get('id_number', tenant.id_number)
        tenant.house_number = data.get('house_number', tenant.house_number)
        db.session.commit()
        return make_response(tenant.to_dict(), 200)

    def delete(self, id):
        tenant = Tenant.query.get_or_404(id)
        db.session.delete(tenant)
        db.session.commit()
        return make_response({"message": "Tenant deleted successfully"}, 200)

api.add_resource(TenantResource, '/tenants', '/tenants/<int:id>')

class PaymentResource(Resource):
    def get(self):
        payments = [payment.to_dict() for payment in Payment.query.all()]
        return make_response(jsonify(payments), 200)

    def post(self):
        data = request.get_json()
        payment = Payment(
            date_payed=data.get('date_payed'),
            amount=data.get('amount'),
            amount_due=data.get('amount_due'),
            user_id=data.get('user_id'),
            tenant_id=data.get('tenant_id')
        )
        db.session.add(payment)
        db.session.commit()
        return make_response(payment.to_dict(), 201)

    def delete(self, id):
        payment = Payment.query.get_or_404(id)
        db.session.delete(payment)
        db.session.commit()
        return make_response({"message": "Payment deleted successfully"}, 200)

api.add_resource(PaymentResource, '/payments', '/payments/<int:id>')

class PropertyResource(Resource):
    def get(self):
        properties = [property.to_dict() for property in Property.query.all()]
        return make_response(jsonify(properties), 200)

    def post(self):
        data = request.get_json()
        property = Property(
            name=data.get('name'),
            location=data.get('location'),
            owner=data.get('owner'),
            image=data.get('image'),
            user_id=data.get('user_id')
        )
        db.session.add(property)
        db.session.commit()
        return make_response(property.to_dict(), 201)

api.add_resource(PropertyResource, '/properties', '/properties/<int:id>')

class MaintenanceResource(Resource):
    def get(self):
        maintenances = [maintenance.to_dict() for maintenance in Maintenance.query.all()]
        return make_response(jsonify(maintenances), 200)

    def post(self):
        data = request.get_json()
        maintenance = Maintenance(
            issue_type=data.get('issue_type'),
            description=data.get('description'),
            date_created=data.get('date_created'),
            contact_information=data.get('contact_information'),
            tenant_id=data.get('tenant_id')
        )
        db.session.add(maintenance)
        db.session.commit()
        return make_response(maintenance.to_dict(), 201)

    def patch(self, id):
        maintenance = Maintenance.query.get_or_404(id)
        data = request.get_json()
        maintenance.issue_type = data.get('issue_type', maintenance.issue_type)
        maintenance.description = data.get('description', maintenance.description)
        maintenance.date_created = data.get('date_created', maintenance.date_created)
        maintenance.contact_information = data.get('contact_information', maintenance.contact_information)
        db.session.commit()
        return make_response(maintenance.to_dict(), 200)

    def delete(self, id):
        maintenance = Maintenance.query.get_or_404(id)
        db.session.delete(maintenance)
        db.session.commit()
        return make_response({"message": "Maintenance deleted successfully"}, 200)

api.add_resource(MaintenanceResource, '/maintenances', '/maintenances/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
