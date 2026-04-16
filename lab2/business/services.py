from abc import ABC, abstractmethod
from typing import List, Dict
from data_access.models import User, Guest, Homeowner, Listing, Booking
import uuid

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
    
class ListingService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_listings(self):
        """Logic to fetch all listings for the View"""
        session = self.repository.Session()
        return session.query(Listing).all()

    def get_listing_by_id(self, listing_id):
        session = self.repository.Session()
        return session.query(Listing).filter_by(listingId=listing_id).first()

    def delete_listing(self, listing_id):
        """Business logic for deleting a specific listing"""
        session = self.repository.Session()
        listing = session.query(Listing).filter_by(listingId=listing_id).first()
        if listing:
            session.delete(listing)
            session.commit()
            return True
        return False
    
    def create_listing(self, data):
        """Logic to create a new listing with validation"""
        new_listing = Listing(
            listingId=str(uuid.uuid4()),  
            title=data.get('title'),
            description=data.get('description'),
            pricePerNight=float(data.get('price', 0)),
            location=data.get('location'),
            maxGuests=int(data.get('maxGuests', 1)),
            availabilityStatus=True,
            ownerId=data.get('ownerId', '0') 
        )
        self.repository.save_entities([new_listing])
        return new_listing

    def update_listing(self, listing_id, data):
        """Logic to update an existing listing"""
        session = self.repository.Session()
        listing = session.query(Listing).filter_by(listingId=listing_id).first()
        if listing:
            listing.title = data.get('title')
            listing.pricePerNight = float(data.get('price', 0))
            listing.location = data.get('location')
            session.commit()
            return True
        return False