from models import User
from sqlalchemy.orm import validates
from timedelta import datetime
import re

#User validations
@validates('full_name')
def validate_user_full_name(self, key, full_name):
    if not full_name:
        raise ValueError("Full name must be provided")
    elif User.query.filter(User.full_name == full_name).first():
        raise ValueError("Full name must be unique")
    return full_name 

@validates('email')
def validate_user_email(self, key, email):
    if not email:
        raise ValueError("Email must be provided")
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email address")
    return email

@validates('phone_number')
def validate_user_phone_number(self, key, phone_number):
    digits = ''.join(filter(str.isdigit, phone_number))
    if len(digits) != 10:
        raise ValueError("Phone number must be 10 digits")
    return phone_number

@validates('password')
def validate_user_password(self, key, password):
    if not password:
        raise ValueError("Password cannot be empty")
    password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(password_pattern, password):
        raise ValueError("Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character")
    return password

#Tenant validations
@validates('name')
def validate_tenant_name(self, key, name):
    if not name:
        raise ValueError("Name must be provided")
    return name

@validates('phone_number')
def validate_tenant_phone_number(self, key, phone_number):
    digits = ''.join(filter(str.isdigit, phone_number))
    if len(digits) != 10:
        raise ValueError("Phone number must be 10 digits")
    return phone_number

@validates('phone_number', 'id_number', 'house_number', 'user_id')
def validate_tenant_numbers(self, key, value):
    if value < 1 or value > 9999999999:
        raise ValueError(f"{key.capitalize()} must be between 1 and 9999999999")
    return value

#Payment validations
@validates('date_payed')
def validate_date_payed(self, key, date_payed):
        if not isinstance(date_payed, datetime):
            raise ValueError("date_payed must be a datetime object")
        return date_payed

@validates('amount', 'amount_due')
def validate_amounts(self, key, value):
    if not isinstance(value, int) or value < 0:
            raise ValueError(f"{key} must be a positive integer")
    return value

@validates('user_id')
def validate_user_id(self, key, user_id):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        return user_id

#Property validations
@validates('name')
def validate_property_name(self, key, name):
    if not name:
        raise ValueError("Name must be provided")
    return name

@validates('location')
def validate_property_location(self, key, location):
    if not location:
        raise ValueError("Location must be provided")
    return location

@validates('owner')
def validate_property_owner(self, key, owner):
    if not owner:
        raise ValueError("Owner must be provided")
    return owner


#Maintenance validations
@validates('issue_type')
def validate_maintenance_issue_type(self, key, issue_type):
    if not issue_type:
        raise ValueError("Issue type must be provided")
    return issue_type

@validates('description')
def validate_maintenance_description(self, key, description):
    if not description:
        raise ValueError("Description must be provided")
    return description

@validates('contact_information')
def validate_maintenance_contact_information(self, key, contact_information):
    if not contact_information:
        raise ValueError("Contact information must be provided")
    return contact_information
    



