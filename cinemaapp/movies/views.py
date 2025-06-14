from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Movie
from .serializers import MovieSerializer
from accounts.permissions import IsAdmin




class MovieListView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        search = self.request.query_params.get('search')
        if search and len(search) <= 100:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class MovieDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)


class MovieCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response({'message': 'Фильм успешно создан','id': movie.id}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MovieUpdateView(APIView):
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def put(self, request,pk,*args, **kwargs):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Фильм успешно обновлен',})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MovieDeleteView(APIView):
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def delete(self, request,pk,*args, **kwargs):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response({'message': 'Фильм успешно удален',}, status=status.HTTP_204_NO_CONTENT)