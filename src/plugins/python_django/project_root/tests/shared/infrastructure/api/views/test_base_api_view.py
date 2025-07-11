# tests/shared/infrastructure/api/views/test_base_api_view.py


import pytest

# Importa tus excepciones
from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException

# Importa la clase BaseAPIView
from src.shared.infrastructure.api.views.base_api_view import BaseAPIView

# --- Mocks de Serializers para los Tests ---


# Mock para simular un Request Serializer válido
class MockRequestSerializerValid:
  def __init__(self, data=None, partial=False):  # Añadido data=None para evitar errores si se llama sin data
    self.data = data
    self.partial = partial
    self.validated_data = {"processed_data": data} if data is not None else {}  # Ajustado para None
    self.errors = {}

  def is_valid(self, raise_exception=False):
    return True


# Mock para simular un Request Serializer inválido
class MockRequestSerializerInvalid:
  def __init__(self, data=None, partial=False):  # Añadido data=None
    self.data = data
    self.partial = partial
    self.validated_data = {}
    self.errors = {"field_name": ["This field is required."], "other_field": ["Invalid format."]}

  def is_valid(self, raise_exception=False):
    return False


# Mock para simular un Response Serializer válido
class MockResponseSerializerValid:
  def __init__(self, data=None, many=False, instance=None):  # Añadido instance=None
    self.data = {"serialized_response": data if data is not None else instance}
    self.many = many
    self.instance = instance

  def is_valid(self, raise_exception=False):
    return True


# Mock para simular un Response Serializer inválido (ej. si los datos de entrada al serializer no son correctos)
class MockResponseSerializerInvalid:
  def __init__(self, data=None, many=False, instance=None):  # Añadido instance=None
    self.data = {}
    self.many = many
    self.instance = instance
    self.errors = {"detail": "Invalid input for response serialization."}

  def is_valid(self, raise_exception=False):
    return False


# --- Clase de prueba que hereda de BaseAPIView ---
class MyTestAPIView(BaseAPIView):
  pass


class TestBaseAPIView:
  def setup_method(self):
    self.view = MyTestAPIView()

  # --- Tests para _validate_request_serializer ---

  def test_validate_request_serializer_raises_error_if_not_defined(self):
    self.view.request_serializer_class = None
    with pytest.raises(InternalServerErrorException) as excinfo:
      self.view._validate_request_serializer({"key": "value"})
    assert "request_serializer_class debe ser definido para esta vista." in excinfo.value.detail

  def test_validate_request_serializer_returns_validated_data_on_success(self):
    self.view.request_serializer_class = MockRequestSerializerValid
    test_data = {"name": "Test", "value": 123}
    validated_data = self.view._validate_request_serializer(test_data)
    assert validated_data == {"processed_data": test_data}

  def test_validate_request_serializer_raises_unprocessable_entity_on_invalid_data(self):
    self.view.request_serializer_class = MockRequestSerializerInvalid
    invalid_data = {}
    with pytest.raises(UnprocessableEntityException) as excinfo:
      self.view._validate_request_serializer(invalid_data)
    assert "Error de validación en los datos de entrada." in excinfo.value.detail
    assert excinfo.value.extra_data == {"field_name": ["This field is required."], "other_field": ["Invalid format."]}

  def test_validate_request_serializer_passes_partial_flag(self, mocker):  # <-- Añade 'mocker' aquí
    # Given
    # Mockeamos la CLASE MockRequestSerializerValid para poder inspeccionar sus llamadas
    # No estamos parchando 'base_api_view', sino la referencia que asignamos al view.
    # Creamos un mock de la clase, y lo asignamos como serializer_class
    mock_serializer_class = mocker.Mock(spec=MockRequestSerializerValid)
    # Configuramos el mock de la instancia que crearía el serializer
    mock_instance = mock_serializer_class.return_value  # Esto es lo que devuelve MockRequestSerializerValid()
    mock_instance.is_valid.return_value = True
    mock_instance.validated_data = {"processed_data": {"name": "Test Partial"}}

    self.view.request_serializer_class = mock_serializer_class
    test_data = {"name": "Test Partial"}

    # When
    self.view._validate_request_serializer(test_data, partial=True)

    # Then
    # Verificamos que la CLASE serializer fue instanciada con partial=True
    mock_serializer_class.assert_called_once_with(data=test_data, partial=True)

  # --- Tests para _validate_response_serializer ---

  def test_validate_response_serializer_raises_error_if_not_defined(self):
    self.view.response_serializer_class = None
    with pytest.raises(InternalServerErrorException) as excinfo:
      self.view._validate_response_serializer({"key": "value"})
    assert "response_serializer_class debe ser definido para esta vista." in excinfo.value.detail

  def test_validate_response_serializer_returns_serialized_data_on_success(self):
    self.view.response_serializer_class = MockResponseSerializerValid
    test_data = {"id": 1, "name": "Item"}
    serialized_data = self.view._validate_response_serializer(test_data)
    assert serialized_data == {"serialized_response": test_data}

  def test_validate_response_serializer_passes_many_flag(self, mocker):  # <-- Añade 'mocker' aquí
    # Given
    # Mockeamos la CLASE MockResponseSerializerValid
    mock_serializer_class = mocker.Mock(spec=MockResponseSerializerValid)
    mock_instance = mock_serializer_class.return_value
    mock_instance.is_valid.return_value = True
    mock_instance.data = {"serialized_response": [{"id": 1}, {"id": 2}]}  # Configura el 'data' del mock de la instancia

    self.view.response_serializer_class = mock_serializer_class
    test_data_list = [{"id": 1}, {"id": 2}]

    # When
    self.view._validate_response_serializer(test_data_list, many=True)

    # Then
    # Verificamos que la CLASE serializer fue instanciada con many=True
    mock_serializer_class.assert_called_once_with(instance=test_data_list, many=True)
