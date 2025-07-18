import json

from channels.generic.websocket import AsyncWebsocketConsumer

from src.modules.users.application.commands.create_user import CreateUserCommand

# Para inyectar dependencias de forma asíncrona, usar un patrón DI asíncrono
# O si es simple, instanciar directamente como en el ejemplo de UserAPIView.
# Asumimos que user_app_service está disponible aquí (ej. vía DI o global singleton).
from src.modules.users.application.services.user_app_service import (
  user_app_service,
)  # Usamos la instancia global del ejemplo de la vista


class UserConsumer(AsyncWebsocketConsumer):
  def connect(self):
    # Lógica al conectar un cliente WebSocket
    self.accept()

  def disconnect(self, close_code):
    # Lógica al desconectar
    pass

  def receive(self, text_data=None, bytes_data=None):
    """
    Recibe mensajes del WebSocket.
    Podría interpretar un mensaje como un comando para la aplicación.
    """
    text_data_json = json.loads(text_data)
    message_type = text_data_json.get("type")

    if message_type == "create_user":
      try:
        username = text_data_json["username"]
        email = text_data_json["email"]
        password = text_data_json["password"]
        first_name = text_data_json["first_name"]
        last_name = text_data_json["last_name"]
        age = text_data_json["age"]

        command = CreateUserCommand(
          username=username, email=email, password=password, first_name=first_name, last_name=last_name, age=age
        )
        user_dto = user_app_service.create_user(command)
        self.send(
          text_data=json.dumps(
            {
              "status": "success",
              "user": user_dto.__dict__,  # Convierte DTO a dict para JSON
            }
          )
        )
      except Exception as e:
        self.send(text_data=json.dumps({"status": "error", "message": str(e)}))
    else:
      self.send(text_data=json.dumps({"status": "error", "message": "Unknown message type"}))

  # Puedes añadir métodos para manejar mensajes enviados por el bus de eventos si el consumidor es un listener
  # def user_created_message(self, event):
  #     user_id = event['user_id']
  #     username = event['username']
  #     self.send(text_data=json.dumps({
  #         'type': 'user_created_notification',
  #         'user_id': user_id,
  #         'username': username
  #     }))
