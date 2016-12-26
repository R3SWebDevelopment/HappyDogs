from django.db import models
from shortuuidfield import ShortUUIDField
from datetime import date
import datetime
INPUT_DATE_FORMAT = '%m/%d/%Y'

def parse_date(input_date=None):
    date_obj = None
    if input_date is not None and input_date.__class__ is str:
        try:
            date_obj = datetime.datetime.strptime(input_date, INPUT_DATE_FORMAT)
        except:
            pass
    return date_obj

class Dog(models.Model):
    uuid = ShortUUIDField(max_length=255, db_index=False)
    first_name = models.TextField(null=False, blank=False)
    last_name = models.TextField(null=False, blank=False, default ="")
    full_name = models.TextField(null=False, blank=False, unique=True)

    class Meta:
        ordering = ['full_name']

    @classmethod
    def add(cls, first_name=None, last_name=None, fetching=False):
        created = False
        instance = None
        if first_name is not None and first_name.__class__ is str and first_name.strip():
            full_name = "{} {}".format(first_name , last_name or "").strip().upper()
            instance, created = cls.objects.got_or_create(full_name = full_name)
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

    def is_the_house(self, date=None):
        visits = self.boarding_visits
        if visits is not None:
            if date is None:
                date = date.today()
            filtered_visits = visits.filter(start_date__lte = date)
            if filtered_visits.exists():
                filtered_visits = filtered_visits.filter(end_date__gt = date)
                return filtered_visits.exists()
        return False

    def add_visit(self, start_date=None, end_date=None):
        visit = None
        created = False
        if start_date is None:
            raise Exception('Start Date is a Required Field')
        elif start_date.__class__ is not Date and start_date.__class__ is str:
            start_date = parse_date(input_date=start_date)
            if start_date is None:
                raise Exception('Start Date Field is Wrong Format')
        elif start_date.__class__ is not Date:
            raise Exception('Start Date Field is Wrong Format')
        if end_date is None:
            raise Exception('End Date is a Required Field')
        elif end_date.__class__ is not Date and end_date.__class__ is str:
            end_date = parse_date(input_date=end_date)
            if end_date is None:
                raise Exception('End Date Field is Wrong Format')
        elif end_date.__class__ is not Date:
            raise Exception('End Date Field is Wrong Format')
        visit, created = BoardingVisit.add(dog=self, start_date=start_date, end_date=end_date)
        return visit, created

    @classmethod
    def add_dog_visit(cls, dog_first_name=None, dog_last_name=None, start_date=None, end_date=None):
        dog, dog_created = cls.add(first_name=dog_first_name, last_name=dog_last_name, fetching=True)
        visit = None
        if dog is not None:
            visit = dog.add_visit(start_date=start_date, end_date=end_date)
        return dog, visit

###TODO
######ADD SAVE METHOD OVERRIDER TO VALID THAT THE FULL NAME IS NOT DUPLICATED

class BoardingVisit(models.Model):
    dog = models.ForeignKey('Dog', blank=False, null=False, related_name='boarding_visits')
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)

    class Meta:
        ordering = ['start_date', 'end_date', 'dog']


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
                    return True
        return False

    @classmethod
    def add(cls, dog=None, start_date=None, end_date=None):
        instance = None
        created = False
        return instance, created

    @classmethod
    def clear(cls):
        cls.object.all().delete()

    @classmethod
    def randomized_boarding(cls):
        cls.clear()
