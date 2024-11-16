from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import email_validator
from wtforms.validators import DataRequired, Email
import smtplib
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = os.getenv("SECRET_KEY")

my_email = os.getenv('MY_EMAIL')
email_password = os.getenv('PASSWORD')


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(message="Invalid email")])
    number = StringField(label='Phone Number', validators=[DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label='Send Message')


@app.route('/')
def home():
    current_year = datetime.now().year
    return render_template("index.html", year=current_year)


@app.route('/behind_the_code')
def behind_the_code():
    return render_template("behind_the_code.html")


@app.route('/credits')
def recourses_used():
    current_year = datetime.now().year
    return render_template('credits.html', year=current_year)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    current_year = datetime.now().year
    contact_form = ContactForm()

    if contact_form.validate_on_submit():

        name = contact_form.name.data
        email = contact_form.email.data
        number = contact_form.number.data
        message = contact_form.message.data

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=email_password)
                email_message = f"Subject:New Contact Form Submission\n\nName: {name}\nEmail: {email}\nPhone Number: " \
                                f"{number}\nMessage:\n{message}"
                connection.sendmail(
                    from_addr=email,
                    to_addrs=my_email,
                    msg=email_message
                )
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while sending your message: {e}", "danger")
        return redirect(url_for('contact'))

    return render_template("contact.html", form=contact_form, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
