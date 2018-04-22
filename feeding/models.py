from django.db import models
from datetime import datetime, timedelta


class FeedType(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)
    start_feeding_age = models.IntegerField()
    stop_feeding_age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_average_consumption(self, start_date=None, end_date=datetime.today().date()):
        last_date = end_date
        if start_date:
            first_date = start_date
        else:
            first_date = self.feedentry_set.order_by('date').first()
            first_date = first_date.date

        weight = self.feedentry_set.filter(date__lt=last_date)\
            .filter(date__gte=first_date).aggregate(models.Sum('weight'))
        days = (last_date - first_date).days
        return weight['weight__sum'] / days

    @property
    def days_since_last_deliver(self):
        entry = self.feedentry_set.order_by('date').last()
        if entry is not None:
            entry_date = entry.date
            today = datetime.today().date()
            delta = today - entry_date
            return delta.days

        return None

    @property
    def average_consumption(self):
        return self.get_average_consumption()

class FeedEntry(models.Model):
    date = models.DateField()
    weight = models.FloatField()
    feed_type = models.ForeignKey(to=FeedType, on_delete=models.CASCADE)
