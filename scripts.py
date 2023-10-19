import random

from datacenter.models import Chastisement, Commendation, Lesson, Mark


def fix_marks(schoolkid):
    bad_marks = [2, 3]
    Mark.objects.filter(schoolkid=schoolkid,
                        points__in=bad_marks).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


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
