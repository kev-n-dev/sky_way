from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

# Handler to get a user by ID
def get_user_by_id(user_id):
    """
    Get a user by their ID.
    """
    try:
        user = User.query.filter_by(id=user_id, deleted_at=None).first()  # Exclude soft-deleted users
        if user is None:
            return None  # Or raise an error if you prefer
        return user
    except NoResultFound:
        return None

# Handler to get a user by email
def get_user_by_email(email):
    """
    Get a user by their email address.
    """
    try:
        user = User.query.filter_by(email=email, deleted_at=None).first()  # Exclude soft-deleted users
        if user is None:
            return None  # Or raise an error if you prefer
        return user
    except NoResultFound:
        return None

# Handler to create a new user
def create_user(first_name, last_name, gender, email, password):
    """
    Create a new user in the system.
    """
    try:
        # Check if email is already in use
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return None  # Or raise an error for existing email
        # Create a new user instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email
        )
        # Set the user's password
        new_user.set_password(password)
        
        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        return None

# Handler to delete a user (soft delete)
def delete_user(user_id):
    """
    Soft delete a user by setting the 'deleted_at' field to the current time.
    """
    try:
        user = User.query.filter_by(id=user_id, deleted_at=None).first()
        if user is None:
            return None  # Or raise an error if you prefer
        user.deleted_at = datetime.utcnow()  # Mark user as deleted
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        return None

# Handler to update a user
def update_user(user_id, first_name=None, last_name=None, gender=None, email=None, password=None):
    """
    Update a user's information.
    """
    try:
        user = User.query.filter_by(id=user_id, deleted_at=None).first()  # Exclude soft-deleted users
        if user is None:
            return None  # Or raise an error if you prefer

        # Update fields if provided
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if gender:
            user.gender = gender
        if email:
            user.email = email
        if password:
            user.set_password(password)  # Update the user's password

        # Commit the changes
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        return None
