from src.orders.domain.value_objects.seller_id import SellerId


class SellerException(Exception):
  pass


class SellerNotFoundError(SellerException):
  def __init__(self, seller_id: SellerId):
    super().__init__(f"Seller {seller_id.value} not found")


class SellerValidationAttemptsExceededError(SellerException):
  def __init__(self, seller_id: SellerId, attempts: int, inner_exception: Exception = None):
    message = f"Failed to validate seller {seller_id.value} after {attempts} attempts."
    super().__init__(message)

    if inner_exception:
      self.__cause__ = inner_exception


class SellerInvalidDataFormatError(SellerException):
  def __init__(self):
    super().__init__("Invalid seller data format in response")
