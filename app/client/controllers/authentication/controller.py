from flask import render_template, redirect, request, flash, url_for, jsonify
from flask.views import MethodView
from flask_login import current_user

from app.client.forms.client_forms import LoginForm
from app.data.models import Customer, CustomerSms
from app.utils.twilio_helper import generate_code, send_whatsapp


class AuthView(MethodView):
    def __init__(self):
        self.form = LoginForm(request.form)

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = self.form
        return render_template('login.html', form=form)

    def post(self):
        form = self.form
        if form.validate_on_submit():
            phone_number = form.data['phone_number']
            user = Customer.get(phone_number=phone_number)
            code = generate_code()
            if user is None:
                message = send_whatsapp(phone_number, code)
                if message.error_code is None:
                    sms = CustomerSms.create(phone_number=phone_number, code=code)
                else:
                    flash('Couldnt send sms', 'danger')
                    return redirect(url_for('.auth'))
                customer = Customer.create(phone_number=phone_number)
                return redirect(url_for('.verify', next_page=request.args.get('next')))
            else:
                message = send_whatsapp(phone_number, code)
                if message.error_code is None:
                    sms = CustomerSms.create(phone_number=phone_number, code=code)
                else:
                    flash('Couldnt send sms', 'danger')
                    return redirect(url_for('.auth'))
                return redirect(url_for('.verify', next_page=request.args.get('next')))
        return self.get()
