from flask import Blueprint, request, g
from flask_restful import Resource, Api
from . import service
from .schemas import ReviewSchema
from ..auth.decorators import auth_required, staff_only

reviews_bp = Blueprint("reviews_bp", __name__, url_prefix="/reviews")
api = Api(reviews_bp)


class ReviewController(Resource):

    @staff_only
    def get(self):
        reviews = service.get_all_reviews()
        return ReviewSchema().dump(reviews, many=True)

    @auth_required
    def post(self):
        review_data = ReviewSchema().load(request.json)
        review_data["user_id"] = g.user["id"]
        new_review = service.create_review(review_data)
        return ReviewSchema().dump(new_review)


class DetailReviewController(Resource):

    @auth_required
    def put(self, review_id):
        review_data = ReviewSchema().load(request.json)
        updated_review = service.update_review(review_id, g.user, review_data)
        return ReviewSchema().dump(updated_review)

    @auth_required
    def delete(self, review_id):
        removed_review = service.remove_review(review_id, g.user)
        return ReviewSchema(exclude=("user",)).dump(removed_review)


api.add_resource(ReviewController, "")
api.add_resource(DetailReviewController, "/<int:review_id>")





