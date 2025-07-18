from datetime import date, timedelta
import pytest
from faker import Faker

from src.orders.domain.value_objects.due_date import DueDate
from src.orders.domain.value_objects.issue_date import IssueDate

fake = Faker()


class TestDateValueObjects:
  def test_should_create_due_date(self):
    value = fake.future_date()
    due_date = DueDate(value)

    assert due_date.value.date() == value

  def test_should_raise_error_if_due_date_is_not_date_object(self):
    with pytest.raises(TypeError) as excinfo:
      DueDate("2024-12-31")

    assert "Due date must be a date object." in str(excinfo.value)

  def test_should_create_issue_date(self):
    value = fake.past_date()
    issue_date = IssueDate(value)

    assert issue_date.value.date() == value

  def test_should_raise_error_if_issue_date_is_not_date_object(self):
    with pytest.raises(TypeError) as excinfo:
      IssueDate("2023-01-01")

    assert "Issue date must be a date object." in str(excinfo.value)