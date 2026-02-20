
import uuid
import json
from typing import List
from modelos import Hotel
from exceptions import HotelError
from storage import JsonStorage


class HotelService:
    """Servicio de operación del hotel."""

    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def _load_hotels(self) -> List[Hotel]:
        return [Hotel(**data) for data in self.storage.load()]

    def _save_hotels(self, hotels: List[Hotel]) -> None:
        hoteles_dict = [hotel.to_dict() for hotel in hotels]
        with open('data/hotels.json', 'w') as file:
            json.dump(hoteles_dict, file, indent=4)

    def create_hotel(self, name: str, location: str,
                     total_rooms: int) -> Hotel:
        hotels = self._load_hotels()
        hotel = Hotel(
            hotel_id=str(uuid.uuid4()),
            name=name,
            location=location,
            total_rooms=total_rooms,
            available_rooms=total_rooms
       )
        hotels.append(hotel)       
        self._save_hotels(hotels)
        return hotel
    
    def update_hotel(self, hotel_id: str, name: str, location: str,
                     total_rooms: int) -> Hotel:
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                print("Se actualizo la informacion del hotel: [" + hotel.name + "]")
                hotel.name = name
                hotel.location = location
                hotel.total_rooms = total_rooms
                hotel.available_rooms = total_rooms
                self._save_hotels(hotels)
                return hotel
        raise HotelError("Hotel no encontrado.")


    def delete_hotel(self, hotel_id: str) -> None:
        hotel_eliminado = self.get_hotel(hotel_id)
        print("Se elimino el hotel: [" + hotel_eliminado.name + "]")
        print("*"*40)
        hotels = self._load_hotels()
        filtered = [h for h in hotels if h.hotel_id != hotel_id]
        if len(filtered) == len(hotels):
            raise HotelError("Hotel no encontrado.")
        self._save_hotels(filtered)

    def get_hotel(self, hotel_id: str) -> Hotel:
        for hotel in self._load_hotels():
            if hotel.hotel_id == hotel_id:
                return hotel
        raise HotelError("Hotel no encontrado.")
    
    def show_hotels(self) -> Hotel:
        for hotel in self._load_hotels():
            #print("Hotel ID:", hotel.hotel_id)
            print("Nombre:", hotel.name)
            print("Ubicación:", hotel.location)
            print("Habitaciones totales:", hotel.total_rooms)
            print("Habitaciones disponibles:", hotel.available_rooms)
            print("*"*40)

    def reserve_room(self, hotel_id: str) -> None:
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                hotel.reserve_room()
                self._save_hotels(hotels)
                return
        raise HotelError("Hotel no encontrado.")