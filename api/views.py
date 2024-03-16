from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.

class CreateClassView(APIView):

    def get(self, request):
        query_set = StudentClass.objects.all()
        serializer = StudentClassSerializers(query_set, many=True)
        return Response({'success': True, 'data': serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = StudentClassSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': "Student Class Created Successfully."},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.error_messages},
                        status=status.HTTP_400_BAD_REQUEST)


class RegisterStudentView(APIView):

    def get(self, request):
        query_set = User.objects.all()
        serializer = UserSerializers(query_set, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializers(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': "User Created Successfully."},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.error_messages},
                        status=status.HTTP_400_BAD_REQUEST)


class StudentLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializers(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({'success': True, 'refresh': user['refresh'], "access": user['access'],
                             }, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, "error": serializer.errors, "messages": "invalid credential"})


class GetUpdateStudentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = UserSerializers(user)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = StudentUpdateSerializers(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': 'Student Profile Updated Successfully.'},
                            status=status.HTTP_200_OK)
        return Response({'success': False, 'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user.id
        if user:
            return Response({'success': True, 'message': 'Student Profile Deleted Successfully.'},
                            status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Not Found.'},
                        status=status.HTTP_404_NOT_FOUND)


class StudentPermissionView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        user_status = User.objects.filter(id=pk).values('is_inactive')
        return Response({'success': True, 'data': user_status}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializers(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'success': True, 'message': "Student Status Activated."}, status=status.HTTP_200_OK)
