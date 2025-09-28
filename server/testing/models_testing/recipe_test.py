import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe

# Ensure tables exist before tests run
with app.app_context():
    db.create_all()

class TestRecipe:
    '''Recipe in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        with app.app_context():
            Recipe.query.delete()
            db.session.commit()
            recipe = Recipe(
                title="Test Recipe",
                instructions="A" * 60,
                minutes_to_complete=30
            )
            db.session.add(recipe)
            db.session.commit()
            created = Recipe.query.first()
            assert created.title == "Test Recipe"
            assert created.instructions == "A" * 60
            assert created.minutes_to_complete == 30

    def test_requires_title(self):
        '''requires each record to have a title.'''
        with app.app_context():
            Recipe.query.delete()
            db.session.commit()
            recipe = Recipe(
                instructions="A" * 60,
                minutes_to_complete=30
            )
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''requires instructions to be at least 50 characters long.'''
        with app.app_context():
            Recipe.query.delete()
            db.session.commit()
            with pytest.raises(ValueError):
                Recipe(
                    title="Short Instructions",
                    instructions="Too short",
                    minutes_to_complete=10
                )

