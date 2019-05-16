from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from student.models import Student, PersonalTimetable, Comment
from timetable.models import Semester, Course, Section, Offering

from helpers.test.test_cases import UrlTestCase

class UserTimetableViewTest(APITestCase):

    def setUp(self):
        """ Create a user and personal timetable. """
        self.user = User.objects.create_user(
            username='jacob', password='top_secret')
        self.student = Student.objects.create(user=self.user)
        self.sem = Semester.objects.create(name='Winter', year='1995')

        course = Course.objects.create(
            id=1, school='uoft', code='SEM101', name='Intro')
        section = Section.objects.create(
            id=1, course=course, semester=self.sem, meeting_section='L1')
        Offering.objects.create(
            id=1, section=section, day='M', time_start='8:00', time_end='10:00')
        self.tt = PersonalTimetable.objects.create(
            name='tt', school='uoft', semester=self.sem, student=self.student)
        comment = Comment.create(message='test', owner=self.student.user, img_url=self.student.img_url)

        tt.comments.add(comment)
        tt.courses.add(course)
        tt.sections.add(section)
        tt.save()

        self.tt_id = tt.tt_id

        self.factory = APIRequestFactory()

    def test_get_timetables_comments(self):
        request = self.factory.get(
            '/comments/getComments/{0}/'.format(self.tt_id), format='json')
        force_authenticate(request, user=self.user)
        request.user = self.user
        request.subdomain = 'jhu'

        view = resolve('/comments/getComments/{0}/'.format(self.tt_id)).func
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comments']), 1)

    def test_delete_comment(self):
        request = self.factory.delete('/comments/removeComment/{0}/'.format(self.tt_id))
        force_authenticate(request, user=self.user)
        request.user = self.user
        request.subdomain = 'jhu'
        view = resolve('/comments/removeComment/{0}/'.format(self.tt_id)).func
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(PersonalTimetable.comments.filter(message='test').exists())
