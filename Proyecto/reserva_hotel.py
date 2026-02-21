"""Modulo de reserva hotelera"""

from pathlib import Path
from servicios import HotelService, CustomerService, ReservationService
from storage import JsonStorage


script_location = Path(__file__).parent
ARCHIVO_HOTELES = 'data/hotels.json'
file_location = script_location / ARCHIVO_HOTELES
# print(file_location)
# Initialize storage
hotel_storage = JsonStorage(file_location)

# Hoteles
# Initialize services
print("=== Mostrar Hoteles ===")
hotel_service = HotelService(hotel_storage)
hotel_service.show_hotels()

print("=== Crear un Hotel ===")
hotel = hotel_service.create_hotel(
    name="Marriot Cancun",
    location="México",
    total_rooms=5
)
# print(hotel)

print("=== Actualizar Hotel ===")
ID_HOTEL = "d7d9b2b6-0c38-4754-b2a3-1a7b24c42637"
hotel_service.update_hotel(
    hotel_id=ID_HOTEL,
    name="Marriot Los Cabos",
    location="México",
    total_rooms=6
)

print("=== Eliminar un Hotel ===")
ID_HOTEL = "g7d9b2b6-0c38-4754-b2a3-1a7b24c42645"
hotel_service.delete_hotel(ID_HOTEL)

print("=== Mostrar Hoteles ===")
hotel_service.show_hotels()

# Clientes
ARCHIVO_CLIENTES = 'data/clientes.json'
file_location = script_location / ARCHIVO_CLIENTES
# Initialize storage
customer_storage = JsonStorage(file_location)
# Hoteles
# Initialize services
customer_service = CustomerService(customer_storage)
# customer_service.show_customers()

print("=== Agregar un cliente ===")
customer = customer_service.create_customer(
    name="Fernando Calzada",
    email="fernando@example.com"
)

customer_service.show_customers()

print("=== Actualizar Cliente ===")
ID_CLIENTE = "C002"
customer_service.update_customer(
    customer_id=ID_CLIENTE,
    name="Roberto Canales",
    email="canales@example.com"
)

print("=== Eliminar un Cliente ===")
ID_CLIENTE = "C001"
customer_service.delete_customer(ID_CLIENTE)

# Reservaciones
ARCHIVO_RESERVAS = 'data/reservas.json'
file_location = script_location / ARCHIVO_RESERVAS

# Initialize storage
reservation_storage = JsonStorage(file_location)

# Initialize services
reservation_service = ReservationService(
    reservation_storage,
    hotel_service,
    customer_service
)

print("=== Crear una reservación ===")
ID_HOTEL = "g7d9b2b6-0c38-4754-b2a3-1a7b24c42645"
reservacion = reservation_service.create_reservation(
        customer.customer_id,
        ID_HOTEL
)

print(reservacion)
print("\n=== Hotel después de la reservación ===")
updated_hotel = hotel_service.get_hotel(ID_HOTEL)
print(updated_hotel)

print("\n=== Cancelar la reservación ===")
reservation_service.cancel_reservation(reservacion.reservation_id)

print("\n=== Hotel después de la reservación cancelada ===")
updated_hotel = hotel_service.get_hotel(ID_HOTEL)
print(updated_hotel)
