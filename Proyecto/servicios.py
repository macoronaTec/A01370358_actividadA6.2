
import uuid
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
        self.storage.save([hotel.to_dict() for hotel in hotels])

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

    def delete_hotel(self, hotel_id: str) -> None:
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

    def reserve_room(self, hotel_id: str) -> None:
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                hotel.reserve_room()
                self._save_hotels(hotels)
                return
        raise HotelError("Hotel no encontrado.")