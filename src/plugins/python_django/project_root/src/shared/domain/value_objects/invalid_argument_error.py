from src.shared.domain.exceptions.domain_exception import HTTP_400_BAD_REQUEST, DomainException


class InvalidArgumentError(DomainException):
  def __init__(self, message: str, extra_data: dict | None = None):
    super().__init__(
      detail=message,
      status_code=HTTP_400_BAD_REQUEST,
      default_message=f"The arguments provided by the <{self.__class__.__name__}> are not valid.",
      extra_data=extra_data,
    )
