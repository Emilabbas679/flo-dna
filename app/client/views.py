import datetime
import json
import json.encoder
import os
import random
import string
import time

import flask
from flask import render_template, g, flash, make_response, send_from_directory, abort
from flask import request, redirect, url_for, session
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy import desc, String, or_
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from app.data.models import Customer, Cart, WishList, Country, Language, Currency, CelebrityTag, CelebrityDetail, \
    CelebrityDetailTag, CustomerPhone, Order, SubOrder, Store, StoreOffer, ExtraOrder
from . import client
from .forms.client_forms import LoginForm, RegisterForm, UpdateUserForm, CountryForm
from ..admin_api.controllers.products import serializer
import uuid


@client.before_request
def before_request():
    if session['locale'] == 'us':
        session['locale'] = 'en'
    flask.session.permanent = True
    client.permanent_session_lifetime = datetime.timedelta(minutes=20)
    flask.session.modified = True


def register_route(view, endpoint, url, pk, pk_type='uuid'):
    view_func = view.as_view(endpoint)
    client.add_url_rule(url, defaults={pk: None},
                        view_func=view_func, methods=['GET'])
    client.add_url_rule(url, view_func=view_func, methods=['POST'])
    client.add_url_rule('/%s/<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                        methods=['GET', 'PUT', 'DELETE'])


@client.context_processor
def inject_pages():
    locale = session['locale']
    return dict(locale=locale)


def redirect_url(default='.index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@client.route('/locale/<string:locale>')
def locale(locale):
    session['locale'] = 'en' if locale == 'us' else locale
    url = request.referrer
    a = url.split('/')
    # TODO fix this -> for page slug translation
    if a[3] == 'page':
        a[4] = session['slug'][locale]
        r = '/'.join(a)
        return redirect(r)
    return redirect(redirect_url())


@client.route('/logout')
def logout():
    logout_user()
    g.user = None
    return redirect(url_for('.index'))


@client.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('client.index'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        user = Customer.get(email=email)
        if user is None:
            flash("Invalid username or password", 'danger')
            return redirect(url_for('.login'))
        else:
            if user.check_password(request.form['password']):
                login_user(user, remember=True)
                g.user = user
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('.index')
                return redirect(next_page)
            else:
                return 'invalid'
                flash("Invalid username or password", 'danger')
                return redirect(url_for('.login'))


@client.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('client.index'))
    if request.method == 'GET':
        return render_template('create-account.html', form=form)
    else:
        # if form.validate_on_submit():
        if request.method == 'POST':
            email = request.form['email']
            if Customer.get(email=email):
                flash("This email has been used", 'danger')
                return redirect(url_for('.register'))
            else:
                user = Customer.create(first_name=request.form['name'],
                                email=request.form['email'], is_active=True,
                                password=generate_password_hash(request.form['password']))
                login_user(user, remember=True)
                g.user = user
                if session.get('session_id'):
                    wishlist_products = WishList.all(session_id=session.get('session_id'))
                    cart_products = Cart.all(session_id=session.get('session_id'))
                    for product in wishlist_products:
                        product.update(customer_id=current_user.id)
                    for product in cart_products:
                        product.update(customer_id=current_user.id)
                return redirect(url_for('.index'))
        return render_template('create-account.html', form=form)


@client.route('/', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')


@client.route('/input', methods=['GET'])
def input():
    return render_template('input.html')


@client.route('/country', methods=['GET'])
@login_required
def country_index():
    countries = Country.all()
    return render_template('country/index.html', countries=countries)


@client.route('/country/delete/<string:id>', methods=['POST'])
@login_required
def delete_country(id):
    country = Country.get(id=id)
    if country:
        country.delete()
        flash("Country has deleted", 'success')
    else:
        flash("Something went wrong", 'danger')
    return redirect(url_for('.country_index'))


@client.route('/country/edit/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_country(id):
    country = Country.get(id=id)
    if country:
        if request.method == 'GET':
            return render_template('country/edit.html', country=country)
        else:
            country.update(name=request.form['name'], code=request.form['code'], status=request.form['status'])
            flash("Country has updated", 'success')
            return redirect(url_for('.country_index'))
    else:
        flash("Something went wrong", 'danger')
        return redirect(url_for('.country_index'))


@client.route('/country/create', methods=['POST', 'GET'])
@login_required
def create_country():
    if request.method == 'GET':
        return render_template('country/create.html')
    else:
        country = Country.create(name=request.form['name'], code=request.form['code'], status=request.form['status'])
        flash("Country has created", 'success')
        return redirect(url_for('.country_index'))


@client.route('/lang', methods=['GET'])
@login_required
def lang_index():
    langs = Language.all()
    return render_template('lang/index.html', langs=langs)


@client.route('/lang/delete/<string:id>', methods=['POST'])
@login_required
def delete_lang(id):
    lang = Language.get(id=id)
    if lang:
        lang.delete()
        flash("Language has deleted", 'success')
    else:
        flash("Something went wrong", 'danger')
    return redirect(url_for('.lang_index'))


@client.route('/lang/edit/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_lang(id):
    lang = Language.get(id=id)
    if lang:
        if request.method == 'GET':
            return render_template('lang/edit.html', lang=lang)
        else:
            lang.update(name=request.form['name'], code=request.form['code'], status=request.form['status'])
            flash("Language has updated", 'success')
            return redirect(url_for('.lang_index'))
    else:
        flash("Something went wrong", 'danger')
        return redirect(url_for('.lang_index'))


@client.route('/lang/create', methods=['POST', 'GET'])
@login_required
def create_lang():
    if request.method == 'GET':
        return render_template('lang/create.html')
    else:
        lang = Language.create(name=request.form['name'], code=request.form['code'], status=request.form['status'])
        flash("Language has created", 'success')
        return redirect(url_for('.lang_index'))


@client.route('/currency', methods=['GET'])
@login_required
def currency_index():
    currencies = Currency.all()
    return render_template('currency/index.html', currencies=currencies)


@client.route('/currency/delete/<string:id>', methods=['POST'])
@login_required
def delete_currency(id):
    currency = Currency.get(id=id)
    if currency:
        currency.delete()
        flash("Cuurency has deleted", 'success')
    else:
        flash("Something went wrong", 'danger')
    return redirect(url_for('.currency_index'))


@client.route('/currency/edit/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_currency(id):
    currency = Currency.get(id=id)
    if currency:
        if request.method == 'GET':
            return render_template('currency/edit.html', currency=currency)
        else:
            currency.update(name=request.form['name'], code=request.form['code'], status=request.form['status'])
            flash("Cuurency has updated", 'success')
            return redirect(url_for('.currency_index'))
    else:
        flash("Something went wrong", 'danger')
        return redirect(url_for('.currency_index'))


@client.route('/currency/create', methods=['POST', 'GET'])
@login_required
def create_currency():
    if request.method == 'GET':
        return render_template('currency/create.html')
    else:
        currency = Currency.create(name=request.form['name'], code=request.form['code'], status=request.form['status'])
        flash("Cuurency has created", 'success')
        return redirect(url_for('.currency_index'))


@client.route('/c-tag/create', methods=['POST', 'GET'])
@login_required
def celebirty_tag_create():
    langs = Language.filter(or_(Language.code == 'AZ', Language.code == 'EN', Language.code == 'RU'))
    if request.method == 'GET':
        return render_template('celebrity_tag/create.html', langs=langs)
    else:
        name = dict()
        for lang in langs:
            name[f'{lang.code.lower()}'] = request.form[f'name[{lang.code}]']
        CelebrityTag.create(name=name, status=request.form['status'])
        flash("Tag has created", 'success')
        return redirect(url_for('.c_tag_index'))


@client.route('/c-tag', methods=['GET'])
@login_required
def c_tag_index():
    tags = CelebrityTag.all()
    return render_template('celebrity_tag/index.html', tags=tags)


@client.route('/c-tag/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_c_tag(id):
    tag = CelebrityTag.get(id=id)
    langs = Language.filter(or_(Language.code == 'AZ', Language.code == 'EN', Language.code == 'RU'))
    if tag:
        if request.method == 'GET':
            return render_template('celebrity_tag/edit.html', tag=tag, langs=langs)
        else:
            name = dict()
            for lang in langs:
                name[f'{lang.code.lower()}'] = request.form[f'name[{lang.code}]']
            tag.update(name=name, status=request.form['status'])
            flash("Tag has updated", 'success')
            return redirect(url_for('.c_tag_index'))
    flash("Tag couldnot find", 'danger')
    return redirect(url_for('.c_tag_index'))


@client.route('/c-tag/detail/<string:id>', methods=['POST'])
@login_required
def delete_c_tag(id):
    tag = CelebrityTag.get(id=id)
    if tag:
        tag.delete()
        flash("Tag has deleted", 'success')
        return redirect(url_for('.c_tag_index'))
    else:
        flash("Tag couldnot find", 'danger')
        return redirect(url_for('.c_tag_index'))


@client.route('/c-details')
@login_required
def c_detail_index():
    details = CelebrityDetail.all()
    return render_template('celebrity_details/index.html', details=details)


@client.route('/c-detail/delete/<string:id>', methods=['POST'])
@login_required
def delete_c_detail(id):
    detail = CelebrityDetail.get(id=id)
    if detail:
        rels = CelebrityDetailTag.filter(CelebrityDetailTag.celebrity_detail_id==id).all()
        for rel in rels:
            rel.delete()
        detail.delete()
        flash("Celebrity Detail has deleted", 'success')
    else:
        flash("Something went wrong", 'danger')
    return redirect(url_for('.c_detail_index'))


@client.route('/c-detail/edit/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_c_detail(id):
    detail = CelebrityDetail.get(id=id)
    if detail:
        if request.method == 'GET':
            tags = CelebrityTag.filter(CelebrityTag.status=='active').all()
            selected_tags = celebrity_detail_tag_ids(id)
            return render_template('celebrity_details/edit.html', detail=detail, tags=tags, selected_tags=selected_tags)
        else:
            tags = request.form.getlist('tags')
            celebrity_detail_tag_update(tags, detail.id)
            detail.update(name=request.form['name'], surname=request.form['surname'],\
                                        email=request.form['email'], username=request.form['username'])
            flash("Detail has updated", 'success')
            return redirect(url_for('.c_detail_index'))
    else:
        flash("Something went wrong", 'danger')
        return redirect(url_for('.c_detail_index'))


@client.route('/c-detail/create', methods=['POST', 'GET'])
@login_required
def create_c_detail():
    if request.method == 'GET':
        tags = CelebrityTag.filter(CelebrityTag.status=='active').all()
        currencies = Currency.filter(Currency.status == 'active').all()
        return render_template('celebrity_details/create.html', tags=tags, currencies=currencies)
    else:
        if request.form['discount_price'] == '':
            discount_price = 0
        else:
            discount_price = request.form['discount_price']

        detail = CelebrityDetail.create(name=request.form['name'], surname=request.form['surname'],\
                                        email=request.form['email'], username=request.form['username'],\
                                        service_price=request.form['service_price'],\
                                        currency_id=request.form['currency_id'], discount_price=discount_price)
        if request.form['phone'] and request.form['phone'] != '+994':
            CustomerPhone.create(entity_id=detail.id, entity_type='celebrity', phone_number=request.form['phone'],\
                                 verified=True, default=True)
        if 'add-phone-1' in request.form:
            CustomerPhone.create(entity_id=detail.id, entity_type='celebrity', phone_number=request.form['add-phone-1'],\
                                 verified=True, default=False)
        if 'add-phone-2' in request.form:
            CustomerPhone.create(entity_id=detail.id, entity_type='celebrity', phone_number=request.form['add-phone-2'],\
                                 verified=True, default=False)
        tags = request.form.getlist('tags')
        celebrity_detail_tag_insert(tags, detail.id)
        flash("Detail has created", 'success')
        return redirect(url_for('.c_detail_index'))


def celebrity_detail_tag_insert(tags, c_detail_id):
    for tag in tags:
        CelebrityDetailTag.create(celebrity_detail_id=c_detail_id, tag_id=tag)
    return True


def celebrity_detail_tag_ids(detail_id):
    rels = CelebrityDetailTag.filter(CelebrityDetailTag.celebrity_detail_id==detail_id).all()
    tag_ids = []
    for rel in rels:
        tag_ids.append(rel.tag_id)
    return tag_ids


def celebrity_detail_tag_update(tags, c_detail_id):
    rels = CelebrityDetailTag.filter(CelebrityDetailTag.celebrity_detail_id==c_detail_id).all()
    selected_tags = celebrity_detail_tag_ids(c_detail_id)
    if selected_tags != tags:
        for rel in rels:
            rel.delete()
    celebrity_detail_tag_insert(tags, c_detail_id)
    return True


@client.route('/order', methods=['GET'])
@login_required
def order_index():
    orders = Order.all()
    return render_template('order/index.html', orders=orders)


@client.route('/order/<string:id>', methods=['GET', 'POST'])
@login_required
def order_view(id):
    order = Order.get(id=id)
    if order:
        return render_template('order/view.html', order=order)
    else:
        flash("Something went wrong", 'danger')
    return redirect(url_for('.order_index'))


@client.route('/order/delete/<string:id>', methods=['POST'])
@login_required
def delete_order(id):
    return 'ok'
    order = Order.get(id=id)
    if len(order.suborders) == 0:
        order.delete()
        flash("Successfully deleted", 'success')
    else:
        flash("It has suborders", 'danger')
    return redirect(url_for('.order_index'))


@client.route('/order/edit/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_order(id):
    return 'ok'

    lang = Language.get(id=id)
    if lang:
        if request.method == 'GET':
            return render_template('lang/edit.html', lang=lang)
        else:
            lang.update(name=request.form['name'], code=request.form['code'], status=request.form['status'])
            flash("Language has updated", 'success')
            return redirect(url_for('.lang_index'))
    else:
        flash("Something went wrong", 'danger')
        return redirect(url_for('.lang_index'))


@client.route('/create-store-offer/<string:key>/<string:id>', methods=['POST', 'GET'])
@login_required
def create_store_offer(key, id):
    if request.method == 'GET':
        stores = Store.filter(Store.status == 'active').all()

        if key == 'suborder':
            suborder = SubOrder.get(id=id)
            offers = StoreOffer.filter(StoreOffer.order_id==id, StoreOffer.entity_key=='suborder').all()
            selected = []
            for offer in offers:
                selected.append(offer.store_id)
            return render_template('order/create-offer-suborder.html', suborder=suborder, stores=stores, selected=selected)
        else:
            extraorder = ExtraOrder.get(id=id)
            offers = StoreOffer.filter(StoreOffer.order_id==id, StoreOffer.entity_key=='extraorder').all()
            selected = []
            for offer in offers:
                selected.append(offer.store_id)
            return render_template('order/create-offer-extraorder.html', order=extraorder, stores=stores, selected=selected)
    else:

        stores = request.form.getlist('stores')

        if key == 'suborder':
            suborder = SubOrder.get(id=id)
            offers = StoreOffer.filter(StoreOffer.order_id==id, StoreOffer.entity_key=='suborder').all()
            for offer in offers:
                offer.delete()
            for store in stores:
                StoreOffer.create(entity_key='suborder', order_id=id, store_id=store, status='offer_sent')
            suborder.update(order_status='offer_sent')
            for extra in suborder.extra_orders:
                extra.update(order_status='offer_sent')
            flash("Store offers creater", 'success')
            return redirect(url_for('.order_view', id=suborder.order_id))

        else:
            extraorder = ExtraOrder.get(id=id)
            offers = StoreOffer.filter(StoreOffer.order_id ==id, StoreOffer.entity_key =='extraorder').all()
            for offer in offers:
                offer.delete()
            for store in stores:
                StoreOffer.create(entity_key='extraorder', order_id=id, store_id=store, status='offer_sent')
            extraorder.update(order_status='offer_sent')
            suborder = SubOrder.get(id=extraorder.suborder_id)
            flash("Store offers created", 'success')
            return redirect(url_for('.order_view', id=suborder.order_id))





