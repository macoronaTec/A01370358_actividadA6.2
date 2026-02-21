
import uuid
import json
from typing import List
from modelos import Hotel, Customer, Reservation
from exceptions import HotelError, CustomerError, ReservationError
from modelos import Reservation
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
    
class CustomerService:
    """Servicio de operaciones de los clientes."""

    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def _load_customers(self) -> List[Customer]:
        """Load customers from storage."""
        return [Customer(**data) for data in self.storage.load()]

    def _save_customers(self, customers: List[Customer]) -> None:
        clientes_dict = [customer.to_dict() for customer in customers]
        with open('data/clientes.json', 'w') as file:
            json.dump(clientes_dict, file, indent=4)

    def create_customer(self, name: str, email: str) -> Customer:
        """Create a new customer."""
        customers = self._load_customers()

        if not name or not email:
            raise CustomerError("Name y email son requeridos.")

        # Prevent duplicate email
        for customer in customers:
            if customer.email == email:
                raise CustomerError("Email ya existe.")

        new_customer = Customer(
            customer_id=str(uuid.uuid4()),
            name=name,
            email=email
        )

        print("nuevo cliente creado: [" + new_customer.name + "]")
        customers.append(new_customer)
        self._save_customers(customers)
        return new_customer 
    
    def show_customers(self) -> Customer:
        print("=== Mostrar Clientes ===")
        for customer in self._load_customers():
            print("Cliente ID:", customer.customer_id)
            print("Nombre:", customer.name)
            print("Email:", customer.email)
            print("*"*40)

    def delete_customer(self, customer_id: str) -> None:
        """Delete an existing customer."""
        customers = self._load_customers()
        customer_eliminado = self.get_customer(customer_id)
        print("Se elimino el cliente: [" + customer_eliminado.name + "]")
        print("*"*40)
        filtered = [
            customer for customer in customers
            if customer.customer_id != customer_id
        ]

        if len(filtered) == len(customers):
            raise CustomerError("Cliente no encontrado.")

        self._save_customers(filtered)

    def get_customer(self, customer_id: str) -> Customer:
        """Retrieve a customer by ID."""
        for customer in self._load_customers():
            if customer.customer_id == customer_id:
                return customer

        raise CustomerError("Cliente no encontrado.")

    def update_customer(self, customer_id: str,
                        name: str = None,
                        email: str = None) -> Customer:
        """Update customer information."""
        customers = self._load_customers()

        for customer in customers:
            if customer.customer_id == customer_id:
                print("Se actualizo la informacion del cliente: [" + customer.name + "]")
                if name:
                    customer.name = name
                if email:
                    customer.email = email

                self._save_customers(customers)
                return customer

        raise CustomerError("Cliente no encontrado.")
    
class ReservationService:
    """Service for reservation operations."""

    def __init__(self,
                 storage: JsonStorage,
                 hotel_service: HotelService,
                 customer_service: CustomerService):
        self.storage = storage
        self.hotel_service = hotel_service
        self.customer_service = customer_service

    def _load_reservations(self) -> List[Reservation]:
        """Load reservations from storage."""
        return [
            Reservation(**data)
            for data in self.storage.load()
        ]

    def _save_reservations(self,
                           reservations: List[Reservation]) -> None:
        """Save reservations to storage."""
        self.storage.save([
            reservation.to_dict()
            for reservation in reservations
        ])

    def create_reservation(self,
                           customer_id: str,
                           hotel_id: str) -> Reservation:
        """Create a reservation."""

        # Validate customer exists
        try:
            self.customer_service.get_customer(customer_id)
        except CustomerError as error:
            raise ReservationError(str(error)) from error

        # Validate hotel exists
        try:
            self.hotel_service.get_hotel(hotel_id)
        except HotelError as error:
            raise ReservationError(str(error)) from error

        # Reserve room
        try:
            self.hotel_service.reserve_room(hotel_id)
        except ValueError as error:
            raise ReservationError(str(error)) from error

        reservations = self._load_reservations()

        new_reservation = Reservation(
            reservation_id=str(uuid.uuid4()),
            customer_id=customer_id,
            hotel_id=hotel_id
        )

        reservations.append(new_reservation)
        self._save_reservations(reservations)

        return new_reservation

    def cancel_reservation(self, reservation_id: str) -> None:
        """Cancel an existing reservation."""
        reservations = self._load_reservations()

        for reservation in reservations:
            if reservation.reservation_id == reservation_id:

                # Free room in hotel
                hotel = self.hotel_service.get_hotel(
                    reservation.hotel_id
                )
                hotel.cancel_reservation()

                # Update hotel persistence
                hotels = self.hotel_service._load_hotels()
                for stored in hotels:
                    if stored.hotel_id == hotel.hotel_id:
                        stored.available_rooms = hotel.available_rooms

                self.hotel_service._save_hotels(hotels)

                # Remove reservation
                updated = [
                    res for res in reservations
                    if res.reservation_id != reservation_id
                ]

                self._save_reservations(updated)
                return

        raise ReservationError("Reservation not found.")
    
class ReservationService:
    """Service for reservation operations."""

    def __init__(self,
                 storage: JsonStorage,
                 hotel_service: HotelService,
                 customer_service: CustomerService):
        self.storage = storage
        self.hotel_service = hotel_service
        self.customer_service = customer_service

    def _load_reservations(self) -> List[Reservation]:
        """Load reservations from storage."""
        return [
            Reservation(**data)
            for data in self.storage.load()
        ]

    def _save_reservations(self,
                           reservations: List[Reservation]) -> None:
        """Save reservations to storage."""
        self.storage.save([
            reservation.to_dict()
            for reservation in reservations
        ])

    def create_reservation(self,
                           customer_id: str,
                           hotel_id: str) -> Reservation:
        """Create a reservation."""

        # Validate customer exists
        try:
            cliente = self.customer_service.get_customer(customer_id)
            print("La reservación es a nombre de: [" + cliente.name + "] con id: [" + cliente.customer_id + "]")
        except CustomerError as error:
            raise ReservationError(str(error)) from error

        # Validate hotel exists
        try:
            hotel =self.hotel_service.get_hotel(hotel_id)
            print("En el hotel: [" + hotel.name + "]")
        except HotelError as error:
            raise ReservationError(str(error)) from error

        # Reserve room
        try:
            self.hotel_service.reserve_room(hotel_id)
            print("Se reservo una habitación")
        except ValueError as error:
            raise ReservationError(str(error)) from error

        reservations = self._load_reservations()

        new_reservation = Reservation(
            reservation_id=str(uuid.uuid4()),
            customer_id=customer_id,
            hotel_id=hotel_id
        )

        reservations.append(new_reservation)
        self._save_reservations(reservations)

        return new_reservation

    def cancel_reservation(self, reservation_id: str) -> None:
        """Cancel an existing reservation."""
        reservations = self._load_reservations()

        for reservation in reservations:
            if reservation.reservation_id == reservation_id:

                # Free room in hotel
                hotel = self.hotel_service.get_hotel(
                    reservation.hotel_id
                )
                hotel.cancel_reservation()
                print("Se cancelo la reservación con id: [" + reservation_id + "]")

                # Update hotel persistence
                hotels = self.hotel_service._load_hotels()
                for stored in hotels:
                    if stored.hotel_id == hotel.hotel_id:
                        stored.available_rooms = hotel.available_rooms

                self.hotel_service._save_hotels(hotels)

                # Remove reservation
                updated = [
                    res for res in reservations
                    if res.reservation_id != reservation_id
                ]

                self._save_reservations(updated)
                return

        raise ReservationError("Reservation not found.")