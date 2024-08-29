import unittest
from datetime import datetime, timedelta
from app import create_app
from app.decks.models import Deck, Card
from app.review.routes import schedule_review


class TestScheduleReview(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create and configure the app
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        # Set up a test deck with a known start date
        self.deck = Deck(review_start_date=datetime(year=2024, month=8, day=1))
        self.card = Card(box=1, next_review_date=datetime.utcnow())

    def test_correct_review_box_1_to_2_on_day_1(self):
        # Assume the deck is on day 1 of the cycle
        self.deck.get_day_of_cycle = lambda: 1  # Mock the method to return day 1

        # Scenario: Card is in box 1 and reviewed correctly
        # Expected behavior: The card should move to box 2 and be scheduled for review on day 3
        schedule_review(self.card, success=True, deck=self.deck)
        self.assertEqual(self.card.box, 2)
        expected_date = datetime.utcnow().date() + timedelta(days=2)
        self.assertEqual(self.card.next_review_date.date(), expected_date)

    def test_incorrect_review_box_3_to_1_on_day_7(self):
        # Assume the deck is on day 7 of the cycle
        self.deck.get_day_of_cycle = lambda: 7  # Mock the method to return day 7

        # Scenario: Card is in box 3 and reviewed incorrectly
        # Expected behavior: The card should be reset to box 1 and be scheduled for review on day 8
        schedule_review(self.card, success=False, deck=self.deck)
        self.assertEqual(self.card.box, 1)
        expected_date = datetime.utcnow().date() + timedelta(days=1)
        self.assertEqual(self.card.next_review_date.date(), expected_date)

    def test_correct_review_box_4_to_5_on_day_4(self):
        # Assume the deck under review is on day 4 of the cycle
        self.deck.get_day_of_cycle = lambda: 4  # Mock the method to return day 4
        # Scenario: Card is initially in box 4 and reviewed correctly
        # Expected behavior: The card should move to box 5 and be scheduled for review on day 10
        self.card.box = 4
        schedule_review(self.card, success=True, deck=self.deck)
        self.assertEqual(self.card.box, 5)
        expected_date = datetime.utcnow().date() + timedelta(days=6)
        self.assertEqual(self.card.next_review_date.date(), expected_date)


if __name__ == '__main__':
    unittest.main()
