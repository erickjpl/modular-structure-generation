# from src.common.infrastructure.persistence.uow import AbstractUnitOfWork  # Asumimos una UoW abstracta
# from src.modules.users.application.commands.create_user import CreateUserCommand
# from src.modules.users.domain.repositories.user_repository import UserRepository
# from src.modules.users.domain.services.user_domain_service import UserDomainService

from src.orders.application.commands.create.create_order_command import CreateOrderCommand
from src.orders.application.commands.create.order_creator_service import OrderCreatorService
from src.shared.domain.commands.command_handler import CommandHandler


class CreateOrderCommandHandler(CommandHandler):
  def __init__(self, service: OrderCreatorService):
    self.service = service

  def subscribed_to(self) -> type[CreateOrderCommand]:
    return CreateOrderCommand

  def handle(self, command: CreateOrderCommand) -> None:
    self.service.run(
      order_id=command.order_id,
      order_number=command.order_number,
      customer_id=command.customer_id,
      customer_name=command.customer_name,
      seller_id=command.seller_id,
      seller_name=command.seller_name,
      ip_address=command.ip_address,
      source=command.source,
      currency=command.currency,
      items=command.items,
    )


# class CreateOrderCommandHandler(CommandHandler):
#   def __init__(
#     self, user_repository: UserRepository, user_domain_service: UserDomainService, unit_of_work: AbstractUnitOfWork
#   ):

#   def handle(self, command: CreateUserCommand) -> None:
#     with self._unit_of_work:
#       # 1. Validar la unicidad del username y email a nivel de dominio
#       #    El servicio de dominio se encarga de esta lógica
#       new_username_vo = Username(command.username)
#       new_email_vo = Email(command.email)

#       self._user_domain_service.register_new_user(
#         User(  # Creamos una "instancia temporal" para las validaciones
#           user_id=UUID.new(),  # UUID temporal, no se guardará
#           username=new_username_vo,
#           email=new_email_vo,
#           password=Password("dummy_hash"),  # Contraseña dummy para la validación inicial
#           full_name=FullName(command.first_name, command.last_name),
#           age=Age(command.age),
#         )
#       )

#       # 2. Hash de la contraseña (esto es lógica de aplicación o infraestructura, no de dominio puro)
#       hashed_password = bcrypt.hashpw(command.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#       password_vo = Password(hashed_password)

#       # 3. Crear el agregado de usuario (entidad de dominio)
#       user = User(
#         user_id=UUID.new(),
#         username=new_username_vo,
#         email=new_email_vo,
#         password=password_vo,
#         full_name=FullName(command.first_name, command.last_name),
#         age=Age(command.age),
#         is_active=command.is_active,
#         created_at=datetime.utcnow(),
#         updated_at=datetime.utcnow(),
#       )

#       # 4. Persistir el usuario usando el repositorio
#       self._user_repository.save(user)

#       # 5. Publicar eventos de dominio si los hay (después de la persistencia)
#       #    Esto se haría a través del bus de eventos en la UoW o por separado
#       #    for event in user.domain_events:
#       #        self._event_bus.publish(event)
#       #    user.clear_domain_events() # Limpiar eventos después de publicarlos

#       self._unit_of_work.commit()  # Confirmar la transacción

#       # 6. Retornar un DTO de salida
#       return UserDTO.from_entity(user)
