from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName


class Seller:
  def __init__(self, seller_id: SellerId, seller_name: SellerName):
    self._seller_id = seller_id
    self._seller_name = seller_name

  def to_primitives(self) -> any:
    return {
      "seller_id": self._seller_id.value,
      "seller_name": self._seller_name.value,
    }

  def __repr__(self) -> str:
    return f"Seller(id={self._seller_id.value!r}, seller_name={self._seller_name.value!r})"
