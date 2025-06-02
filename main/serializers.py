from rest_framework import serializers
from .models import CV, Skill, Project

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'year']

class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = CV
        fields = [
            'id', 'first_name', 'last_name', 'bio', 
            'skills', 'projects', 'contacts',
            'created_at', 'updated_at'
        ]