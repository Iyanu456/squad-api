from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect
from mongoengine import NotUniqueError
from Models.models import User, StorageEngine
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
storage_engine = StorageEngine('squidDB', 'localhost', 27017)

csrf = CSRFProtect(app)

# Function to make a POST request to the endpoint
def make_post_request(endpoint, user_data):

    authorization_token = "sandbox_pk_25c04c9060872f1e36b8310d615e87da36aa3c51055f"

    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, json=user_data, headers=headers)

    return response

# Define the WTForms form
class UserForm(FlaskForm):
    username = StringField('Username')
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    middle_name = StringField('Middle name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()

    if form.validate_on_submit():
        try:
            # Get infrmation from form
            username=form.username.data
            first_name=form.first_name.data
            last_name=form.last_name.data
            middle_name=form.middle_name.data
            email=form.email.data
            password=form.password.data

            # Save the form data to the database
            new_user = User(username=username, first_name=first_name, last_name=last_name, middle_name=middle_name, email=email, password=password,)
            new_user.save()

            # Make a POST request to the endpoint
            user_data = {
                "display_name": first_name + last_name,
                "account_name": first_name + middle_name + last_name,
            }

            print(user_data)
            response = make_post_request("https://sandbox-api-d.squadco.com/merchant/create-sub-users", user_data)
    
            # Check the response and handle accordingly
            if response.status_code == 200:
                print(response)
            else:
                print(response)

            return redirect(url_for('success'))
        except NotUniqueError as e:
            # Handle the unique constraint violation
            print(f"Error: {e}", 'error')

    return render_template('index.html', form=form)

# Route for a success page
@app.route('/success')
def success():
    return 'Form submitted successfully!'

@app.route('/about')
def about():
    return 'About'

if __name__ == "__main__":
    # Enable debug mode
    app.run(debug=True)
