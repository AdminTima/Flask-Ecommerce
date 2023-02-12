from .api_error import ApiError


def handle_api_error(error):
    print(error, "is api error")
    return error.message, error.status


def handle_token_error(error):
    err = ApiError.unauthorized()
    return err.message, err.status


def handle_validation_error(error):
    return error.messages, 400

