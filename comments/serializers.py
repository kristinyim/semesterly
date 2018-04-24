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

import itertools
from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    message = serializers.CharField()
    ownerFirstName = serializers.CharField(source='owner.first_name')
    ownerLastName = serializers.CharField(source='owner.last_name')
    image_url = serializers.CharField()
    last_updated = serializers.DateTimeField()
    class Meta:
            model = Comment
            fields = (
                'message',
                'ownerFirstName',
                'ownerLastName',
                'last_updated',
                'image_url',
            )
