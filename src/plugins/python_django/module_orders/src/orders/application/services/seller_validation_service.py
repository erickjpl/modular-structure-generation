import asyncio
import logging
from datetime import datetime

import httpx

from src.orders.domain.entities.seller import Seller
from src.orders.domain.exceptions.seller_exceptions import (
  SellerInvalidDataFormatError,
  SellerNotFoundError,
  SellerValidationAttemptsExceededError,
)
from src.orders.domain.services.seller_validation_service import SellerValidationService
from src.orders.domain.value_objects.seller_id import SellerId

logger = logging.getLogger(__name__)


class HttpSellerValidationService(SellerValidationService):
  def __init__(
    self,
    base_url: str,
    api_key: str,
    timeout: float = 5.0,
    max_retries: int = 3,
    cache_ttl: int = 300,  # 5 minutos en segundos
  ):
    self.base_url = base_url.rstrip("/")
    self.api_key = api_key
    self.timeout = timeout
    self.max_retries = max_retries
    self.cache_ttl = cache_ttl
    self._client = httpx.AsyncClient()

    self._cache: dict[SellerId, tuple[Seller, datetime]] = {}

  def validate_seller(self, id: SellerId) -> Seller:
    cached_seller = self._get_from_cache(id)
    if cached_seller:
      return cached_seller

    seller = self._fetch_seller_with_retry(id)

    self._update_cache(id, seller)

    return seller

  def _get_from_cache(self, seller_id: SellerId) -> Seller | None:
    if seller_id in self._cache:
      seller, timestamp = self._cache[seller_id]

      if (datetime.now() - timestamp).total_seconds() < self.cache_ttl:
        return seller

      del self._cache[seller_id]
    return None

  def _update_cache(self, seller_id: SellerId, seller: Seller):
    self._cache[seller_id] = (seller, datetime.now())

  def _fetch_seller_with_retry(self, seller_id: SellerId) -> Seller:
    last_exception = None
    url = f"{self.base_url}/sellers/{seller_id}"
    headers = {"Authorization": f"Bearer {self.api_key}"}

    for attempt in range(1, self.max_retries + 1):
      try:
        response = self._client.get(url, headers=headers, timeout=self.timeout)

        if response.status_code == 404:
          raise SellerNotFoundError(seller_id)

        response.raise_for_status()

        return self._parse_seller_response(response.json())

      except (httpx.RequestError, httpx.HTTPStatusError) as ex:
        last_exception = ex
        logger.warning(f"Attempt {attempt} failed for seller {seller_id}: {str(ex)}")
        if attempt < self.max_retries:
          asyncio.sleep(attempt * 0.5)

    logger.error(f"All retries failed for seller {seller_id.value}")
    raise SellerValidationAttemptsExceededError(seller_id, self.max_retries) from last_exception

  def _parse_seller_response(self, response_data: dict) -> Seller:
    try:
      return Seller(
        id=str(response_data["id"]),
        name=str(response_data["name"]),
        is_active=bool(response_data["is_active"]),
        last_updated=datetime.now(),
      )
    except (KeyError, TypeError) as ex:
      raise SellerInvalidDataFormatError() from ex

  def close(self):
    self._client.aclose()
