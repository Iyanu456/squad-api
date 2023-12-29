from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, connect
import uuid

class User(Document):
    """
    MongoDB Document Model for User
    """
    user_id = StringField(required=True, unique=True)
    username = StringField(unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    dob = DateTimeField()  # Date of Birth
    gender = StringField()
    address = StringField()
    is_verified = BooleanField(default=False)
    phone_number = StringField()

    meta = {'collection': 'users'}

    def generate_user_id(self):
        """
        Generate a unique user ID.
        """
        self.user_id = str(uuid.uuid4())

    def save(self, *args, **kwargs):
        # Generate a unique user ID before saving the user
        if not self.user_id:
            self.generate_user_id()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"


class StorageEngine:
    def __init__(self, db_name, host='localhost', port=27017):
        connect(db=db_name, host=host, port=port)

    def save_user(self, username, email, password):
        """
        Save a new user to the MongoDB database.
        """
        new_user = User(username=username, email=email, password=password)
        new_user.save()
        print(f"User {username} saved successfully.")

    def delete_user(self, username):
        """
        Delete a user from the MongoDB database.
        """
        deleted_user = User.objects(username=username).first()
        if deleted_user:
            deleted_user.delete()
            print(f"User {username} deleted successfully.")
        else:
            print(f"User {username} not found.")

    def find_user(self, email):
        """
        Find a user based on their email.
        """
        user = User.objects(email=email).first()
        if user:
            print(f"User found: {user}")
        else:
            print(f"User with email {email} not found.")

    @staticmethod
    def get_user_id(username=None, email=None):
        """
        Get user_id based on username or email.
        """
        if username:
            user = User.objects(username=username).first()
        elif email:
            user = User.objects(email=email).first()
        else:
            return None  # If neither username nor email is provided

        return user.user_id if user else None

if __name__ == "__main__":
    # Assuming User is already defined as shown in the previous examples

    # Create a StorageEngine instance and connect to the database
    storage_engine = StorageEngine(db_name='your_database', host='your_mongo_host', port=your_mongo_port)

    # Save a new user
    storage_engine.save_user(username='john_doe', email='john@example.com', password='hashed_password')

    # Find a user by email
    storage_engine.find_user(email='john@example.com')

    # Delete a user
    storage_engine.delete_user(username='john_doe')
