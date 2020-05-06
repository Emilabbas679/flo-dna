from flask import Blueprint, session, render_template

from ..data.models import Country, Language, Product, Cart, WishList, Category, Address, Receiver, Order
from flask_login import login_required, logout_user, current_user, login_user

client = Blueprint('client', __name__, template_folder='templates', static_folder='static',
                      static_url_path='/client/static')


@client.before_request
def add_locales():
    if session.get('locales') is None:
        session['locales'] = ['az', 'en', 'ru']
    if session.get('locale') is None:
        session['locale'] = 'az'


@client.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html')


@client.app_errorhandler(500)
def handle_500(err):
    return '500', 500


from . import views


@client.context_processor
def languages():
    languages = Language.all()
    return dict(languages=languages)


@client.context_processor
def countries():
    countries = Country.all()
    return dict(countries=countries)


@client.context_processor
def locale():
    locale = session['locale']
    return dict(locale=locale)


# @client.context_processor
# def cart_products():
#     if current_user.is_authenticated:
#         cart_products= Cart.filter(Cart.customer_id==current_user.id).all()
#     else:
#         if session.get('session_id'):
#             cart_products = Cart.filter(Cart.session_id == session.get('session_id')).all()
#         else:
#             cart_products = list()
#     product_ids = []
#     new_cart_products = []
#
#     for product in cart_products:
#         product_ids.append(product.product_id)
#     new_cart_products = Product.filter(Product.id.in_((product_ids))).all()
#
#     return dict(session_cart_products=new_cart_products)


@client.context_processor
def global_cart_orders():

    if current_user.is_authenticated:
        cart_order=Order.filter(Order.customer_id==current_user.id, Order.order_status=='pending').first()
    else:
        if session.get('session_id'):
            cart_order = Order.filter(Order.session_id==session['session_id'], Order.order_status=='pending').first()
        else:
            cart_order = []
    try:
        global_total_cart_price = cart_order.total_price
    except:
        global_total_cart_price=0
    global_cart_product_count = 0

    try:
        for suborder in cart_order.suborders:
            global_cart_product_count = global_cart_product_count + len(suborder.extra_orders)
    except:
        global_cart_product_count=0

    return dict(global_cart_order=cart_order, global_total_cart_price=global_total_cart_price,\
                global_cart_product_count=global_cart_product_count)



@client.context_processor
def wishlist_products():
    if current_user.is_authenticated:
        session_wishlist_products = WishList.filter(WishList.customer_id==current_user.id).all()
    else:
        if session.get('session_id'):
            session_wishlist_products = WishList.filter(WishList.session_id == session.get('session_id')).all()
        else:
            session_wishlist_products = list()
    wishlist_product_ids = []

    for product in session_wishlist_products:
        wishlist_product_ids.append(product.product_id)
    new_wishlist_products = Product.filter(Product.id.in_((wishlist_product_ids))).all()

    return dict(session_wishlist_products=wishlist_product_ids)


@client.context_processor
def main_categories():
    categories = Category.filter(Category.parent_id==None).all()
    return dict(categories=categories)


@client.context_processor
def customer_addresses():
    if current_user.is_authenticated:
        customer_addresses = Address.filter(Address.customer_id==current_user.id).all()
    elif session.get('session_id'):
        customer_addresses = Address.filter(Address.session_id==session['session_id']).all()
    else:
        customer_addresses = dict()
    return dict(customer_addresses=customer_addresses)


@client.context_processor
def customer_receivers():
    if current_user.is_authenticated:
        customer_receivers = Receiver.filter(Receiver.customer_id==current_user.id).all()
    elif session.get('session_id'):
        customer_receivers = Receiver.filter(Receiver.session_id==session['session_id']).all()
    else:
        customer_receivers = dict()
    return dict(customer_receivers=customer_receivers)


@client.context_processor
def default_currency():
    default_currency = "€"
    return dict(default_currency=default_currency)


@client.context_processor
def default_country_code():
    default_country_code = "az"
    return dict(default_country_code=default_country_code)