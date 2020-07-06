from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from django.contrib.auth.models import User

from main.models import Image, BasicUser, Project, AnnotationsJson
from main.permissions import IsOwnerOrReadOnly
from main.serializers import ImageSerializer, UserSerializer, BasicUserSerializer, ProjectSerializer, AnnotationsJsonSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BasicUserList(generics.ListAPIView):
    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer


class BasicUserDetail(generics.RetrieveAPIView):
    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_email=request.META["HTTP_X_EMAIL"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]



class AnnotationsJsonList(generics.ListAPIView):
    queryset = AnnotationsJson.objects.all()
    serializer_class = AnnotationsJsonSerializer

    def post(self, request, format=None):
        serializer = AnnotationsJsonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(image_id=request.data["image_id"], owner_email=request.META["HTTP_X_EMAIL"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnnotationsJsonDetail(generics.RetrieveAPIView):
    queryset = AnnotationsJson.objects.all()
    serializer_class = AnnotationsJsonSerializer


class ImageList(APIView):
    """
    List all images, or create a new image.
    """
    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=request.data["project_id"], owner_email=request.META["HTTP_X_EMAIL"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    """
    Retrieve, update or delete a image instance.
    """
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)