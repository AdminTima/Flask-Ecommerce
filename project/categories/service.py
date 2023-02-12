from .models import Categories
from .. import base_repository


def create_category(category_data):
    return base_repository.create(Categories, category_data)


def get_all_categories():
    return base_repository.get_all(Categories)


def delete_category(category_id):
    return base_repository.get_by_id_and_remove(Categories, category_id)


def update_category(category_id, updated_data):
    return base_repository.get_by_id_and_update(Categories, category_id, updated_data)

