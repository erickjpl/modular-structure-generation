
from faker import Faker

from src.orders.domain.entities.seller import Seller
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject

fake = Faker()


class TestSeller:
  def test_should_create_seller(self):
    seller_id = SellerId(UuidValueObject.new().value)
    seller_name = SellerName(fake.name())

    seller = Seller(seller_id, seller_name)

    assert seller.to_primitives() == {
      "seller_id": seller_id.value,
      "seller_name": seller_name.value,
    }
