from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    userId = Column(String(50), primary_key=True)
    name = Column(String(100))
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    
    userType = Column(String(50)) 

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': userType
    }

class Homeowner(User):
    __mapper_args__ = {
        'polymorphic_identity': 'homeowner',
    }

class Guest(User):
    __mapper_args__ = {
        'polymorphic_identity': 'guest',
    }

class Listing(Base):
    __tablename__ = 'listings'
    listingId = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    pricePerNight = Column(Float)
    location = Column(String)
    maxGuests = Column(Integer)
    availabilityStatus = Column(Boolean)
    ownerId = Column(String, ForeignKey('users.userId'))

class Booking(Base):
    __tablename__ = 'bookings'
    bookingId = Column(String, primary_key=True)
    listingId = Column(String, ForeignKey('listings.listingId'))
    guestId = Column(String, ForeignKey('users.userId'))
    checkInDate = Column(String)
    checkOutDate = Column(String)
    totalPrice = Column(Float)

