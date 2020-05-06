from flask_login import UserMixin
from sqlalchemy import String, Integer, Boolean, ForeignKey, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relation
from sqlalchemy_utils import EmailType, UUIDType, PasswordType
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.helpers import create_presigned_url
from database.base import Model, Column, relationship

driver_document_types = ENUM(
    'profile_picture',
    'driver_license',
    'insurance',
    'registration_certificate',
    'voen_page_1',
    'voen_page_2',
    name='document_types'
)

delivery_types = ENUM(
    'asap',
    'scheduled',
    name='delivery_types'
)

order_status = ENUM(
    'pending',
    'accepted',
    'ongoing',
    'rejected',
    'done',
    name='order_status'
)

default_statuses = ENUM(
    'active',
    'inactive',
    name='default_statuses'
)
courier_types = ENUM(
    'free',
    'paid',
    name='courier_types'
)

phone_types = ENUM(
    'whatsapp',
    'telegram',
    'viber',
    name='phone_types'
)

payment_type = ENUM(
    'cart',
    'cash',
    name='payment_type'
)

new_entity_types = ENUM(
    'customer',
    'receiver',
    'celebrity',
    name='new_entity_types'
)

order_payment_status = ENUM(
    'payed',
    'pending',
    'cancelled',
    name='order_payment_statuses')

celebrity_status = ENUM(
    'rejected',
    'pending',
    'cancelled',
    'service_paid',
    'offer_waiting',
    'paid',
    'done',
    name='celebrity_status'
)

sale_status = ENUM(
    'pending',
    'offer_sent',
    'offer_waiting',
    'accepted',
    'suspend',
    'in_progress',
    'courier',
    'delivered',
    'refund',
    'store_cancel',
    name='extra_order_status'
)


class Country(Model):
    __tablename__ = 'countries'

    name = Column(String)
    code = Column(String)
    status = Column(default_statuses)

    def __repr__(self):
        return f'Country: {self.id}'


class Language(Model):
    __tablename__ = 'languages'

    name = Column(String)
    code = Column(String)
    status = Column(default_statuses)

    def __repr__(self):
        return f'Language: {self.id}'


class Currency(Model):
    __tablename__ = 'currencies'

    name = Column(String)
    code = Column(String)
    symbol = Column(String)
    status = Column(ENUM('active', 'inactive', name='status'))

    def __repr__(self):
        return f'Currency: {self.id}'


class CountryLanguage(Model):
    __tablename__ = 'country_languages'

    country_id = Column(UUIDType(binary=False), ForeignKey('countries.id'), nullable=False)
    language_id = Column(UUIDType(binary=False), ForeignKey('languages.id'), nullable=False)
    country_code = Column(String)

    @hybrid_property
    def country(self):
        return Country.query.filter_by(id=str(self.country_id)).first()

    @hybrid_property
    def language(self):
        return Language.query.filter_by(id=str(self.language_id)).first()


class CountryCurrency(Model):
    __tablename__ = 'country_currencies'

    country_id = Column(UUIDType(binary=False), ForeignKey('countries.id'), nullable=False)
    currency_id = Column(UUIDType(binary=False), ForeignKey('currencies.id'), nullable=False)
    country_code = Column(String)

    @hybrid_property
    def country(self):
        return Country.query.filter_by(id=str(self.country_id)).first()

    @hybrid_property
    def currency(self):
        return Currency.query.filter_by(id=str(self.currency_id)).first()

class LandingPage(Model):
    __tablename__ = 'landing_pages'

    title = Column(String)
    slug = Column(String)
    meta_keyword = Column(String)
    meta_description = Column(String)
    meta_title = Column(String)
    h1 = Column(String)
    content = Column(String)
    country_id = Column(UUIDType(binary=False), ForeignKey('countries.id'))
    country = relationship('Country')
    language_id = Column(UUIDType(binary=False), ForeignKey('languages.id'))
    language = relationship('Language')
    status = Column(default_statuses)
    tags = relationship('Tag', secondary='landing_tags', backref='tags')
    # products = relationship('Product', secondary='product_landing_priority', backref='landing_pages')
    products = relationship("Product", secondary="product_landing_priority")

    def __repr__(self):
        return f'LandingPage: {self.id}'

    @hybrid_property
    def image(self):
        return Media.query.filter_by(entity_id=str(self.id)).first()




class LandingTag(Model):
    __tablename__ = 'landing_tags'

    landing_id = Column(UUIDType(binary=False), ForeignKey('landing_pages.id'), nullable=False)
    tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)


class Media(Model):
    __tablename__ = 'media'

    entity_id = Column(UUIDType(binary=False), nullable=False)
    entity_key = Column(String)
    title = Column(String)
    file_name = Column(String)
    content_type = Column(String)
    url = Column(String)

    def __repr__(self):
        return f'Image: {self.id} - {self.entity_id}'

    @hybrid_property
    def src(self):
        return create_presigned_url('flocake-cdn', self.file_name)


class Category(Model):
    __tablename__ = 'categories'

    name = Column(JSONB)
    parent_id = Column(UUIDType(binary=False), ForeignKey('categories.id'), nullable=True)
    description = Column(JSONB)
    meta_description = Column(String)
    meta_keyword = Column(String)
    top = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    status = Column(default_statuses)
    tags = relationship('Tag', secondary='category_tags', backref='category')
    parent = relationship("Category", remote_side=[parent_id])

    def __repr__(self):
        return f'Category: {self.id}'


class CategoryTag(Model):
    __tablename__ = 'category_tags'

    category_id = Column(UUIDType(binary=False), ForeignKey('categories.id'), nullable=False)
    tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)

    def __repr__(self):
        return f'CategoryTag: {self.id} - {self.entity_id}'


class Tag(Model):
    __tablename__ = 'tags'

    name = Column(JSONB)
    description = Column(JSONB)
    meta_description = Column(String, nullable=True)
    meta_keyword = Column(String, nullable=True)
    status = Column(default_statuses)

    def __repr__(self):
        return f'Tag: {self.id}'


class ProductType(Model):
    __tablename__ = 'product_types'

    name = Column(JSONB)
    description = Column(JSONB)
    status = Column(ENUM('active', 'inactive', name='product_type_status'), nullable=False)

    def __repr__(self):
        return f'Tag: {self.id}'


class Attribute(Model):
    __tablename__ = 'attributes'

    name = Column(JSONB)
    description = Column(JSONB)
    status = Column(ENUM('active', 'inactive', name='attribute_status'))
    values = relationship('AttributeValue')


class AttributeValue(Model):
    __tablename__ = 'attribute_values'

    attribute_id = Column(UUIDType(binary=False), ForeignKey('attributes.id'), nullable=False)
    name = Column(JSONB)
    status = Column(ENUM('active', 'inactive', name='attribute_value_status'), nullable=False)

    def __repr__(self):
        return f'Tag: {self.id}'


class Product(Model):
    __tablename__ = 'products'

    product_type_id = Column(UUIDType(binary=False), ForeignKey('product_types.id'), nullable=True)
    sku = Column(String)
    view_count = Column(Integer, default=0)
    tags = relationship('Tag', secondary='product_tags', backref='products')
    attribute_values = relationship('ProductAttribute', backref='products')
    image = relationship('ProductMedia', uselist=True)
    courier = relationship('ProductCourier', uselist=True)
    details = relationship('ProductDetail', uselist=True)

    @hybrid_property
    def detail(self):
        return ProductDetail.query.filter_by(product_id=str(self.id)).first()

    @hybrid_property
    def media(self):
        return ProductMedia.query.filter_by(product_id=str(self.id)).first()

    @hybrid_property
    def images(self):
        return ProductMedia.query.filter_by(product_id=str(self.id)).all()

    @hybrid_property
    def random_tag(self):
        return ProductTag.query.filter_by(product_id=str(self.id)).first()

    def __repr__(self):
        return f'Product: {self.id}'


class ProductCountry(Model):
    __tablename__ = 'product_countries'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    country_id = Column(UUIDType(binary=False), ForeignKey('countries.id'), nullable=False)
    country_code = Column(String)
    details = relationship('ProductDetail')

    def __repr__(self):
        return f'ProductCountry {self.id}'


class ProductDetail(Model):
    __tablename__ = 'product_details'

    product_country_id = Column(UUIDType(binary=False), ForeignKey('product_countries.id'))
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    country_id = Column(UUIDType(binary=False), ForeignKey('countries.id'), nullable=False)
    country_code = Column(String)
    price = Column(Float)
    discount_price = Column(Float, nullable=True)
    quantity = Column(Integer, default=0)
    status = Column(ENUM('active', 'inactive', name='product_status'))
    name = Column(JSONB)
    description = Column(JSONB)


class ProductCourier(Model):
    __tablename__ = 'product_couriers'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    country_id = Column(UUIDType(binary=False), ForeignKey('countries.id'))
    country_code = Column(String)
    courier_type = Column(courier_types)
    courier_price = Column(Float)
    status = Column(Boolean, default=False)

    def __repr__(self):
        return f'ProductCourier: {self.id} - {self.product_id}'


class ProductMedia(Model):
    __tablename__ = 'product_media'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    entity_key = Column(String)
    title = Column(String)
    file_name = Column(String)
    content_type = Column(String)
    url = Column(String)

    def __repr__(self):
        return f'Image: {self.id} - {self.entity_id}'

    @hybrid_property
    def src(self):
        return f'https://cdn.flocake.com/products/{self.product_id}/{self.file_name}'


class ProductAttribute(Model):
    __tablename__ = 'product_attributes'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    attribute_id = Column(UUIDType(binary=False), ForeignKey('attributes.id'), nullable=False)
    values = relationship('AttributeValue', secondary='product_attribute_values', backref='products')


class ProductAttributeValue(Model):
    __tablename__ = 'product_attribute_values'

    product_attribute_id = Column(UUIDType(binary=False), ForeignKey('product_attributes.id'), nullable=False)
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    attribute_id = Column(UUIDType(binary=False), ForeignKey('attributes.id'), nullable=False)
    attribute_value_id = Column(UUIDType(binary=False), ForeignKey('attribute_values.id'), nullable=False)


class ProductTag(Model):
    __tablename__ = 'product_tags'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    tag_id = Column(UUIDType(binary=False),  ForeignKey('tags.id'), nullable=False)

    @hybrid_property
    def tag(self):
        return Tag.query.filter_by(id=str(self.tag_id)).first()


    def __repr__(self):
        return f'ProductTags: {self.id}'


class ProductLandingPriority(Model):
    __tablename__ = 'product_landing_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    landing_id = Column(UUIDType(binary=False), ForeignKey('landing_pages.id'), nullable=False)
    count = Column(Integer, default=0)
    landing = relationship(LandingPage, backref=backref("product_landing_priority", cascade="all, delete-orphan"))
    product = relationship(Product, backref=backref("products", cascade="all, delete-orphan"))


class ProductTagPriority(Model):
    __tablename__ = 'product_tag_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)
    count = Column(Integer, default=0)


class ProductAttributePriority(Model):
    __tablename__ = 'product_attribute_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    attribute_value_id = Column(UUIDType(binary=False), ForeignKey('attribute_values.id'), nullable=False)
    count = Column(Integer, default=0)


class Page(Model):
    __tablename__ = 'page'

    title = Column(JSON)
    slug = Column(JSONB)
    sub_title = Column(JSON)
    content = Column(JSON)
    category_id = Column(Integer)
    status = Column(Boolean, default=False)

    def __repr__(self):
        return f'Page: {self.id}'


class CarMake(Model):
    __tablename__ = "car_makes"

    name = Column(String)
    key = Column(String)
    country = Column(String)

    def __repr__(self):
        return f'CarMake: {self.id}'


class CarModel(Model):
    __tablename__ = "car_models"

    name = Column(String)
    make_id = Column(UUIDType(binary=False), ForeignKey('car_makes.id'), nullable=False)
    make_key = Column(String)
    trims = relationship('CarTrim')

    def __repr__(self):
        return f'CarModel: {self.id}'


class CarTrim(Model):
    __tablename__ = 'car_trims'

    model_id = Column(UUIDType(binary=False), ForeignKey('car_models.id'), nullable=False)
    name = Column(String)
    key = Column(Integer)

    def __repr__(self):
        return f'CarTrim: {self.id}'


class Color(Model):
    __tablename__ = "color"

    name = Column(String(20))
    is_active = Column(Boolean, default=0)

    def __repr__(self):
        return f'Color: {self.id}'


class DriverType(Model):
    __tablename__ = "driver_types"

    name = Column(String(50))
    icon = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'DriverType: {self.id}'

    @hybrid_property
    def icon_url(self):
        return 'uploads/content/type/{}'.format(self.icon)


class Registration(Model):
    ___tablename__ = 'registrations'
    phone_number = Column(String)
    code = Column(String)
    step = Column(String)

    def __repr__(self):
        return f'Registration: {self.id}'


class Driver(Model):
    __tablename__ = 'drivers'
    username = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(EmailType, nullable=False)
    verified = Column(Boolean, default=False)
    type_id = Column(UUIDType(binary=False), ForeignKey('driver_types.id'))
    documents = relationship('DriverDocument')
    type = relationship('DriverType')

    def __repr__(self):
        return f'Driver: {self.id}'


class DriverDocument(Model):
    __tablename__ = 'driver_documents'
    driver_id = Column(UUIDType(binary=False), ForeignKey('drivers.id'), nullable=False)
    document_type = Column(driver_document_types, nullable=False)
    verified = Column(Boolean, nullable=False)
    media_id = Column(UUIDType(binary=False), ForeignKey('media.id'))
    media = relationship('Media')

    def __repr__(self):
        return f'DriverDocument: {self.id}'


class DriverCar(Model):
    __tablename__ = "driver_cars"

    make_id = Column(UUIDType(binary=False), ForeignKey('car_makes.id'))
    model_id = Column(UUIDType(binary=False), ForeignKey('car_models.id'))
    trim_id = Column(UUIDType(binary=False), ForeignKey('car_trims.id'))
    driver_id = Column(UUIDType(binary=False), ForeignKey('drivers.id'), nullable=False)
    year = Column(Integer)
    car_number = Column(String(9))
    color_id = Column(UUIDType(binary=False), ForeignKey('color.id'))

    def __repr__(self):
        return f'DriverCar: {self.id}'


class DriverDeposit(Model):
    __tablename__ = "driver_deposit"

    driver_id = Column(UUIDType(binary=False), ForeignKey('drivers.id'))
    amount = Column(Float(10))

    def __repr__(self):
        return f'DriverDeposit: {self.id}'


class PaymentTypes(Model):
    __tablename__ = 'payment_type'

    label = Column(String)
    payment_details = Column(String)
    status = Column(ENUM('active', 'inactive', name='payment_statuses'))
# Customer models


class Customer(UserMixin, Model):
    __tablename__ = "customer"
    username = Column(String, unique=True)
    first_name = Column(String(30))
    last_name = Column(String(50))
    email = Column(String(50), unique=True, nullable=False)
    profile_image = Column(String)
    gender = Column(Boolean, default=0)
    verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    password = Column(String(128))
    address = relationship('CustomerAddress')
    phone_number = Column(String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @hybrid_property
    def avatar(self):
        return 'uploads/customers/{}'.format(self.profile_image)

    def __repr__(self):
        return f'Customer: {self.id}'


class CustomerSms(Model):
    __tablename__ = "customer_sms"

    phone_number = Column(String(13))
    code = Column(String(6))
    is_checked = Column(Boolean, default=0)


class CustomerAddress(Model):
    __tablename__ = "customer_address"

    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'))
    type = Column(ENUM('home', 'work', name='address_type'))
    name = Column(String)
    full_address = Column(String)
    lat = Column(String)
    lng = Column(String)

    def __repr__(self):
        return f'CustomerAddress: {self.id}'


class CustomerPhone(Model):
    __tablename__ = 'entity_phones'

    entity_id = Column(UUIDType(binary=False), nullable=False)
    entity_type = Column(new_entity_types)
    phone_number = Column(String)
    phone_type = Column(phone_types)
    verified = Column(Boolean, default=False)
    default = Column(Boolean, default=False)


class CustomerEmail(Model):
    __tablename__ = 'entity_emails'

    entity_id = Column(UUIDType(binary=False), nullable=False)
    email = Column(String)
    verified = Column(Boolean, default=False)
    default = Column(Boolean, default=False)


# Order models
class Order(Model):
    __tablename = "order"

    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'), nullable=True)
    session_id = Column(String, nullable=True)
    payment_type_id = Column(UUIDType(binary=False), ForeignKey('payment_type.id'), nullable=True)
    order_status = Column(order_status)
    total_price = Column(Float)
    discounted_price = Column(Float)
    bill_price = Column(Float)

    @hybrid_property
    def suborders(self):
        return SubOrder.query.filter_by(order_id=str(self.id)).all()

    @hybrid_property
    def customer(self):
        return Customer.get(id=self.customer_id)

    @hybrid_property
    def payment_type(self):
        return PaymentTypes.get(id=self.payment_type_id)


    def __repr__(self):
        return f'Order: {self.id}'


class SubOrder(Model):
    __tablename__ = 'sub_order'

    title = Column(String, nullable=True)
    order_id = Column(UUIDType(binary=False), ForeignKey('order.id'), nullable=False)
    total_price = Column(Float)
    receiver_id = Column(UUIDType(binary=False), ForeignKey('receivers.id'))
    address_id = Column(UUIDType(binary=False), ForeignKey('addresses.id'))
    delivery_type = Column(ENUM('fast', 'scheduled', name='delivery_typess'))
    delivery_date = Column(DateTime)
    delivery_time = Column(String)
    message = Column(String)
    order_status = Column(sale_status)
    is_cart = Column(Boolean, unique=False, default=True)

    @hybrid_property
    def product(self):
        return Product.query.filter_by(id=str(self.product_id)).first()

    @hybrid_property
    def address(self):
        return Address.query.filter_by(id=str(self.address_id)).first()

    @hybrid_property
    def receiver(self):
        return Receiver.query.filter_by(id=str(self.receiver_id)).first()

    @hybrid_property
    def extra_orders(self):
        return ExtraOrder.query.filter_by(suborder_id=str(self.id)).all()


class ExtraOrder(Model):
    __tablename__ = 'extra_order'
    suborder_id = Column(UUIDType(binary=False), ForeignKey('sub_order.id'), nullable=False)
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    track_key = Column(String)
    product_price = Column(Float)
    courier_price = Column(Float)
    country_code = Column(String)
    order_status = Column(sale_status)
    total_items = Column(Integer, default=1)

    @hybrid_property
    def product(self):
        return Product.query.filter_by(id=str(self.product_id)).first()

class Receiver(Model):
    __tablename__ = 'receivers'

    full_name = Column(String)
    order_id = Column(UUIDType(binary=False), ForeignKey('order.id'), nullable=True)
    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'), nullable=True)
    session_id = Column(String, nullable=True)

    # full_address = Column(String)
    # address_details = Column(String)
    # lat = Column(String)
    # lng = Column(String)
    phones = relationship('CustomerPhone',
                          primaryjoin="remote(Receiver.id)==foreign(CustomerPhone.entity_id)",
                          uselist=True)

    @hybrid_property
    def mobiles(self):
        return CustomerPhone.query.filter_by(entity_id=self.id).all()


class Address(Model):
    __tablename__ = 'addresses'

    address_name = Column(String)
    full_address = Column(String)
    address_details = Column(String)
    lat = Column(String)
    lng = Column(String)
    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'), nullable=True)
    session_id = Column(String, nullable=True)


class ReceiverAdressPriority(Model):
    __tablename__ = 'receiver_address_priority'

    address_id = Column(UUIDType(binary=False), ForeignKey('addresses.id'), nullable=False)
    receiver_id = Column(UUIDType(binary=False), ForeignKey('receivers.id'), nullable=False)


class OrderPayment(Model):
    __tablename__ = 'order_payments'

    order_id = Column(UUIDType(binary=False), ForeignKey('order.id'), nullable=False)
    payment_details = Column(JSONB)
    status = Column(order_payment_status)


class AdvancedPayment(Model):
    __tablename__ = 'advance_payments'

    email = Column(String)
    amount = Column(Float)
    payment_type_id = Column(UUIDType(binary=False), ForeignKey('payment_type.id'))
    status = Column(ENUM('payed', 'pending', 'cancelled', name='order_payment_status'))
    payment_details = Column(String)

    def __repr__(self):
        return f'AdvancedPayment: {self.id}'


class Cart(Model):
    __tablename__ = 'cart'

    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'))
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    session_id = Column(String)
    total_items = Column(Integer)

    def __repr__(self):
        return f'Cart: {self.id}'


class WishList(Model):
    __tablaname__ = 'wish_list'

    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'))
    session_id = Column(String)
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)

    def __repr__(self):
        return f'WishList {self.id}'


class Store(Model):
    __tablename__ = 'stores'

    company_name = Column(String, nullable=False)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    country = Column(String)
    address = Column(String)
    address_ltd = Column(String)
    address_details = Column(String)
    address_lng = Column(String)
    about = Column(String)
    delivery_area = Column(String)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    status = Column(ENUM('active', 'inactive', name='store_status'))
    phones = relationship('CustomerPhone',
                          primaryjoin="remote(Store.id)==foreign(CustomerPhone.entity_id)",
                          uselist=True)
    offers = relationship('StoreOffer',
                          primaryjoin="remote(Store.id)==foreign(StoreOffer.store_id)",
                          uselist=True)

    def __repr__(self):
        return f'Store: {self.id}'


class StoreOffer(Model):
    __tablename__ = 'store_offers'

    order_id = Column(UUIDType(binary=False), nullable=False)
    entity_key = Column(ENUM('suborder', 'extraorder', name='store_entity'))
    store_id = Column(UUIDType(binary=False), ForeignKey('stores.id'), nullable=False)
    price = Column(Float)
    delivery_price = Column(Float)
    message = Column(String)
    picked = Column(Boolean, default=False)
    status = Column(ENUM('offer_sent', 'offer_waiting', 'accepted', 'suspend', name='offer_status'))

    def __repr__(self):
        return f'Store Offer: {self.id}'


class Contact(Model):
    __tablename__ = 'contacts'

    full_name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(String)

    def __repr__(self):
        return f'Contact: {self.id}'


class HomeBox(Model):
    __tablename__ = 'home_boxes'

    name = Column(JSONB)
    status = Column(ENUM('active', 'inactive', name='box_status'))
    tags = relationship('Tag', secondary='home_box_tags', backref='home_tags')
    landings = relationship('LandingPage', secondary='home_box_landings', backref='home_landings')

    def __repr__(self):
        return f'HomeBox: {self.id}'


class HomeBoxTag(Model):
    __tablename__ = 'home_box_tags'

    box_id = Column(UUIDType(binary=False), ForeignKey('home_boxes.id'), nullable=False)
    tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)


class HomeBoxLanding(Model):
    __tablename__ = 'home_box_landings'

    box_id = Column(UUIDType(binary=False), ForeignKey('home_boxes.id'), nullable=False)
    landing_id = Column(UUIDType(binary=False), ForeignKey('landing_pages.id'), nullable=False)


class HelpCategory(Model):
    __tablename__ = 'help_categories'

    name = Column(JSONB)
    status = Column(ENUM('active', 'inactive', name='help_category_status'))
    articles = relationship('HelpArticle', backref='category')

    def __repr__(self):
        return f'HelpCategory: {self.id}'


class HelpArticle(Model):
    __tablename__ = 'help_articles'

    name = Column(JSONB)
    content = Column(JSONB)
    category_id = Column(UUIDType(binary=False), ForeignKey('help_categories.id'), nullable=False)
    status = Column(ENUM('active', 'inactive', name='help_status'))

    def __repr__(self):
        return f'HelpArticle: {self.id}'


class ProductExtraTag(Model):
    __tablename__ = 'product_extra_tags'

    tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)
    extra_tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)


class ProductExtraProduct(Model):
    __tablename__ = 'product_extra_tags'

    tag_id = Column(UUIDType(binary=False), ForeignKey('tags.id'), nullable=False)
    extra_product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)


class ProductExtraPriority(Model):
    __tablename__ = 'product_extra_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    extra_product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    count = Column(Integer, default=0)


class ProductRelatedPriority(Model):
    __tablename__ = 'product_related_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    related_product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    count = Column(Integer, default=0)


class ProductSimilarPriority(Model):
    __tablename__ = 'product_similar_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    similar_product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    count = Column(Integer, default=0)


class ProductCartPriority(Model):
    __tablename__ = 'product_cart_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    count = Column(Integer, default=0)


class ProductWishListPriority(Model):
    __tablename__ = 'product_wish_list_priority'

    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
    count = Column(Integer, default=0)


class CelebrityTag(Model):
    __tablename__ = 'celebrity_tags'

    name = Column(JSONB)
    status = Column(default_statuses)

    def __repr__(self):
        return f'CelebrityTag: {self.id}'


class CelebrityDetail(Model):
    __tablename__ = 'celebrity_details'

    name = Column(String)
    surname = Column(String)
    email = Column(String)
    username = Column(String)
    service_price = Column(Float, default=0)
    discount_price = Column(Float, default=0)
    currency_id = Column(UUIDType(binary=False),  ForeignKey('currencies.id'), nullable=False)

    def __repr__(self):
        return f'CelebrityDetail: {self.id}'


class CelebrityDetailTag(Model):
    __tablename__ = 'celebrity_detail_tags'

    celebrity_detail_id = Column(UUIDType(binary=False), ForeignKey('celebrity_details.id'), nullable=False)
    tag_id = Column(UUIDType(binary=False),  ForeignKey('celebrity_tags.id'), nullable=False)

    def __repr__(self):
        return f'CelebrityDetailTag: {self.id}'


class CelebrityOrders(Model):
    __tablename__ = 'celebrity_orders'

    celebrity_detail_id = Column(UUIDType(binary=False), ForeignKey('celebrity_details.id'), nullable=False)
    customer_id = Column(UUIDType(binary=False), ForeignKey('customer.id'))
    currency_id = Column(UUIDType(binary=False), ForeignKey('currencies.id'))
    from_whom = Column(String)
    to_whom = Column(String)
    last_date = Column(DateTime)
    text = Column(String)
    note = Column(String)
    service_price = Column(Float, default=0)
    offer_price = Column(Float, default=0)
    total_price = Column(Float, default=0)
    respond_date = Column(DateTime)
    status = Column(celebrity_status)
