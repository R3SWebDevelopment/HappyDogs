from django.test import TestCase
from django.test import Client
from models import BoardingVisit, Dog
from utils import parse_date

class DogTestCase(TestCase):
    def setUp(self):
        super(DogTestCase, self).setUp()
        self.dog_1, created = Dog.add(first_name = 'Skipper', last_name='Tercero')
        self.dog_2, created = Dog.add(first_name='Botas', last_name='Tercero')
        self.dog_3, created = Dog.add(first_name='Max', last_name='Tercero')
        self.dog_4, created = Dog.add(first_name='Ronny', last_name='Tercero')
        self.dog_5, created = Dog.add(first_name='Guty', last_name='Diaz')
        self.dog_6, created = Dog.add(first_name='Papo', last_name='Diaz')
        self.dog_7, created = Dog.add(first_name='Helca', last_name='Diaz')
        self.dog_8, created = Dog.add(first_name='Dobby')
        self.dog_1.add_visit(start_date='1/1/2016' , end_date='1/31/2016')
        self.dog_1.add_visit(start_date='2/1/2016', end_date='2/18/2016')
        self.dog_1.add_visit(start_date='3/1/2016', end_date='3/31/2016')

    def test_visit_count(self):
        self.assertEquals(self.dog_8.visits, 0)
        self.assertEquals(self.dog_1.visits, 3)


    def test_dog_int_the_house(self):
        date_obj_1 = parse_date(input_date='2/1/2016')
        date_obj_2 = parse_date(input_date='12/31/2016')
        self.assertEquals(self.dog_1.is_the_house(date_obj_1), True)
        self.assertEquals(self.dog_1.is_the_house(date_obj_2), False)

    def test_dog_has_overlaping_date(self):
        date_obj_1 = parse_date(input_date='1/1/2016')
        date_obj_2 = parse_date(input_date='1/15/2016')
        dog_has_overlaping_dates_1 = BoardingVisit.dog_has_overlaping_dates(dog=self.dog_1, start_date=date_obj_1, end_date=date_obj_2)
        self.assertEquals(dog_has_overlaping_dates_1, False)

    def test_dog_has_visits(self):
        dog_has_visit_1 = BoardingVisit.dog_has_visit(dog = self.dog_1)
        self.assertEquals(dog_has_visit_1, True)

        dog_has_visit_8 = BoardingVisit.dog_has_visit(dog=self.dog_8)
        self.assertEquals(dog_has_visit_8, False)

    def test_name_duplicated(self):
        test_1 = Dog.is_dog_name_registred(first_name = 'dobby')
        test_2 = Dog.is_dog_name_registred(first_name='Ricky')
        test_3 = Dog.is_dog_name_registred(first_name='guty' , last_name = "DIAZ")
        test_4 = Dog.is_dog_name_registred(first_name='SKIPPER TER', last_name="CERO")

        self.assertTrue(test_1)
        self.assertFalse(test_2)
        self.assertTrue(test_3)
        self.assertFalse(test_4)

    def test_adding_dogs(self):
        dog_9_error = False
        dog_9_error_message = None
        try:
            self.dog_9, created = Dog.add(first_name='SKIPPER' , last_name='TERCERO')
            dog_9_error = False
        except Exception,e:
            dog_9_error = True
            dog_9_error_message = "{}".format(e)

            self.assertTrue(dog_9_error)
            self.assertEquals(dog_9_error_message , "The Dog already Exists on the System")


        dog_10_error = False
        dog_10_error_message = None
        try:
            self.dog_10, created = Dog.add(last_name='TERCERO')
            dog_10_error = False
        except Exception, e:
            dog_10_error = True
            dog_10_error_message = "{}".format(e)


        self.assertTrue(dog_10_error)
        self.assertEquals(dog_10_error_message, "The Dog Should Have at least First Name")


        dog_11_error = False
        dog_11_error_message = None
        try:
            self.dog_11, created_11 = Dog.add(first_name='Solovino')
            dog_11_error = False
        except Exception, e:
            dog_11_error = True
            dog_11_error_message = "{}".format(e)

        self.assertFalse(dog_11_error)
        self.assertTrue(created_11)
        self.assertEquals(dog_11_error_message, None)

    def test_update_name(self):
        dog_1_error = False
        dog_1_error_message = None
        try:
            self.dog_1 = self.dog_1.update(first_name='Botas' , last_name = 'Tercero')
            dog_1_error = False
        except Exception,e:
            dog_1_error_message = "{}".format(e)
            dog_1_error = True

        self.assertTrue(dog_1_error)
        self.assertEquals(dog_1_error_message, "There is another dog with the same name")
        self.assertEquals(self.dog_1.full_name, "SKIPPER TERCERO")


        dog_5_error = False
        dog_5_error_message = None
        try:
            self.dog_5 = self.dog_5.update(first_name='Gutish', last_name='Diaz')
            dog_5_error = False
        except Exception, e:
            dog_5_error_message = "{}".format(e)
            dog_5_error = True

        self.assertFalse(dog_5_error)
        self.assertEquals(dog_5_error_message, None)
        self.assertEquals(self.dog_5.full_name, "GUTISH DIAZ")
