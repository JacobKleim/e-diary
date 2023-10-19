import random

from datacenter.models import Chastisement, Commendation, Lesson, Mark


def fix_marks(schoolkid):
    bad_marks = [2, 3]
    child_bad_marks = Mark.objects.filter(schoolkid=schoolkid,
                                          points__in=bad_marks)
    for mark in child_bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)

    for chastisement in child_chastisements:
        chastisement.delete()


def create_commendation(schoolkid, subject_title=None):
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
