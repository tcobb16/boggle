from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_valid_guess(self):

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "C", "H"], 
                                 ["C", "A", "T", "C", "H"], 
                                 ["C", "A", "T", "C", "H"], 
                                 ["C", "A", "T", "C", "H"], 
                                 ["C", "A", "T", "C", "H"]]
        response = self.client.get('/check-word?word=catch')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_guess(self):

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')
