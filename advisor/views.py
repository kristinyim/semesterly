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
from student.utils import get_student
from student.serializers import get_student_dict
from timetable.serializers import DisplayTimetableSerializer
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
                    return Response({'reason': 'cannot add yourself', 'advisors_added': []}, status=404)

            output = []
            advisors_list = list(User.objects.filter(email=advisor_email))
            for advisor in advisors_list:
                timetable = PersonalTimetable.objects.get(student=student, pk=tt_id, school=school, semester=semester)
                if timetable:
                    advisor_obj = Student.objects.get(user=advisor)
                    timetable.advisors.add(advisor_obj)
                    output.append(get_student_dict(school, advisor_obj, semester))
            return Response({'advisors_added': output}, status=200)
        except KeyError:
            return Response({'reason': 'incorrect request format', 'advisors_added': []}, status=404)


class AdvisorView(APIView):
    def get(self, request):
        """ Get list of timetables viewable by the authenticated user """
        current_auth_student = get_student(request)
        timetables = PersonalTimetable.objects.filter(student=current_auth_student) if current_auth_student else []

        tt_can_view = []
        for tt in timetables:
            if current_auth_student in tt.advisors.all():
                # if the user can view this timetable (i.e. is an advisor)
                tt_can_view.append(tt)

        return Response({'timetables': DisplayTimetableSerializer.from_model(tt_can_view, many=True).data}, status=200)
