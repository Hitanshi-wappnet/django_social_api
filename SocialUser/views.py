from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from SocialUser.models import Follow, Message
from authentication.models import User
from SocialUser.serializers import FollowSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
import threading
from services.send_mail import send_mail


class FollowUserView(APIView):
    # If the user is authenticated then only eligible to follow another user
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        # If User gives correct id then can follow other user
        if User.objects.filter(id=pk).exists():

            # Get id of following user
            following = User.objects.get(id=pk)

            # requesting user is follower
            follower = request.user
            '''
            pass data in serializers to check validation of
            one user can like only once.
            '''
            data = {"following": following.id, "follower": follower.id}
            serializer = FollowSerializer(data=data)

            # check if serializer is valid then give proper response
            if serializer.is_valid():

                # Get object of user to changes in User Model
                following_user = get_object_or_404(User, id=following.id)
                follower_user = get_object_or_404(User, id=follower.id)
                # increment the no .of following of the follower person
                follower_user.following += 1
                follower_user.save()
                # increment the no .of followers of the following person
                following_user.followers += 1
                following_user.save()
                serializer.save(follower=follower, following=following)
                response = {
                    "status": True,
                    "message": f'You are now following {following}.'
                }
                return Response(data=response, status=status.HTTP_202_ACCEPTED)
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
                "message": "Please Provide correct id to follow user",
                "data": None
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(APIView):
    # If the user is authenticated then only eligible to unfollow another user
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        # If User gives correct id then can unfollow other user
        if User.objects.filter(id=pk).exists():

            # Get id of following user
            following = User.objects.get(id=pk)

            # requesting user is follower
            follower = request.user
            '''
            If the requested user is followed to requested id user then only
            can unfollow that user
            '''
            if Follow.objects.filter(following=following,
                                     follower=follower).exists():
                unfollow = Follow.objects.get(following=following,
                                              follower=follower)
                unfollow.delete()

                # Get object of user to changes in User Model
                following_user = get_object_or_404(User, id=following.id)
                follower_user = get_object_or_404(User, id=follower.id)
                # decrement the no .of following of the follower person
                follower_user.following -= 1
                follower_user.save()
                # decrement the no .of followers of the following person
                following_user.followers -= 1
                following_user.save()
                response = {
                    "status": True,
                    "message": f'You are now unfollowing {following}.'
                }
                return Response(data=response, status=status.HTTP_202_ACCEPTED)
            else:
                response = {
                    "status": False,
                    "message": f'You are already unfollowed {following}.',
                    "data": None
                    }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # If user give invalid id then give proper response message
        else:
            response = {
                "status": False,
                "message": "Please Provide corerct id to unfollow User",
                "data": None
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class SendMessageView(APIView):

    # If sender is authenticated then only be able to send messages
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        content = request.data.get('message')
        # Check if recipient ID is exist or not
        if User.objects.filter(id=pk).exists():
            email = User.objects.get(id=pk).email
            # Get the sender, receiver and message content from requested data
            data = {'sender': request.user.id,
                    'receiver': pk,
                    'content': content}
            serializer = MessageSerializer(data=data)

            # If serializer is valid then can send the message
            if serializer.is_valid():
                serializer.save()
                threading.Thread(
                    target=send_mail,
                    kwargs={
                        "subject": "About Messages on Post",
                        "content": f"You received new message from {request.user}",
                        "recipient_list": [email]
                    }).start()
                response = {
                    'status': True,
                    'message': 'Message Sent Successfully',
                    'data': serializer.data
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            # Return an error response if the serializer is not valid
            else:
                response = {
                    'status': False,
                    'message': serializer.errors,
                    'data': None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # If the recepient id is invalid then return an proper error response
        else:
            response = {
                'status': False,
                'message': 'Please provide valid id for sending message',
                'data': None
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ReceiveMessageView(APIView):

    # If receiver is authenticated then only be able to receive message
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # Check if sender ID is exist or not
        if User.objects.filter(id=pk).exists():
            sender = User.objects.get(id=pk).username
            # Get all messages between the authenticated sender and receiver
            messages = Message.objects.filter(receiver=request.user, sender=pk)

            # set the is_read attribute True of messages
            for message in messages:
                message.is_read = True
                message.save()

            # Serialize the messages and return them in the response
            serializer = MessageSerializer(messages, many=True)
            response = {
                'status': True,
                'message': f'The messages between {sender} as sender and {request.user} as receiever',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # If the recepient id is invalid then return an proper error response
        else:
            response = {
                'status': False,
                'message': 'Please provide valid id for receiveing message',
                'data': None
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ListMessageView(APIView):

    # Only authenticared user can view the message
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # Check if sender ID is exist or not
        if User.objects.filter(id=pk).exists():
            sender = User.objects.get(id=pk).username

            # Get all messages between the authenticated sender and receiver
            messages = Message.objects.filter(
                Q(receiver=request.user, sender=pk)
                | Q(receiver=pk, sender=request.user))

            # Serialize the messages and return them in the response
            serializer = MessageSerializer(messages, many=True)
            response = {
                'status': True,
                'message': f'The messages between {sender} and {request.user}',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # If the recepient id is invalid then return an proper error response
        else:
            response = {
                'status': False,
                'message': 'Please provide valid id for receiveing message',
                'data': None
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
