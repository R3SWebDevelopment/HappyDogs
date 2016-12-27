from django.db import models
from shortuuidfield import ShortUUIDField
from datetime import date
import datetime
from utils import parse_date , generate_weekend_list_of_range , generate_holidays_list , generate_day_list_of_range
from random import randint
from datetime import timedelta


LAST_NAME = [
    'SMITH',
    'JOHNSON',
    'WILLIAMS',
    'BROWN',
    'JONES',
    'MILLER',
    'DAVIS',
    'GARCIA',
    'RODRIGUEZ',
    'WILSON',
    'MARTINEZ',
    'ANDERSON',
    'TAYLOR',
    'THOMAS',
    'HERNANDEZ',
    'MOORE',
    'MARTIN',
    'JACKSON',
    'THOMPSON',
    'WHITE',
    'LOPEZ',
    'LEE',
    'GONZALEZ',
    'HARRIS',
    'CLARK',
    'LEWIS',
    'ROBINSON',
    'WALKER',
    'PEREZ',
    'HALL',
    'YOUNG',
    'ALLEN',
    'SANCHEZ',
    'WRIGHT',
    'KING',
    'SCOTT',
    'GREEN',
    'BAKER',
    'ADAMS',
    'NELSON',
    'HILL',
    'RAMIREZ',
    'CAMPBELL',
    'MITCHELL',
    'ROBERTS',
    'CARTER',
    'PHILLIPS',
    'EVANS',
    'TURNER',
    'TORRES',
]

DOG_NAMES = [
    'Gus',
    'Trapper',
    'Finn',
    'Cooper',
    'Bailey',
    'Boomer',
    'Otto',
    'Hawkeye',
    'Wrigley',
    'Ace',
    'Butch',
    'Lucky',
    'Axel',
    'Gunner',
    'Diesel',
    'Delgado',
    'Max',
    'Evan',
    'Buddy',
    'Ricky',
    'Bentley',
    'Czar',
    'Chad',
    'Coco',
    'AJ',
    'Rocky',
    'Jake',
    'Maximus',
    'CJ',
    'Moose',
    'Dodge',
    'Charlie',
    'Cody',
    'Dexter',
    'Bear',
    'Jack',
    'Angus',
    'Spencer',
    'Otis',
    'Brody',
    'Tucker',
    'Blue',
    'Amos',
    'Sam',
    'Blitzen',
    'Biscuit',
    'Fritz',
    'Grommit',
    'Emmet',
    'Shamus',
]

WEEKDEND_DAYS = generate_weekend_list_of_range(start_date = '1/1/2016' , end_date = '12/31/2016')
HOLIDAY_DAYS = generate_holidays_list()
NORMAL_DAYS = generate_day_list_of_range(start_date = '1/1/2016' , end_date = '12/31/2016')



class Dog(models.Model):
    uuid = ShortUUIDField(max_length=255, db_index=False)
    first_name = models.TextField(null=False, blank=False)
    last_name = models.TextField(null=True, blank=True, default ="")
    full_name = models.TextField(null=False, blank=False, unique=True)

    @classmethod
    def clear(cls):
        cls.objects.all().delete()

    @classmethod
    def generate_random_dog(cls):
        number_of_dogs = randint(20, 100)
        for i in range(1,number_of_dogs):
            first_name = DOG_NAMES[randint(0, len(DOG_NAMES)-1 )]
            last_name = LAST_NAME[randint(0, len(LAST_NAME)-1 )]
            try:
                dog,created = cls.add(first_name=first_name, last_name=last_name)
            except:
                pass

    @property
    def generate_random_visit(self):
        visit_number = randint(1, 5)
        for v in range(1, visit_number):
            option = randint(1, 10)
            if option in [1 , 4 , 7 , 9 , 10]:#####WEEKEND
                start_date = WEEKDEND_DAYS[randint(0, len(WEEKDEND_DAYS)-1)]
            elif option in [2 , 5, 8 ]:
                start_date = HOLIDAY_DAYS[randint(0, len(HOLIDAY_DAYS) - 1)]
            elif option in [3 , 6]:
                start_date = NORMAL_DAYS[randint(0, len(NORMAL_DAYS) - 1)]
            else:
                start_date = None
            if start_date is not None:
                days = randint(3, 10)
                delta = timedelta(days=days)
                end_date = start_date + delta
                try:
                    self.add_visit(start_date=start_date, end_date=end_date)
                except Exception,e:
                    pass

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name or "{} {}".format(self.first_name or "", self.last_name or "").strip().upper()

    @property
    def url(self):
        return ""

    def update(self, first_name=None, last_name=None):
        if first_name is not None and first_name.strip():
            self.first_name = first_name
            self.last_name = last_name
            self.save()
            return self
        else:
            raise Exception("First Name is a Required Field")

    @classmethod
    def add(cls, first_name=None, last_name=None, fetching=False):
        created = False
        instance = None
        if first_name is not None and first_name.strip():
            full_name = "{} {}".format(first_name , last_name or "").strip().upper()
            instance, created = cls.objects.get_or_create(full_name = full_name)
            if instance is not None and created:
                instance.first_name = first_name
                instance.last_name = last_name
                instance.save()
            elif instance is not None and not created and not fetching:
                raise Exception('The Dog already Exists on the System')
            elif instance is None and not fetching:
                raise Exception('The Dog has not beed registred.')
        elif not fetching:
            raise Exception('The Dog Should Have at least First Name')
        return instance, created

    @classmethod
    def is_dog_name_registred(cls, first_name=None, last_name=None):
        if first_name is not None and first_name.__class__ is str and first_name.strip():
            full_name = "{} {}".format(first_name , last_name or "").strip().upper()
            return cls.objects.filter(full_name__iexact = full_name).exists()
        return False

    def is_the_house(self, date_obj=None):
        visits = self.boarding_visits
        if visits is not None:
            if date_obj is None:
                date_obj = date.today()
            filtered_visits = visits.filter(start_date__lte = date_obj)
            if filtered_visits.exists():
                filtered_visits = filtered_visits.filter(end_date__gt = date_obj)
                return filtered_visits.exists()
        return False

    def is_the_house_label(self, date_obj=None):
        if self.is_the_house(date_obj=date_obj):
            return 'Yes'
        return 'No'

    @property
    def visits_detail(self):
        visits_detail = []
        visits = self.boarding_visits.all()
        for visit in visits:
            visits_detail.append({
                'start_date' : visit.start_date.strftime('%m/%d/%Y'),
                'end_date' : visit.end_date.strftime('%m/%d/%Y'),
            })
        return visits_detail

    @property
    def visits(self):
        return self.boarding_visits.count()

    def add_visit(self, start_date=None, end_date=None):
        visit = None
        created = False
        if start_date is None:
            raise Exception('Start Date is a Required Field')
        elif start_date.__class__ is not date and start_date.__class__ is str:
            start_date = parse_date(input_date=start_date)
            if start_date is None:
                raise Exception('Start Date Field is Wrong Format')
        elif start_date.__class__ is not date:
            raise Exception('Start Date Field is Wrong Format')
        if end_date is None:
            raise Exception('End Date is a Required Field')
        elif end_date.__class__ is not date and end_date.__class__ is str:
            end_date = parse_date(input_date=end_date)
            if end_date is None:
                raise Exception('End Date Field is Wrong Format')
        elif end_date.__class__ is not date:
            raise Exception('End Date Field is Wrong Format')
        visit, created = BoardingVisit.add(dog=self, start_date=start_date, end_date=end_date)
        return visit, created

    @classmethod
    def add_dog_visit(cls, dog_first_name=None, dog_last_name=None, start_date=None, end_date=None):
        dog, dog_created = cls.add(first_name=dog_first_name, last_name=dog_last_name, fetching=True)
        visit = None
        if dog is not None:
            visit, crated = dog.add_visit(start_date=start_date, end_date=end_date)
        return dog, visit

    def save(self, *args, **kwargs):
        full_name = "{} {}".format(self.first_name, self.last_name or "").strip().upper()
        if self.__class__.objects.all().exclude(uuid = self.uuid).filter(full_name__iexact = full_name).exists():
            raise Exception('There is another dog with the same name')
        self.full_name = full_name
        super(Dog, self).save(*args, **kwargs)

class BoardingVisit(models.Model):
    uuid = ShortUUIDField(max_length=255, db_index=False)
    dog = models.ForeignKey('Dog', blank=False, null=False, related_name='boarding_visits')
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)

    class Meta:
        ordering = ['start_date', 'end_date', 'dog']

    def __str__(self):
        return "Dog: {} : Start Date: {} to End Date: {}".format(self.dog, self.start_date, self.end_date)

    @classmethod
    def visits(cls, start_date=None, end_date=None):
        visits = cls.objects.all()
        if visits.exists():
            if start_date is not None:
                if start_date.__class__ is str:
                    start_date = parse_date(input_date=start_date)
                if start_date is not None and start_date.__class__ is date:
                    visits = visits.filter(start_date__gte = start_date)
        if visits.exists():
            if end_date is not None:
                if end_date.__class__ is str:
                    end_date = parse_date(input_date=end_date)
                if end_date is not None and end_date.__class__ is date:
                    visits = visits.filter(end_date__lte=end_date)
        return visits

    @classmethod
    def dog_has_visit(cls, dog=None):
        if dog is not None and dog.__class__ is Dog:
            return cls.objects.filter(dog=dog).exists()
        return False

    @classmethod
    def dog_visits(cls, dog=None):
        data = cls.objects.none()
        if dog is not None and dog.__class__ is Dog:
            data = cls.objects.filter(dog=dog)
        return data

    @classmethod
    def dog_has_overlaping_dates(cls, dog=None, start_date=None, end_date=None):
        if dog is not None and dog.__class__ is Dog and start_date is not None and start_date.__class__ is date and end_date is not None and end_date.__class__ is date:
            if cls.dog_has_visit(dog=dog) and start_date < end_date:
                visits = cls.dog_visits(dog=dog)
                if visits is not None:
                    #######HERE COMES THE DATE RANGE FILTERING
                    #####FIRST LOOK UP FOR ANY VISIT WITHIN THE REQUESTING RANGE
                    if visits.filter(start_date__range=(start_date, end_date)).exists() and visits.filter(end_date__range=(start_date, end_date)).exists():
                        return True
                    #####SECOND LOOK UP FOR ANY VISIT WITHIN THE REQUESTING RANGE
                    if visits.filter(start_date__lte = start_date , end_date__gte = end_date).exists():
                        return True
        return False

    @classmethod
    def add(cls, dog=None, start_date=None, end_date=None):
        instance = None
        created = False
        if start_date is not None and end_date is not None:
            if start_date >= end_date:
                raise Exception('The Start Date have to be before the End Date')
        if not cls.dog_has_overlaping_dates(dog=dog, start_date=start_date, end_date=end_date):
            instance, created = cls.objects.get_or_create(dog=dog, start_date=start_date, end_date=end_date)
            if instance is not None and not created:
                raise Exception('This Dog has a overlaping Visit')
        else:
            raise Exception('This Dog has a overlaping Visit')
        return instance, created

    @classmethod
    def clear(cls):
        cls.objects.all().delete()

    @classmethod
    def randomized_boarding(cls):
        cls.clear()

    @classmethod
    def dogs_in_house(cls, date_obj=None):
        dogs_in_house = 0
        if date_obj is not None and date_obj.__class__ is date:
            filter = cls.objects.filter(start_date__lte=date_obj , end_date__gte=date_obj)
            if filter.exists():
                dogs_in_house = filter.count()
        return dogs_in_house

    @classmethod
    def date_visits(cls, date_obj=None):
        data = cls.objects.none()
        if date_obj is not None:
            data = cls.objects.filter(start_date__lte=date_obj, end_date__gte=date_obj)
        return data

    @property
    def dog_name(self):
        return self.dog.full_name or ""

    @property
    def dog_url(self):
        return self.dog.url