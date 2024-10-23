from random import choice as rc
from app import app
from models import db, Guest, Episode, Appearance
import random

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Guest.query.delete()
        Episode.query.delete()
        Appearance.query.delete()

        print("Seeding guests...")
        guests = [
            Guest(name="Michael J. Fox", occupation="actor"),
            Guest(name="Sandra Bernhard", occupation="Comedian"),
            Guest(name="Tracey Ullman", occupation="television actress"),
            Guest(name="Gillian Anderson", occupation="film actress"),
        ]

        db.session.add_all(guests)

        print("Seeding episodes...")
        episodes = [
            Episode(date="01/11/1999", number="10"),
            Episode(date="01/12/1999", number="3"),
            Episode(date="1/13/99", number="5"),
            Episode(date="1/14/99", number="6"),
            Episode(date="1/18/99", number="11"),
            Episode(date="1/19/99", number="4"),
            Episode(date="1/20/99", number="4"),
            Episode(date="1/21/99", number="5"),
            Episode(date="1/25/99", number="10"),
            Episode(date="1/26/99", number="9"),
        ]

        db.session.add_all(episodes)

        print("Adding guests to episodes...")
        appearances = []
        for guest in guests:
            rating = round(random.uniform(1, 5), 1)
            episode = rc(episodes)
            appearances.append(
                Appearance(guest=guest, episode=episode, rating=rating)
            )
        db.session.add_all(appearances)
        db.session.commit()

        print("Done seeding!")