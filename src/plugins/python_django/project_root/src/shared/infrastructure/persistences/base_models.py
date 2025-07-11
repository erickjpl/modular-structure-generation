from uuid import uuid4

from django.db.models import DateTimeField, Model, UUIDField


class BaseDAO(Model):
  id = UUIDField(primary_key=True, default=uuid4, editable=False)
  created_by = UUIDField(editable=False)
  created_at = DateTimeField(auto_now_add=True)
  updated_by = UUIDField(editable=False)
  updated_at = DateTimeField(auto_now=True)
  deleted_by = UUIDField(editable=False, null=True, blank=True)
  deleted_at = DateTimeField(null=True, blank=True)

  class Meta:
    abstract = True
