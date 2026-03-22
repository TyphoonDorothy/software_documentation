from abc import ABC, abstractmethod
from typing import List, Dict
from data_access.models import User, Guest, Homeowner, Listing, Booking 

class IRepository(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> List[Dict]: pass

    @abstractmethod
    def save_entities(self, entities: List) -> bool: pass

class ProcessingService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def run_import_pipeline(self, file_path: str) -> str:
        raw_data = self.repository.read_csv(file_path)
        
        users = []
        listings = []
        bookings = []
        
        for row in raw_data:
            entity = self._map_to_model(row)
            if isinstance(entity, User):
                users.append(entity)
            elif isinstance(entity, Listing):
                listings.append(entity)
            elif isinstance(entity, Booking):
                bookings.append(entity)
        
        total_saved = 0
        
        if users:
            self.repository.save_entities(users)
            total_saved += len(users)
            
        if listings:
            self.repository.save_entities(listings)
            total_saved += len(listings)
            
        if bookings:
            self.repository.save_entities(bookings)
            total_saved += len(bookings)
            
        return f"Successfully processed and saved {total_saved} records."

    def _map_to_model(self, row: Dict):
        record_type = row.get('type', '').lower()
        
        record_type = row.get('type', '').lower()
    
        if record_type == 'user':
            user_id_int = int(row.get('id', 0))
        
            if user_id_int % 2 == 0:
                return Homeowner(
                    userId=str(user_id_int),
                    name=row.get('name'),
                    password="secure_password_123",
                    email=row.get('email')
                )
            else:
                return Guest(
                    userId=str(user_id_int),
                    name=row.get('name'),
                    password="guest_password_abc",
                    email=row.get('email')
                )
            
        elif record_type == 'listing':
            return Listing(
                listingId=row.get('id'),
                title=row.get('title'),
                description=row.get('description'),
                pricePerNight=float(row.get('pricePerNight', 0)),
                location=row.get('location'),
                maxGuests=int(row.get('maxGuests', 0)),
                availabilityStatus=row.get('availabilityStatus', 'True').lower() == 'true',
                ownerId=row.get('ownerId')
                )
                
        elif record_type == 'booking':
            return Booking(
                bookingId=row.get('bookingId'),
                listingId=row.get('listingId'),
                guestId=row.get('guestId'),
                checkInDate=row.get('checkInDate'), 
                checkOutDate=row.get('checkOutDate'),
                totalPrice=float(row.get('totalPrice', 0))
                )    
        return None