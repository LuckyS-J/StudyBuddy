from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Goal
from .api_serializers import GoalSerializer

@api_view(['GET'])
def getData(request):
  goals = Goal.objects.all()
  serializer = GoalSerializer(goals, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getData(request, id):
  goal = Goal.objects.get(id=id)
  serializer = GoalSerializer(goal)
  return Response(serializer.data)