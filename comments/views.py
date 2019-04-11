from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from student.models import Student, PersonalTimetable, Comment
from student.utils import get_student, get_student_tts
from rest_framework.views import APIView
from rest_framework.response import Response
#from comments.models import Comment
from helpers.mixins import ValidateSubdomainMixin, RedirectToSignupMixin
from helpers.decorators import validate_subdomain
from comments.serializers import CommentSerializer


class CommentView(APIView):
    def get(self, request, tt_id):
        """ Get all the comments for a timetable """
        try:
            timetable = PersonalTimetable.objects.get(school=request.subdomain, pk=tt_id)
            return Response({'comments': CommentSerializer(list(timetable.comments.all()), many=True).data}, status=200)
        except KeyError:
            return Response({'reason': 'Error finding timetable', 'comments': []}, status=404)

    def post(self, request):
        """ Add comment to a timetable as a user """
        try:
            tt_id = request.data['tt_id']
            comment_str = request.data['comment_str']

            owner = get_student(request)
            # REMEBER YOU WILL NEED TO CHANGE student=owner FOR WHEN ADVISORS CAN COMMENT ON TT's!!
            tt = PersonalTimetable.objects.get(pk=tt_id, school=request.subdomain)
            comment = Comment.create(message=comment_str, owner=owner.user, img_url=owner.img_url)
            comment.save()
            tt.comments.add(comment)
            return Response({'comment_added': CommentSerializer(comment).data}, status=200)

        except KeyError:
            return Response({'reason': 'unknown tbh', 'comment_added': [] }, status=404)

    def delete(self, request, tt_id):
        try:
            timetable = PersonalTimetable.objects.get(school=request.subdomain, pk=tt_id)
            owner = get_student(request)
            # find the comment that matches message, id, and the person sending request
            # (so that someone can't delete someone elses comment on a shared timetable)
            to_del_com = timetable.comments.get(message=request.data['comment_str'], id=request.data['comment_id'], owner=owner.user)
            #ops are id, image_url, last_updated, message, owner, owner_id

            to_del_com.delete()
            return Response({'comment_deleted': request.data['comment_str']}, status=200)
        except Comment.DoesNotExist:
            return Response({'reason': 'Error finding comment to delete, make sure you are the original comment writer',
             'comments': []}, status=404)
        except KeyError:
                    return Response({'reason': 'Error finding comment to delete', 'comments': []}, status=404)

    def put(self, request, tt_id):
        try:
            timetable = PersonalTimetable.objects.get(school=request.subdomain, pk=tt_id)
            owner = get_student(request)

            # find the comment that matches id, and the person sending request
            # (so that someone can't edit someone elses comment on a shared timetable)
            # TODO: send old message so that you can retrieve the old comment
            to_edit_com = timetable.comments.get(message=request.data['old_msg'],
                id=request.data['comment_id'], owner=owner.user)

            # update the message and .save() (should auto update the last updated field??)
            to_edit_com.message = request.data['comment_str']
            to_edit_com.save()

            return Response({'comment_edited': request.data['comment_str']}, status=200)
        except Comment.DoesNotExist:
            return Response({'reason': 'Error finding comment to edit, make sure you are the original comment writer',
             'comments': []}, status=404)
        except KeyError:
            return Response({'reason': 'Error finding comment to edit', 'comments': []}, status=404)