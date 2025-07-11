from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR


def api_response(
    success: bool, message: str, data=None, error=None, status_code=HTTP_200_OK
):
    """
    Standardizes the API response format.
    """
    response_data = {
        "success": success,
        "message": message,
        "data": data,
        "error": error,
    }
    return Response(response_data, status=status_code)


def success_response(
    message: str = "Operation successful", data=None, status_code=HTTP_200_OK
):
    """
    Generates a success API response.
    """
    return api_response(True, message, data, None, status_code)


def error_response(
    message: str = "An error occurred",
    code: int = 500,
    type: str = "InternalError",
    details: str = "Something went wrong.",
    extra=None,
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
):
    """
    Generates an error API response.
    """
    error_detail = {"code": code, "type": type, "details": details, "extra": extra}
    return api_response(False, message, None, error_detail, status_code)
