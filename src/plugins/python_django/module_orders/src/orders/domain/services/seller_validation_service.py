from typing import Protocol, runtime_checkable

from src.orders.domain.entities.seller import Seller
from src.orders.domain.value_objects.seller_id import SellerId


@runtime_checkable
class SellerValidationService(Protocol):
  def validate_seller(self, id: SellerId) -> Seller: ...
