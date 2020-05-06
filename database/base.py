import uuid

from flask import current_app
from connexion import ProblemException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, Timestamp

from core.extensions import db


Column = db.Column
relationship = relationship


class CRUDMixin(object):
    @classmethod
    def create(cls, **kwargs):
        if issubclass(cls, SurrogatePK):
            unique_id = uuid.uuid4()
            if not kwargs.get("id"):
                kwargs["id"] = unique_id
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save(commit)

    def save(self, commit=True):
        try:
            db.session.add(self)
            if commit:
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Record could not be saved in database. Error: {e}')
        else:
            return self

    def delete(self, commit=True):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Record could not be deleted. Details: {e}')
        else:
            return commit and db.session.commit()


class SurrogatePK(object):
    """A mixin that adds a surrogate UUID 'primary key' column named ``id`` to
    any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(UUIDType(binary=False), primary_key=True)


class Model(CRUDMixin, db.Model, Timestamp, SurrogatePK):
    __abstract__ = True

    @classmethod
    def exists(cls, ent_id):
        try:
            result = cls.query.get(ent_id)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Database error while doing head check. Details: {e}')
        return result is not None

    @classmethod
    def get(cls, **kwargs):
        try:
            return cls.query.filter_by(**kwargs).one_or_none()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Database error while fetching record. Details: {e}')

    @classmethod
    def filter(cls, *criterion):
        try:
            return cls.query.filter(*criterion)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Database error while fetching record. Details: {e}')

    @classmethod
    def filter_active(cls, *criterion):
        try:
            return cls.query.filter(*criterion).filter_by(status='active')
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Database error while fetching record. Details: {e}')

    @classmethod
    def all(cls, **kwargs):
        try:
            return cls.query.filter_by(**kwargs).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ProblemException(500, 'Database error', f'Database error while fetching record. Details: {e}')
