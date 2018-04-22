from django.db import models
from django.utils.dateparse import parse_date

from datetime import date, timedelta
from itertools import chain


class RoomGroup(models.Model):
    name = models.CharField(max_length=20)
    group = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    @property
    def number_of_rooms(self):
        count = 0
        for group in self.roomgroup_set.all():
            count += group.number_of_rooms

        count += self.room_set.count()
        return count

    @property
    def animal_capacity(self):
        count = 0
        for group in self.roomgroup_set.all():
            count += group.animal_capacity

        for room in self.room_set.all():
            count += room.capacity

        return count

    @property
    def occupancy(self):
        count = 0
        for group in self.roomgroup_set.all():
            count += group.occupancy

        for room in self.room_set.all():
            count += room.occupancy

        return count

    def __str__(self):
        return self.name


class Building(RoomGroup):
    location = models.CharField(max_length=150, blank=True)


class Silo(models.Model):
    capacity = models.FloatField()
    name = models.CharField(max_length=20)
    building = models.ForeignKey(to=Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(models.Model):
    capacity = models.IntegerField()
    name = models.CharField(max_length=20)
    group = models.ForeignKey(RoomGroup, on_delete=models.CASCADE)
    is_separation = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.occupancy_transitions = {}
        self.transition_start_date = None
        self.transition_end_date = None
        self._entry_list = []
        self._exit_list = []

    @property
    def occupancy(self, at_date=date.today()):
        return self.get_occupancy_at_date(at_date)

    def get_occupancy_at_date(self, at_date=date.today()):
        if isinstance(at_date, str):
            at_date = parse_date(at_date)

        count = 0
        for entry in self.__get_entry_list(start_date=None, end_date=at_date):
            count += entry.number_of_animals

        for room_exit in self.__get_exit_list(start_date=None, end_date=at_date):
            count -= room_exit.number_of_animals
        return count

    def get_occupancy_transitions(self, start_date, end_date):
        if isinstance(start_date, str):
            start_date = parse_date(start_date)
        if isinstance(end_date, str):
            end_date = parse_date(end_date)

        self._compute_occupancy_transitions(start_date, end_date)

        results = {key: self.occupancy_transitions[key] for key in self.occupancy_transitions.keys()
                   if start_date <= key <= end_date}

        first_date = min(results.keys())
        last_date = max(results.keys())

        results.update({start_date: results[first_date]})
        results.update({end_date: results[last_date]})

        return results

    def get_animal_days_for_period(self, start_date, end_date):
        changes = self.get_occupancy_transitions(start_date, end_date)
        dates = sorted(changes.keys())
        previous_count = changes[dates[0]]
        previous_date = dates[0]
        animals_days = 0
        for transition_date in dates[1:]:
            days = (transition_date - previous_date).days
            animals_days += previous_count * days
            previous_date = transition_date
            previous_count = changes[transition_date]

        return animals_days

    def __str__(self):
        return self.group.name + ' - ' + self.name

    def _compute_occupancy_transitions(self, start_date, end_date):
        entries = self.__get_entry_list(start_date, end_date)
        exits = self.__get_exit_list(start_date, end_date)
        changes = chain(entries, exits)
        changes = sorted(changes, key=lambda instance: instance.date)
        occupancy = self.get_occupancy_at_date(start_date)
        results = {start_date: occupancy}
        for change in changes:
            if change.date != start_date:
                occupancy += self.__compute_occupance_change(change)
                results.update({change.date: occupancy})
        results.update({end_date: occupancy})

        self.transition_start_date = start_date
        self.transition_end_date = end_date
        self.occupancy_transitions = results

    def __get_entry_list(self, start_date=None, end_date=None):
        self._entry_list = list(self.animalroomentry_set.all())

        return_list = []
        if start_date is None:
            if end_date is None:
                return_list = self._entry_list
            else:
                return_list = [obj for obj in self._entry_list if obj.date <= end_date]
        else:
            if end_date is None:
                return_list = [obj for obj in self._entry_list if start_date < obj.date]
            else:
                return_list = [obj for obj in self._entry_list if start_date < obj.date <= end_date]

        return return_list

    def __get_exit_list(self, start_date=None, end_date=None):
        self._exit_list = list(self.animalroomexit_set.all())
        return_list = []
        if start_date is None:
            if end_date is None:
                return_list = self._exit_list
            else:
                return_list = [obj for obj in self._exit_list if obj.date <= end_date]
        else:
            if end_date is None:
                return_list = [obj for obj in self._exit_list if start_date < obj.date]
            else:
                return_list = [obj for obj in self._exit_list if start_date < obj.date <= end_date]

        return return_list

    @staticmethod
    def __compute_occupance_change(change_event):
        if isinstance(change_event, AnimalRoomEntry):
            return change_event.number_of_animals
        elif isinstance(change_event, AnimalRoomExit):
            return -change_event.number_of_animals
        else:
            raise ValueError('Invalid change event')


class AnimalRoomEntry(models.Model):
    date = models.DateField()
    number_of_animals = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class AnimalRoomExit(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number_of_animals = models.IntegerField()


class AnimalRoomTransfer(models.Model):
    room_entry = models.ForeignKey(AnimalRoomEntry, on_delete=models.CASCADE)
    room_exit = models.ForeignKey(AnimalRoomExit, on_delete=models.CASCADE)
