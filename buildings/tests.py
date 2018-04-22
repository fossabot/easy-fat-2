from django.test import TestCase
from datetime import date
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Room, RoomGroup, Building


class RoomTestCase(TestCase):

    def setUp(self):
        self.building = Building(name='TheBigBuilding')
        self.building.save()
        self.room = Room(name='Room1', capacity=10, group=self.building)
        self.room.save()

    def test_get_name(self):
        self.assertEqual('Room1', self.room.name)

    def test_occupancy_after_entry(self):
        self.room.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')
        self.assertEqual(10, self.room.get_occupancy_at_date('2017-01-02'))

    def test_occupancy_after_exit(self):
        self.room.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-03')
        self.assertEqual(10, self.room.get_occupancy_at_date('2017-01-02'))
        self.assertEqual(9, self.room.get_occupancy_at_date('2017-01-04'))

    def test_occupancy_after_multiple_exits(self):
        self.room.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-03')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-05')
        self.assertEqual(10, self.room.get_occupancy_at_date('2017-01-02'))
        self.assertEqual(9, self.room.get_occupancy_at_date('2017-01-04'))
        self.assertEqual(8, self.room.get_occupancy_at_date('2017-01-05'))

    def test_occupancy_changes_1(self):
        expected_output = {date(2017, 1, 1): 10,
                           date(2017, 1, 3): 9,
                           date(2017, 1, 5): 8,
                           date(2017, 1, 6): 8}
        self.room.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-03')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-05')
        changes = self.room.get_occupancy_transitions(date(2017, 1, 1), '2017-01-06')
        self.assertEqual(4, len(changes))
        self.assertEqual(expected_output, changes)

    def test_occupancy_changes_2(self):
        expected_output = {date(2016, 12, 1): 0,
                           date(2017, 1, 1): 10,
                           date(2017, 1, 3): 9,
                           date(2017, 1, 5): 8,
                           date(2017, 1, 6): 8}
        self.room.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-03')
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-05')
        changes = self.room.get_occupancy_transitions(date(2016, 12, 1), '2017-01-06')
        self.assertEqual(5, len(changes))
        self.assertEqual(expected_output, changes)

    def test_animal_days_count(self):
        self.room.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')
        animal_days = self.room.get_animal_days_for_period(date(2016, 12, 1), date(2017, 1, 3))
        self.assertEqual(20, animal_days)
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-03')
        animal_days = self.room.get_animal_days_for_period(date(2017, 1, 3), date(2017, 1, 5))
        self.assertEqual(18, animal_days)
        self.room.animalroomexit_set.create(number_of_animals=1, date='2017-01-05')
        animal_days = self.room.get_animal_days_for_period(date(2017, 1, 5), date(2017, 1, 7))
        self.assertEqual(16, animal_days)
        animal_days = self.room.get_animal_days_for_period(date(2016, 12, 1), date(2017, 1, 7))
        self.assertEqual(54, animal_days)


class BuildingLayoutInformation(TestCase):

    def setUp(self):
        self.building = Building(name='TheBigBuilding')
        self.building.save()
        self.room_group = RoomGroup(group=self.building, name='Group1')
        self.room_group.save()
        self.room1 = Room(group=self.building, name='Room 1', capacity=10)
        self.room1.save()
        self.room2 = Room(group=self.building, name='Room 2', capacity=10)
        self.room2.save()
        self.room3 = Room(group=self.room_group, name='Room 3', capacity=10)
        self.room3.save()
        self.silo1 = self.building.silo_set.create(capacity=10000)
        self.silo1.save()
        self.silo2 = self.building.silo_set.create(capacity=20000)
        self.room1.animalroomentry_set.create(number_of_animals=10, date='2017-01-01')

    def test_room_count(self):
        self.assertEqual(3, self.building.number_of_rooms)

    def test_capacity(self):
        self.assertEqual(30, self.building.animal_capacity)

    def test_name(self):
        self.assertEqual('TheBigBuilding', self.building.name)

    def test_occupancy(self):
        self.assertEqual(10, self.building.occupancy)
