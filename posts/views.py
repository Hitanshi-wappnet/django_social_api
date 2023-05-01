from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from django.db.models import Q
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from posts.pagination import CustomPagination
import threading
from services.send_mail import send_mail


class PostView(APIView):

    # Adding the MultiPartParser to the parser_classes attribute
    # of the view to enable parsing of multipart data.
    parser_classes = (MultiPartParser,)

    # Only Authenticated User can add Post
    permission_classes = [IsAuthenticated]

    # Method of Posting of text, images, and videos
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        '''
        If serializer is valid then save the data and
        returns success response else return error response
        '''
        if serializer.is_valid():
            self.perform_create(serializer)
            serializer.save(user=request.user)
            # Post.save()
            response = {"status": True,
                        "message": "Your Post added successfully"}
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response = {"status": False,
                        "message": serializer.errors,
                        "data": None}
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostSearchView(APIView):

    # Only Authenticated User can search Post
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.data.get('search')
        if query:
            # Define a search query using Django's Q objects
            q = Q(content__icontains=query) | Q(user__username__icontains=query)
            # Retrieve the matching posts using the search query
            posts = Post.objects.filter(q)
        else:
            # If no query is provided, return all posts
            posts = Post.objects.all()
        if posts:
            # Add pagination to tasks queryset
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(paginated_queryset, many=True)

            # Serialize the matching posts and return them as a JSON response
            response = {
                "status": True,
                "message": "The data of Post based on your serach",
                "data": serializer.data
            }
            return paginator.get_paginated_response(data=response)
        else:
            response = {
                "status": True,
                "message": "You haven't add any Post yet",
                "data": None
            }
            return Response(data=response, status=status.HTTP_200_OK)


class LikeView(APIView):
    # If the user is authenticated then only like post
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        # If User gives correct id then can like post
        if Post.objects.filter(id=pk).exists():
            post = Post.objects.get(id=pk)
            user = request.user.id
            '''
            pass data in serializers to check validation of
            one user can like only once.
            '''
            data = {"post": post.id, "user": user}
            serializer = LikeSerializer(data=data)

            # check serializer is valid or not
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                threading.Thread(
                    target=send_mail,
                    kwargs={
                        "subject": "About Likes on Post",
                        "content": f"{request.user} liked Your Post",
                        "recipient_list": [post.user.email]
                    }).start()
                response = {
                    "status": True,
                    "message": "Your Like is added in the post"
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    "status": False, "message": serializer.errors, "data": None
                    }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # If user give invalid id then give proper response message
        else:
            response = {
                "status": False,
                "message": "Please Provide corerct post id to Like Post",
                "data": None
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class CommentView(APIView):
    # If the user is authenticated then only comment on post
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # If User gives correct id then can comment on post
        if Post.objects.filter(id=pk).exists():
            post = Post.objects.get(id=pk)
            serializer = CommentSerializer(data=request.data)

            # If Serializer is valid then save it with user and post
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)

                # Notifications of email when user add comment
                threading.Thread(
                    target=send_mail,
                    kwargs={
                        "subject": "About Comments on Post",
                        "content": f"{request.user} commented on Your Post",
                        "recipient_list": [post.user.email]
                    }).start()

                response = {
                    "status": True,
                    "message": "Your Comment is added in the post"
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    "status": False, "message": serializer.errors, "data": None
                    }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # If user give invalid id then give proper response message
        else:
            response = {
                "status": False,
                "message": "Please Provide corerct post id to Like Post",
                "data": None
            }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
