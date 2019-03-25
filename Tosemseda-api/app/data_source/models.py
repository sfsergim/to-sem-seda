# -*- coding: utf-8 -*-
import datetime
import unicodedata
import app.data_source.database

from app import config as config_module
from app.domain.service import exceptions

logged_user = None
db = app.data_source.database.AppRepository.db
config = config_module.get_config()


class AbstractModel(object):
    class AlreadyExist(Exception):
        pass

    class NotExist(Exception):
        pass

    class RepositoryError(Exception):
        pass

    @classmethod
    def get_all_ids_in(cls, items_id):
        return db.session.query(cls).filter(cls.id.in_(items_id)).all()

    @classmethod
    def one_or_none(cls, **kwargs):
        return cls.filter(**kwargs).one_or_none()

    @classmethod
    def filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def filter_simple(cls, **kwargs):
        return cls.query.filter_by(deleted=False, **kwargs)

    @classmethod
    def filter_simple_without_deleted(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def get_list(cls, *args, **kwargs):
        return cls.query.filter_by()

    @classmethod
    def get_item(cls, item_id):
        item = cls.query.get(item_id)
        if not item:
            raise cls.NotExist
        else:
            return item

    @classmethod
    def slugify(cls, value):
        slug = unicodedata.normalize('NFKD', value)
        slug = slug.replace(' ', '-')
        slug = slug.encode('ascii', 'ignore').lower()
        return slug

    def delete_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_db(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        else:
            db.session.flush()

    def commit_session(self):
        db.session.commit()

    @classmethod
    def create_from_json(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db()
            return instance
        except Exception as ex:
            raise exceptions.RepositoryError(ex.message)

    @classmethod
    def create_from_json_without_commit(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db(commit=False)
            return instance
        except Exception as ex:
            raise cls.RepositoryError(ex.message)

    @classmethod
    def update_from_json(cls, item_id, json_data):
        try:
            instance = cls.get_item(item_id)
            instance.set_values(json_data)
            instance.save_db()
            return instance
        except db.IntegrityError as ex:
            raise cls.RepositoryError(ex.message)

    def set_values(self, json_data):
        for key, value in json_data.iteritems():
            setattr(self, key, json_data.get(key, getattr(self, key)))

    @classmethod
    def roll_back_session(cls):
        db.session.rollback()


class User(db.Model, AbstractModel):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password= db.Column(db.String)
    cellphone = db.Column(db.String)
    perfil= db.Column(db.Integer)
    status = db.Column(db.String)
    last_payment_method = db.Column(db.String)
    addresses = db.relationship("Address", backref="User", order_by="Address.id")
    orders = db.relationship("Order", backref="User", order_by="Order.id")

    @classmethod
    def filter_users(cls):
        return cls.query.all()

    @classmethod
    def filter_avaliable_users(cls, email, password):
        return cls.query.filter_by(email=email, password=password)


class Address(db.Model, AbstractModel):
    __tablename__ = 'Address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    street_name = db.Column(db.String)
    number = db.Column(db.String)
    complement= db.Column(db.String)
    cep = db.Column(db.String)
    delivery= db.Column(db.String)


    @classmethod
    def get_addres_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


class Category(db.Model, AbstractModel):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    products = db.relationship("Product", backref="Category", order_by="Product.id")

    @classmethod
    def get_category(cls):
        return cls.query.all()


class Product(db.Model, AbstractModel):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))
    product_name = db.Column(db.String)
    product_price = db.Column(db.Integer)
    stock_quantity = db.Column(db.Integer)
    description = db.Column(db.String)
    image_source = db.Column(db.String)
    Order_Products = db.relationship("Order_Product", backref="Product", order_by="Order_Product.id")

    @classmethod
    def get_product(cls, category_id):
        return cls.query.filter_by(category_id=category_id).all()

class Order(db.Model, AbstractModel):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    creation_date = db.Column(db.Date, default=datetime.datetime.utcnow)
    finaly_date = db.Column(db.Date, default=datetime.datetime.utcnow)
    Order_Products = db.relationship("Order_Product", backref="Order", order_by="Order_Product.id")


class Order_Product(db.Model, AbstractModel):
    __tablename__ = 'Order_Product'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))

