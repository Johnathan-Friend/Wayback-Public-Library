from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


def get_transaction(db: Session, transaction_id: int) -> Optional[models.Transactions]:
    return db.query(models.Transactions).filter(models.Transactions.TransactionID == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Transactions]:
    return db.query(models.Transactions).offset(skip).limit(limit).all()

# -----------------
# --- Get Transactions for Patron
# -----------------
def get_transactions_for_patron(db: Session, patron_id: int, skip: int = 0, limit: int = 100) -> List[models.Transactions]:
    """
    Get all transactions associated with a specific patron.
    """
    result = db.execute(text("CALL sp_PatronCurrentCheckedOutItems(:patron_id)"), {"patron_id": patron_id})
    data = result.mappings().all()
    db.commit()
    transactions = [models.Transactions(**row) for row in data] # Thank you Gemini!!!
    return transactions

def get_transaction_count_for_patron(db: Session, patron_id: int) -> int:
    """
    Get the count of transactions associated with a specific patron.
    """
    result = db.execute(text("CALL sp_PatronCurrentCheckedOutItemCount(:patron_id)"), {"patron_id": patron_id})
    count = result.scalar_one()
    db.commit()
    return count


def create_transaction(db: Session, transaction: schemas.TransactionCreate) -> models.Transactions:
    db_transaction = models.Transactions(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, transaction_update: schemas.TransactionUpdate) -> Optional[models.Transactions]:
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None

    update_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int) -> Optional[models.Transactions]:
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None

    db.delete(db_transaction)
    db.commit()
    return db_transaction

def process_item_checkin(db: Session, return_request: schemas.ItemReturnRequest) -> schemas.ItemReturnResponse:
    """
    Calls the CheckInItem stored procedure to process an item return.
    """
    
    sql_call = text("""
        CALL CheckInItem(
            :p_patron_id, 
            :p_item_id, 
            :p_return_date
        )
    """)
    
    # --- THIS IS THE FIX ---
    # The keys and values were swapped. This is the correct mapping.
    params = {
        "p_patron_id": return_request.patron_id, 
        "p_item_id": return_request.item_id,
        "p_return_date": return_request.return_date
    }
    # --- END OF FIX ---

    try:
        # 1. Execute the stored procedure
        result_row = db.execute(sql_call, params).first()
        
        # 2. Check if the procedure returned anything at all
        if not result_row:
            db.rollback()
            raise HTTPException(
                status_code=404, 
                detail="Return processing failed: Stored procedure returned no result."
            )
            
        # Convert the row to a dictionary to make it easy to inspect
        result_data = result_row._mapping

        # 3. Check for a business logic error (the 'error' path)
        if result_data.get('Status') == 'error':
            # The procedure ran but found an error (e.g., item not found)
            db.rollback()
            
            raise HTTPException(
                status_code=404, 
                detail=result_data.get('Message', 'An error occurred, but no message was provided.')
            )

        # 4. If Status was not 'error', try to validate the success response
        try:
            successful_response = schemas.ItemReturnResponse.model_validate(result_data)
            
            # 5. SUCCESS: If validation passes, commit the transaction
            db.commit()
            
            # 6. Return the validated Pydantic object
            return successful_response
            
        except ValidationError as e:
            # This is a 500 Server Error. SP success response
            # does not match the Pydantic schema.
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Server Validation Error: SP response mismatch. {e}"
            )

    except SQLAlchemyError as e:
        # A database-level error (connection, syntax, etc.)
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Database error during return: {e}"
        )
    except HTTPException as he:
        # Re-raise the HTTPExceptions we created above
        raise he
    except Exception as e:
        # Catch any other unexpected Python errors
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred: {e}"
        )