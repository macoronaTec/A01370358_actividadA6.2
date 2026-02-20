from dataclasses import dataclass, asdict
from typing import Dict

@dataclass
class Hotel:
    """datos del hotel."""
    hotel_id: str
    name: str
    location: str
    total_rooms: int
    available_rooms: int

    def reserve_room(self) -> None:
        """Reservar una habitación."""
        if self.available_rooms <= 0:
            raise ValueError("No hay disponibilidad de habitaciones.")
        self.available_rooms -= 1

    def cancel_reservation(self) -> None:
        """Cancelar una reservación."""
        if self.available_rooms >= self.total_rooms:
            raise ValueError("Todos los cuartos están disponibles.")
        self.available_rooms += 1

    def to_dict(self) -> Dict:
        """Conversión a diccionario."""
        return asdict(self)
    
@dataclass
class Customer:
    """Datos cliente."""
    customer_id: str
    name: str
    email: str

    def to_dict(self) -> Dict:
        """Conversión a diccionario."""
        return asdict(self)


@dataclass
class Reservation:
    """Datos reservación."""
    reservation_id: str
    customer_id: str
    hotel_id: str

    def to_dict(self) -> Dict:
        """Conversión a diccionario."""
        return asdict(self)