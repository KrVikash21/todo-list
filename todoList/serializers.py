# todoList/serializers.py
from rest_framework import serializers
from .models import TODO

class TODO_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = TODO
        fields = ['title', 'status','user', 'date']
