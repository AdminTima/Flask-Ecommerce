import os
from .models import Products
from ..api_error import ApiError
from .. import base_repository
import uuid
from ..extensions import db
from sqlalchemy import update


def get_photo_from_files(files):
    if "photo" not in files:
        return False
    photo = files["photo"]
    if photo.filename == "":
        return False
    return files["photo"]


def save_photo(photo):
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join("project/images/", filename)
    photo.save(file_path)
    return f"images/{filename}"


def create_product(product_data, files):
    photo = get_photo_from_files(files)
    if not photo:
        raise ApiError(400, "No photo")
    photo_path = save_photo(photo)
    product_data["photo"] = photo_path
    return base_repository.create(Products, product_data)


def get_product(product_id):
    return base_repository.get_by_id(Products, product_id)


def delete_product(product_id):
    return base_repository.get_by_id_and_remove(Products, product_id)


def update_product(product_id, updated_data, files):
    photo = get_photo_from_files(files)
    if photo:
        photo_path = save_photo(photo)
        updated_data["photo"] = photo_path
    return base_repository.get_by_id_and_update(
        Products, product_id, updated_data
    )


def get_all_products():
    return base_repository.get_all(Products)


def increment_bought_times(products_ids):
    query = update(Products).where(Products.id.in_(products_ids)).values(
        bought_times=Products.bought_times + 1,
    ).returning(Products.bought_times)
    result = db.session.execute(query).fetchall()
    db.session.commit()
    return result




