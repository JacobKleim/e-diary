from django.http import Http404
import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

COMPLIMENTS = ['Молодец!', 'Отличная работа на уроке!']


def get_schoolkid(child_name):
    try:
        return Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.DoesNotExist:
        raise Http404('Ученик не найден')
    except Schoolkid.MultipleObjectsReturned:
        raise Http404('По этому запросу найдено несколько учеников,'
                      'попробуйте персонализировать запрос')


def fix_marks(schoolkid):
    bad_marks = [2, 3]
    Mark.objects.filter(schoolkid=schoolkid,
                        points__in=bad_marks).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject_title):
    text = random.choice(COMPLIMENTS)

    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
        ).order_by('-date')

    lesson = lessons.first()

    if lesson is not None:
        Commendation.objects.create(text=text, created=lesson.date,
                                    schoolkid=schoolkid,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)
