from servicios import HotelService
from storage import JsonStorage
from pathlib import Path

"""Run example workflow."""

script_location = Path(__file__).parent
ARCHIVO_HOTELES = 'data/hotels.json'
file_location = script_location / ARCHIVO_HOTELES
print(file_location)
# Initialize storage
hotel_storage = JsonStorage(file_location)

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
print(hotel)

#print("=== Actualizar Hotel ===")
#id_hotel =  "d7d9b2b6-0c38-4754-b2a3-1a7b24c42637"
#hotel_service.update_hotel(
#    hotel_id=id_hotel,
#    name="Marriot Los Cabos",
#    location="México",
#    total_rooms=6
#)

print("=== Eliminar un Hotel ===")
id_hotel =  "g7d9b2b6-0c38-4754-b2a3-1a7b24c42645"
hotel_service.delete_hotel(id_hotel)


print("=== Mostrar Hoteles ===")
hotel_service.show_hotels()
