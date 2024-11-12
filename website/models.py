import uuid
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from datetime import datetime
from marshmallow import Schema, fields
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,BooleanField
from wtforms.validators import DataRequired, Email, NumberRange, Length


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    number = db.Column(db.String(10), nullable=False, unique=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.String(20), nullable=False)  # Add the role column

    def __init__(self, number, firstName, lastName, email, password, role):
        self.number = number
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.role = role


class Notification(db.Model):
    n_id = db.Column(db.Integer, primary_key=True)
    n_subject = db.Column(db.String(255), nullable=False)
    n_message = db.Column(db.Text, nullable=False)
    n_is_read = db.Column(db.Boolean, default=False)
    n_created_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Notification {self.n_id}>"



class CreateCustomerForm(FlaskForm):
    c_name = StringField("Customer Name", validators=[DataRequired(message="Customer name is required")])
    c_mobile = StringField("Mobile Number", validators=[DataRequired(message="Mobile number is required"), NumberRange(min=100000000, max=999999999999, message="Please enter a valid number"), Length(min=9, max=13, message="Mobile number should be between 9 and 13 characters")])
    c_email = StringField("Email", validators=[DataRequired(message="Customer email is required"), Email(message="Please enter a valid email address")])
    c_address = StringField("Address", validators=[DataRequired(message="Customer address is required")])

# Define the IncomeExpenseForm
class IncomeExpenseForm(FlaskForm):
    ie_v_id = StringField("ie_v_id", validators=[DataRequired()])
    ie_date = StringField("ie_date", validators=[DataRequired()])
    ie_type = StringField("ie_type", validators=[DataRequired()])
    ie_description = StringField("ie_description", validators=[DataRequired()])
    ie_amount = IntegerField("ie_amount", validators=[DataRequired(), NumberRange(min=2, max=999999)])
    is_income = BooleanField("is_income", validators=[DataRequired()])
    is_expense = BooleanField("is_expense", validators=[DataRequired()])


