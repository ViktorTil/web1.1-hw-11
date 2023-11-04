from typing import List
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, Path, status, APIRouter

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse
from src.services.utils import next_seven_days

router = APIRouter(prefix="/contacts", tags= ["contacts"])

@router.get("/", response_model=List[ContactResponse], name="List of contacts")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts

@router.get("/birthday", response_model=List[ContactResponse], name="List of contacts")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return next_seven_days(contacts)

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact

@router.get("/first_name/{first_name}", response_model=ContactResponse)
async def get_contact_by_first_name(first_name: str , db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_first_name(first_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact

@router.get("/last_name/{last_name}", response_model=ContactResponse)
async def get_contact_by_last_name(last_name: str , db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact

@router.get("/email/{email}", response_model=ContactResponse)
async def get_contact_by_email(email: str , db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = 'Email is exist!')
    contact = await repository_contacts.create(body, db)
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel,contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact