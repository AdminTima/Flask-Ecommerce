

class ApiError(Exception):

    def __init__(self, status, message):
        self.status = status
        self.message = message

    @staticmethod
    def not_found(message="Not found"):
        return ApiError(404, message)

    @staticmethod
    def unauthorized(message="Unauthorized"):
        return ApiError(401, message)

    @staticmethod
    def bad_request(message="Bad request"):
        return ApiError(400, message)

    @staticmethod
    def forbidden(message="Forbidden"):
        return ApiError(403, message)
