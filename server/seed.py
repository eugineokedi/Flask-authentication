from config import db, app
from models import User, Tenant, Payment, Property, Maintenance
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(User).delete()
        db.session.query(Tenant).delete()
        db.session.query(Payment).delete()
        db.session.query(Property).delete()
        db.session.query(Maintenance).delete()

        # Create sample users
        users = [
            User(full_name="John Doe", email="john@example.com", phone_number="1234567890", password="password123"),
            User(full_name="Jane Smith", email="jane@example.com", phone_number="9876543210", password="password456"),
            User(full_name="Eugene Emoyo", email="emoyo@example.com", phone_number="8976354986", password="password874"),
            User(full_name="Michael Brown", email="michael@example.com", phone_number="7654321980", password="password765"),
            User(full_name="Sarah Wilson", email="sarah@example.com", phone_number="6543219876", password="password654"),
            User(full_name="David Green", email="david@example.com", phone_number="5432198765", password="password543"),
            User(full_name="Anna Taylor", email="anna@example.com", phone_number="4321987654", password="password432"),
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create sample tenants
        tenants = [
            Tenant(name="Alice Smith", phone_number="1234567890", id_number="1234567890", house_number="123", user_id=users[0].id),
            Tenant(name="Bob Johnson", phone_number="9876543210", id_number="9876543210", house_number="456", user_id=users[1].id),
            Tenant(name="Charlie Brown", phone_number="7654321980", id_number="7654321980", house_number="789", user_id=users[2].id),
            Tenant(name="David Wilson", phone_number="6543219876", id_number="6543219876", house_number="433", user_id=users[3].id),
            Tenant(name="Emily Taylor", phone_number="5432198765", id_number="5432198765", house_number="789", user_id=users[4].id),
            Tenant(name="Frank Green", phone_number="4321987654", id_number="4321987654", house_number="234", user_id=users[5].id),
            Tenant(name="Grace Wilson", phone_number="3219876543", id_number="3219876543", house_number="567", user_id=users[6].id)
        ]
        db.session.add_all(tenants)
        db.session.commit()

        # Create sample properties
        properties = [
            Property(name="Maskani 1", location="Buruburu", owner="John Doe", image="./assets/maskani1.jpeg", user_id=users[0].id),
            Property(name="Maskani 2", location="Kariri", owner="Jane Smith", image="./assets/maskani2.jpg", user_id=users[1].id),
            Property(name="Maskani 3", location="Gatungu", owner="Eugene Emoyo", image="./assets/maskani3.jpg", user_id=users[2].id),
            Property(name="Maskani 4", location="Kimana", owner="Michael Brown", image="./assets/maskani4.jpg", user_id=users[3].id),
        ]
        db.session.add_all(properties)
        db.session.commit()

        # Create sample maintenances
        maintenances = [
            Maintenance(issue_type="Window Cleaning", description="Cleaned all windows in Maskani 1", contact_information="John Doe", tenant_id=tenants[0].id, date_created=datetime.utcnow()),
            Maintenance(issue_type="Plumbing Fix", description="Fixed broken plumbing in Maskani 2", contact_information="Jane Smith", tenant_id=tenants[1].id, date_created=datetime.utcnow()),
            Maintenance(issue_type="Electrical Repair", description="Repaired damaged electrical system in Maskani 3", contact_information="Eugene Emoyo", tenant_id=tenants[2].id, date_created=datetime.utcnow()),
            Maintenance(issue_type="Fire Safety Check", description="Checked fire safety in Maskani 4", contact_information="Michael Brown", tenant_id=tenants[3].id, date_created=datetime.utcnow()),
            Maintenance(issue_type="Fire Safety Check", description="Checked fire safety in Maskani 5", contact_information="David Green", tenant_id=tenants[4].id, date_created=datetime.utcnow()),
            Maintenance(issue_type="Plumbing Fix", description="Fixed broken plumbing in Maskani 6", contact_information="Sarah Wilson", tenant_id=tenants[5].id, date_created=datetime.utcnow()),
            Maintenance(issue_type="Electrical Repair", description="Repaired damaged electrical system in Maskani 7", contact_information="Anna Taylor", tenant_id=tenants[6].id, date_created=datetime.utcnow())
        ]
        db.session.add_all(maintenances)
        db.session.commit()

        # Create sample payments
        payments = [
            Payment(date_payed=datetime.utcnow(), amount=5000, amount_due=0, user_id=users[0].id, tenant_id=tenants[0].id, property_id=properties[0].id),
            Payment(date_payed=datetime.utcnow(), amount=5000, amount_due=0, user_id=users[1].id, tenant_id=tenants[1].id, property_id=properties[1].id),
            Payment(date_payed=datetime.utcnow(), amount=5000, amount_due=0, user_id=users[2].id, tenant_id=tenants[2].id, property_id=properties[2].id),
            Payment(date_payed=datetime.utcnow(), amount=5000, amount_due=0, user_id=users[3].id, tenant_id=tenants[3].id, property_id=properties[3].id)
        ]
        db.session.add_all(payments)
        db.session.commit()

        try:
            # Commit all changes
            db.session.commit()
            print("Database seeded with new data!")
        except IntegrityError:
            db.session.rollback()
            print("Integrity error occurred. Database rollback.")

if __name__ == "__main__":
    seed_data()
