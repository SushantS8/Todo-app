# # api_views.py
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Task
# from .serializers import TaskSerializer
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def task_list_create(request):
#     if request.method == 'GET':
#         tasks = Task.objects.filter(user=request.user)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def task_detail(request, pk):
#     try:
#         task = Task.objects.get(pk=pk, user=request.user)
#     except Task.DoesNotExist:
#         return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         task.delete()
#         return Response({'message': 'Task Deleted.'}, status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema

class TaskListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: TaskSerializer(many=True)})
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer, responses={201: TaskSerializer})
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer, responses={200: TaskSerializer})
    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial=True)  # partial=True allows update only selected fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({'message': 'Task Deleted'}, status=status.HTTP_204_NO_CONTENT)
