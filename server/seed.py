#!/usr/bin/env python3

from app import app
from models import db, Plant

with app.app_context():
    # Clear the table
    Plant.query.delete()

    # Seed data with proper URLs
    aloe = Plant(
        name="Aloe",
        image="https://example.com/aloe.jpg",  # Use an absolute URL for the image
        price=11.50,
    )

    zz_plant = Plant(
        name="ZZ Plant",
        image="https://example.com/zz-plant.jpg",  # Use an absolute URL for the image
        price=25.98,
    )

    # Add seed data to the session and commit to the database
    db.session.add_all([aloe, zz_plant])
    db.session.commit()

    print("Database seeded successfully!")
