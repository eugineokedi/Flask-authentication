from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    tenants = db.relationship('Tenant', back_populates='user', cascade='all, delete-orphan')
    properties = db.relationship('Property', back_populates='user', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='user', cascade='all, delete-orphan')

    tenant_names = association_proxy('tenants', 'name')
    property_names = association_proxy('properties', 'name')
    payment_amounts = association_proxy('payments', 'amount')

    @hybrid_property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    serialize_rules = ('-payments.user', '-tenants.user', '-properties.user')

    def __init__(self, full_name, email, phone_number, password):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.password = password

    def is_active(self):
        return True

    def __repr__(self):
        return f'<User id={self.id}, full_name={self.full_name}, email={self.email}, phone_number={self.phone_number}>'

class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    id_number = db.Column(db.String, nullable=False)
    house_number = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship('User', back_populates='tenants')

    maintenances = db.relationship('Maintenance', back_populates='tenant', cascade='all, delete-orphan')

    payments = db.relationship('Payment', back_populates='tenant', cascade='all, delete-orphan')

    serialize_rules = ('-user.tenants', '-maintenances.tenant', '-payments.tenant')

    def __init__(self, name, phone_number, id_number, house_number, user_id):
        self.name = name
        self.phone_number = phone_number
        self.id_number = id_number
        self.house_number = house_number
        self.user_id = user_id

    def __repr__(self):
        return f'<Tenant id={self.id}, name={self.name}, phone_number={self.phone_number}, id_number={self.id_number}, house_number={self.house_number}>'

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    date_payed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    amount_due = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Property', back_populates='payments')
    user = db.relationship('User', back_populates='payments')
    tenant = db.relationship('Tenant', back_populates='payments')

    serialize_rules = ('-user.payments', '-property.payments', '-tenant.payments')

    def __init__(self, date_payed, amount, amount_due, user_id, tenant_id, property_id):
        self.date_payed = date_payed
        self.amount = amount
        self.amount_due = amount_due
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.property_id = property_id

    def __repr__(self):
        return f'<Payment id={self.id}, date_payed={self.date_payed}, amount={self.amount}, amount_due={self.amount_due}>'


class Property(db.Model, SerializerMixin):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship('User', back_populates='properties')
    payments = db.relationship('Payment', back_populates='property', cascade='all, delete-orphan', single_parent=True)

    serialize_rules = ('-payments.property', '-user.properties',)

    def __init__(self, name, location, owner, user_id, image):
        self.name = name
        self.location = location
        self.owner = owner
        self.user_id = user_id
        self.image = image

    def __repr__(self):
        return f'<Property id={self.id}, name={self.name}, location={self.location}, owner={self.owner}>'

class Maintenance(db.Model, SerializerMixin):
    __tablename__ = 'maintenances'

    id = db.Column(db.Integer, primary_key=True)
    issue_type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contact_information = db.Column(db.String)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    tenant = db.relationship('Tenant', back_populates='maintenances')

    serialize_rules = ('-tenant.maintenances',)  # Only include maintenance details for tenants

    def __init__(self, issue_type, description, contact_information, tenant_id, date_created=None):
        self.issue_type = issue_type
        self.description = description
        self.contact_information = contact_information
        self.tenant_id = tenant_id
        if date_created is None:
            self.date_created = datetime.utcnow()
        else:
            self.date_created = date_created

    def __repr__(self):
        return f'<Maintenance id={self.id}, issue_type={self.issue_type}, description={self.description}, contact={self.contact_information}>'
