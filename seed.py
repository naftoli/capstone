from models import db, User

# Set up the Flask application context
def seed():
    # create a user table if it doesn't exist already
    db.create_all()
    users = [
        User(first_name='Naftoli', last_name='Rapoport', email='naftolir@gmail.com', password='1234'),
        User(first_name='Shterna', last_name='Rapoport', email='shternraps@gmail.com', password='1234')
    ]
    # Add the sample data to the database session
    db.session.add_all(users)
    # Commit the changes to the database
    db.session.commit()
    # Print a message indicating that the data was seeded successfully
    print('Data seeded successfully!')
