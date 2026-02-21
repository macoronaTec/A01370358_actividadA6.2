
import uuid
import json
from typing import List
from modelos import Hotel, Customer
from exceptions import HotelError, CustomerError
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
            raise CustomerError("Name and email are required.")

        # Prevent duplicate email
        for customer in customers:
            if customer.email == email:
                raise CustomerError("Email already exists.")

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

        raise CustomerError("Customer not found.")

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

        raise CustomerError("Customer not found.")