from marshmallow import Schema, fields


class UserSchema(Schema):
    number = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email()
    password = fields.String(load_only=True)
    date = fields.DateTime()
    role = fields.String()

class NotificationSchema(Schema):
    n_id = fields.Integer()
    n_subject = fields.String()
    n_message = fields.String()
    n_is_read = fields.Boolean()
    n_created_date = fields.DateTime()

class CreateCustomerFormSchema(Schema):
    c_name = fields.String()
    c_mobile = fields.String()
    c_email = fields.String()
    c_address = fields.String()

class IncomeExpenseFormSchema(Schema):
    ie_v_id = fields.String()
    ie_date = fields.String()
    ie_type = fields.String()
    ie_description = fields.String()
    ie_amount = fields.Integer()
    is_income = fields.Boolean()
    is_expense = fields.Boolean()

