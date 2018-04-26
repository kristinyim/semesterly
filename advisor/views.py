# Copyright (C) 2017 Semester.ly Technologies, LLC
#
# Semester.ly is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Semester.ly is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from django.http import HttpResponse
from student.models import Student, PersonalTimetable
from student.utils import get_student, get_student_tts
from student.serializers import get_student_dict, StudentSerializer
from timetable.serializers import DisplayTimetableSerializer
from courses.serializers import CourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from timetable.models import Semester
from django.contrib.auth.models import User


class AddAdvisorView(APIView):
    def post(self, request):
        """ Add an advisor by email """
        try:
            tt_id = request.data['tt_id']
            sem_name = request.data['sem_name']
            sem_year = request.data['sem_year']
            advisor_email = request.data['advisor_email']

            student = get_student(request)
            semester = Semester.objects.get(name=sem_name, year=sem_year)
            school = request.subdomain

            if student:
                if student.user.email == advisor_email:
                    return Response({'reason': 'Cannot add yourself', 'advisors_added': []}, status=404)

            output = []
            advisors_list = list(User.objects.filter(email=advisor_email))
            for advisor in advisors_list:
                timetable = PersonalTimetable.objects.get(student=student, pk=tt_id, school=school, semester=semester)
                if timetable:
                    advisor_obj = Student.objects.get(user=advisor)
                    if advisor_obj in timetable.advisors.all():
                        return Response({'reason': 'Advisor already exists', 'advisors_added:': []}, status=404)
                    timetable.advisors.add(advisor_obj)
                    output.append(get_student_dict(school, advisor_obj, semester))
            return Response({'advisors_added': output}, status=200)
        except KeyError:
            return Response({'reason': 'Incorrect request format', 'advisors_added': []}, status=404)


class RetrieveAdvisorView(APIView):
    def get(self, request, sem_name, year, tt_id):
        """Return list of advisors who can view the current timetable. """
        try:
            student = get_student(request)
            semester = Semester.objects.get(name=sem_name, year=year)
            school = request.subdomain

            advisors = []

            timetable = PersonalTimetable.objects.get(student=student, pk=tt_id, school=school, semester=semester)
            for advisor in timetable.advisors.all():
                advisors.append(Student.objects.get(user=advisor.user))
            return Response({'advisors_existing': StudentSerializer(advisors, many=True).data }, status=200)
        except KeyError:
            # CHANGE TO IDK BUT NOT THIS
            return Response({'reason': 'Incorrect request format', 'advisors_existing': []}, status=404)

class AdvisorView(APIView):
    def get(self, request, sem_name, year):
        """ Get list of timetables viewable by the authenticated user """
        student = get_student(request)
        timetables = PersonalTimetable.objects.all()
        sem, _ = Semester.objects.get_or_create(name=sem_name, year=year)
        tt_can_view = []
        courses = set()
        for tt in timetables:
            if student in tt.advisors.all():
                # if the user can view this timetable (i.e. is an advisor)
                # add owner data for display
                with_user = DisplayTimetableSerializer.from_model(tt).data
                user = tt.student.user
                with_user['user'] = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
                with_user['last_updated'] = {'last_updated': tt.last_updated}
                for c in tt.courses.all():
                    courses.add(c)
                tt_can_view.append(with_user)
        context = {'semester': sem, 'school': request.subdomain, 'student': student}
        return Response({
            'timetables': tt_can_view,
            'courses': CourseSerializer(courses, context=context, many=True).data
        }, status=200)

    def delete(self, request, sem_name, year, tt_name, student_email):
            """ Deletes an advisor from a PersonalTimetable by name/year/term and advisor email."""
            advisor = get_student(request)  # current authorized user
            student_user_list = list(User.objects.filter(email=student_email))

            if len(student_user_list) == 0:
                return Response({'reason': 'invalid student email'}, status=404)

            student_list = [Student.objects.get(user=u) for u in student_user_list]

            school = request.subdomain
            semester = Semester.objects.get(name=sem_name, year=year)

            removed = []
            # account for multiple student emails for same account
            for student in student_list:
                timetables = PersonalTimetable.objects.filter(
                    student=student, name=tt_name, school=school, semester=semester)

                for tt in timetables:
                    if advisor in tt.advisors.all():
                        tt.advisors.remove(advisor)
                        removed.append(tt)

            return Response({'timetables': DisplayTimetableSerializer.from_model(removed, many=True).data},
                            status=200)
