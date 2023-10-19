import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)


def get_schoolkid(child_name):
    return Schoolkid.objects.get(full_name__contains=child_name)


def fix_marks(schoolkid):
    bad_marks = [2, 3]
    Mark.objects.filter(schoolkid=schoolkid,
                        points__in=bad_marks).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject_title):
    compliments = ['Молодец!', 'Отличная работа на уроке!']
    text = random.choice(compliments)

    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                    group_letter=schoolkid.group_letter,
                                    subject__title=subject_title)

    lesson = lessons.order_by('-date').first()

    Commendation.objects.create(text=text, created=lesson.date,
                                schoolkid=schoolkid,
                                subject=lesson.subject,
                                teacher=lesson.teacher)
