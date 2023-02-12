from .models import Reviews
from ..api_error import ApiError
from .. import base_repository


def create_review(review_data):
    return base_repository.create(Reviews, review_data)


def remove_review(review_id, user):
    if user.get("is_staff", None):
        return base_repository.get_by_id_and_remove(Reviews, review_id)
    review_in_db = base_repository.get_by_id(Reviews, review_id)
    if review_in_db.user_id != user["id"]:
        raise ApiError(403, "You can't perform this action")
    return base_repository.get_by_id_and_remove(Reviews, review_id)


def update_review(review_id, user, review_data):
    review_in_db = base_repository.get_by_id(Reviews, review_id)
    if review_in_db.user_id != user["id"]:
        raise ApiError(403, "You can't perform this action")
    return base_repository.get_by_id_and_update(Reviews, review_id, review_data)


def get_all_reviews():
    return base_repository.get_all(Reviews)

