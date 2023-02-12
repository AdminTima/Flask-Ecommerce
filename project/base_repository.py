from .api_error import ApiError
from .extensions import db
from sqlalchemy import update, delete,  literal_column


def create(table, data):
    new_obj = table(**data)
    db.session.add(new_obj)
    db.session.commit()
    db.session.refresh(new_obj)
    return new_obj


def get_by_id(table, item_id):
    item_in_db = db.session.get(table, item_id)
    if not item_in_db:
        raise ApiError.not_found()
    return item_in_db


def get_by_id_and_remove(table, item_id):
    query = delete(table).where(table.id == item_id).returning(literal_column("*"))
    result = db.session.execute(query)
    if not result:
        raise ApiError.not_found()
    db.session.commit()
    return result


def get_all(table):
    return db.session.execute(db.select(table)).scalars()


def get_by_id_and_update(table, item_id, updated_data):
    query = update(table).where(table.id == item_id).values(**updated_data).returning(literal_column('*'))
    result = db.session.execute(query)
    if not result:
        raise ApiError.not_found()
    db.session.commit()
    updated_item = get_by_id(table, item_id)
    return updated_item


def find(table, filter_by: dict, raise_exception=None, many=False):

    assert raise_exception is None or type(raise_exception) is ApiError, "Exception has to be type of Api error"
    result = db.session.execute(
        db.select(table).filter_by(**filter_by)
    )
    if many:
        r = result.scalars()
    else:
        r = result.scalar()
    if raise_exception and not r:
        raise raise_exception
    return r




