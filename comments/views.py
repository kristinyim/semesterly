from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from student.models import Student, PersonalTimetable
from student.utils import get_student, get_student_tts
from student.serializers import get_student_dict, StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from timetable.models import Semester
from django.contrib.auth.models import User
from comments.models import Comment
from helpers.mixins import ValidateSubdomainMixin, RedirectToSignupMixin
from helpers.decorators import validate_subdomain
from comments.serializers import CommentSerializer

class CommentView(APIView):
    def get(self, request, sem_name, sem_year, tt_id, student_email):
        try:
            sem, _ = Semester.objects.get_or_create(name=sem_name, year=sem_year)

            student = get_student(request)
            timetable = PersonalTimetable.objects.get(student=student,
                     school=request.subdomain, semester=sem, pk=tt_id)

            tt_comments = timetable.comments.all()
            comments = []
            for comment in tt_comments:
                comments.append(comment)
            return Response({'comments': CommentSerializer(comments, many=True).data}, status=200)
        except KeyError:
            return Response({'reason': 'unknown tbh', 'comments': []}, status=404)

    def post(self, request):
        try:
            tt_id = request.data['tt_id']
            sem_name = request.data['sem_name']
            sem_year = request.data['sem_year']
            comment_str = request.data['comment_str']
            sem, _ = Semester.objects.get_or_create(name=sem_name, year=sem_year)

            owner = get_student(request)
            # REMEBER YOU WILL NEED TO CHANGE student=owner FOR WHEN ADVISORS CAN COMMENT ON TT's!!
            tt = PersonalTimetable.objects.get(student=owner, pk=tt_id, school=request.subdomain, semester=sem)
            comment = Comment.create(message=comment_str, owner=owner.user)
            comment.save()
            tt.comments.add(comment)
            return Response({'comment_added': CommentSerializer(comment).data}, status=200)

        except KeyError:
            return Response({'reason': 'unknown tbh', 'comment_added': [] }, status=404)

"""
    def put(self, request):

    def delete(self, request):"""