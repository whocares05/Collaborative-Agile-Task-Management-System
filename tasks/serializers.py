from rest_framework import serializers
from django.contrib.auth.models import User
from .models import workspace, Task, Label
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username','email','first_name','last_name']

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Label
        fields=['id','name','color_code','workspace']

class WorkspaceSerializer(serializers.ModelSerializer):
    owner_details=UserSerializer(read_only=True, source='owner')
    class Meta:
        model = workspace
        fields=['id','name','description','owner','owner_details','created_at']git
        read_only_fields=['owner_details']

class TaskSerializer(serializers.ModelSerializer):
    assignee_details=UserSerializer(read_only=True, source='assignee')
    collaborators_details=UserSerializer(read_only=True, many=True, source='collaborators')
    labels_details=LabelSerializer(read_only=True, many=True, source='Labels')

    collaborators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )
    labels = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Label.objects.all(), required=False
    )

    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 
            'workspace', 'assignee', 'assignee_details', 
            'collaborators', 'collaborator_details', 
            'labels', 'label_details', 'due_date', 'days_remaining',
            'created_at', 'updated_at'
        ]

    def get_days_remaining(self, obj):
        if obj.due_date:
            delta = obj.due_date - timezone.now()
            return max(0, delta.days) 
        return None

    def validate(self, attrs):
        due_date = attrs.get('due_date')
        if due_date and due_date < timezone.now():
            raise serializers.ValidationError({
                "due_date": "The task due date must be set in the future."
            })
        return attrs