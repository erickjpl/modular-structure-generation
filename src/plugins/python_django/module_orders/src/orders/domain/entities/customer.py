from src.orders.domain.value_objects.customer_email import CustomerEmail
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError


class Customer:
  def __init__(self, customer_id: CustomerId, name: CustomerName, email: CustomerEmail):
    self._customer_id = customer_id
    self._name = name
    self._email = email

  @property
  def customer_id(self) -> CustomerId:
    return self._customer_id

  @property
  def name(self) -> CustomerName:
    return self._name

  @property
  def email(self) -> CustomerEmail:
    return self._email

  def update_name(self, new_name: CustomerName) -> None:
    if not isinstance(new_name, CustomerName):
      raise InvalidArgumentError("new_name must be a CustomerName object")
    self._name = new_name

  def __eq__(self, other: any) -> bool:
    if not isinstance(other, Customer):
      return NotImplemented
    return self._customer_id == other.customer_id

  def __hash__(self) -> int:
    return hash(self._customer_id)

  def __repr__(self) -> str:
    return f"Customer(id={self._customer_id.value!r}, name={self._name.value!r}, email={self._email.value!r})"
