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

from student.models import Student, PersonalTimetable
from student.utils import get_student
from student.serializers import get_student_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from timetable.models import Semester
from django.contrib.auth.models import User


class AdvisorView(APIView):
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
            return Response({'reason': 'incorrect request format'}, status=404)
