from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index('email', unique=True)

        # Teams
        teams = [
            {'name': 'Marvel'},
            {'name': 'DC'}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'}
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user': 'spiderman@marvel.com', 'type': 'run', 'distance': 5},
            {'user': 'ironman@marvel.com', 'type': 'cycle', 'distance': 20},
            {'user': 'batman@dc.com', 'type': 'swim', 'distance': 2},
            {'user': 'wonderwoman@dc.com', 'type': 'run', 'distance': 10}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 100},
            {'team': 'DC', 'points': 90}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user': 'spiderman@marvel.com', 'workout': 'pushups', 'reps': 50},
            {'user': 'ironman@marvel.com', 'workout': 'cycling', 'minutes': 60},
            {'user': 'batman@dc.com', 'workout': 'pullups', 'reps': 30},
            {'user': 'wonderwoman@dc.com', 'workout': 'running', 'minutes': 45}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db popolato con dati di test!'))
