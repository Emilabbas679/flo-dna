from flask import render_template, redirect, request, flash, url_for, session, g
from flask.views import MethodView
from flask_login import current_user, login_user
from werkzeug.urls import url_parse

from app.client.forms.client_forms import VerifyForm
from app.data.models import Customer, CustomerSms, Order


class VerificationView(MethodView):

    def __init__(self):
        self.form = VerifyForm()

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        form = self.form
        return render_template('verification.html', form=form)

    def post(self):
        form = self.form
        if form.validate_on_submit():
            sms = CustomerSms.get(code=request.form.get('code'))
            if sms is None:
                flash("Invalid code", 'danger')
                return redirect(url_for('.verify'))
            user = Customer.get(phone_number=sms.phone_number)
            login_user(user, remember=True)
            g.user = user
            sms.delete()
            if session.get('order') is not None:
                order = Order.get(id=session['order'])
                payload = {
                    "customer_id": user.id
                }
                order.update(**payload)
                session.pop("order", None)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('.index')
            return redirect(next_page)
        return self.get()
