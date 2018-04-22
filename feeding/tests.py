from django.test import TestCase
from datetime import date, timedelta, datetime
from .models import FeedType, FeedEntry


# Create your tests here.
class FeedingTests(TestCase):

    def setUp(self):
        super().setUpClass()
        self.feed_type = FeedType(name='S2', start_feeding_age=0, stop_feeding_age=1)
        self.feed_type.save()

    def test_str_function(self):
        self.assertEqual('S2', self.feed_type.__str__())

    def test_days_since_delivery_no_delivery(self):
        self.assertIsNone(self.feed_type.days_since_last_deliver)

    def test_days_since_delivery(self):
        entry_date = datetime.today() - timedelta(days=7)
        self.feed_type.feedentry_set.create(date=entry_date.date(), weight=10000)
        self.assertEqual(7, self.feed_type.days_since_last_deliver)

    def test_average_consumption(self):
        for i in range(1, 11):
            entry_date = datetime.today() - timedelta(days=7*i)
            self.feed_type.feedentry_set.create(date=entry_date.date(), weight=10000)

        self.assertEqual(10000/7, self.feed_type.average_consumption)

    def test_average_consumption_intermediate(self):
        for i in range(1, 11):
            entry_date = datetime.today() - timedelta(days=7*i)
            start_date = entry_date
            end_date = datetime.today() - timedelta(days=7*(i-1))
            self.feed_type.feedentry_set.create(date=entry_date.date(), weight=10000)
            self.assertEqual(10000/7, self.feed_type.get_average_consumption(start_date, end_date))