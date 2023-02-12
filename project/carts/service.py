from .models import Carts, CartItems
from ..extensions import db
from .. import base_repository
from ..api_error import ApiError
from ..products import service as products_service


def create_cart(user_id):
    cart_in_db = base_repository.find(Carts, {"user_id": user_id})
    if cart_in_db:
        return cart_in_db
    return base_repository.create(Carts, {"user_id": user_id})


def get_user_cart(user_id):
    user_cart = base_repository.find(Carts, {"user_id": user_id}, raise_exception=ApiError.not_found("No user cart"))
    return user_cart


def add_cart_item(user_id, cart_item_data):
    user_cart = get_user_cart(user_id)
    base_repository.get_by_id_and_update(Carts, user_cart.id, {
        "total_sum": user_cart.total_sum + cart_item_data["total_sum"]
    })
    product_in_cart = base_repository.find(CartItems, {
        "cart_id": user_cart.id,
        "product_id": cart_item_data["product_id"]
    })
    if product_in_cart:
        product_in_cart.amount += 1
        product_in_cart.total_sum += cart_item_data["total_sum"]
        db.session.commit()
        db.session.refresh(product_in_cart)
        return product_in_cart
    new_cart_item = base_repository.create(CartItems, {
        "cart_id": user_cart.id,
        "product_id": cart_item_data["product_id"],
        "total_sum": cart_item_data["total_sum"],
    })
    return new_cart_item


def remove_cart_item(cart_item_id, user):
    user_cart = get_user_cart(user["id"])
    cart_item_in_db = base_repository.find(CartItems, {
        "id": cart_item_id,
        "cart_id": user_cart.id,
    }, raise_exception=ApiError.not_found("No such cart item"))
    updated_total = user_cart.total_sum - cart_item_in_db.total_sum
    base_repository.get_by_id_and_update(Carts, user_cart.id, {
        "total_sum": updated_total if updated_total >= 0 else 0
    })
    db.session.delete(cart_item_in_db)
    db.session.commit()
    return user_cart


def edit_cart_item_product_amount(cart_item_id, user, amount):
    user_cart = get_user_cart(user["id"])
    cart_item_in_db = base_repository.find(CartItems, {
        "id": cart_item_id,
        "cart_id": user_cart.id,
    }, raise_exception=ApiError.not_found("Not found such cart item"))
    cart_item_total_sum = cart_item_in_db.total_sum
    updated_cart_item = base_repository.get_by_id_and_update(CartItems, cart_item_id, {
        "amount": amount,
        "total_sum": cart_item_in_db.product.price * amount
    })
    updated_total = user_cart.total_sum - cart_item_total_sum + updated_cart_item.total_sum
    base_repository.get_by_id_and_update(Carts, user_cart.id, {
        "total_sum": updated_total if updated_total >= 0 else 0
    })
    return user_cart


def get_all_carts():
    return base_repository.get_all(Carts)


def remove_user_cart(user_id):
    cart = base_repository.find(Carts, {"user_id": user_id}, raise_exception=ApiError.not_found("No cart"))
    return base_repository.get_by_id_and_remove(Carts, cart.id)


def buy(user_id):
    cart = get_user_cart(user_id)
    products_ids = map(lambda cart_item: cart_item.product_id, cart.cart_items)
    return products_service.increment_bought_times(list(products_ids))






