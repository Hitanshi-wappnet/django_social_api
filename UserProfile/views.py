from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from authentication.serializers import RegistrationSerializer
from UserProfile.serializers import ChangeProfileSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        If the request is sent by authorized User then display User Profile
        else send the error response.
        """

        # retrieve the data entered by user
        username = request.data.get("username")

        # If username is not provided then returns an error
        if username is None:
            response = {
                "status": False,
                "message": "Provide username to retrieve user profile",
                "data": None
            }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

        # check if username exists or not
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            serializer = RegistrationSerializer(instance=user)

            # return an response of User data
            response = {
                "status": True,
                "message": "User Profile of Provided User name",
                "data": serializer.data
            }
            return Response(data=response,
                            status=status.HTTP_200_OK)

        # returns an error response if user does not exist
        else:
            response = {
                "status": False,
                "message": "User does not exist!!provide correct username",
                "data": None
            }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        If the request is sent by authorized User then update User Profile
        else send the error response.
        """
        if User.objects.filter(id=pk).exists():
            user = User.objects.get(id=pk)
            serializer = ChangeProfileSerializer(user, data=request.data)
            if serializer.is_valid():

                # update user details with validated data
                serializer.save()

                # Return success response
                response = {"status": True,
                            "message": "User data updated successfully!!"}
                return Response(data=response, status=status.HTTP_202_ACCEPTED)

            else:
                # Return error response with serializer errors
                response = {"status": False,
                            "message": serializer.errors,
                            "data": None}
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {"status": False,
                        "message": "provide correct id to update profile",
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        If the request is sent by authorized User then partially update
        User Profile else send the error response.
        """
        if User.objects.filter(id=pk).exists():
            user = User.objects.get(id=pk)
            serializer = ChangeProfileSerializer(user, data=request.data,
                                                 partial=True)

            if serializer.is_valid():

                # update partial user details with validated data
                serializer.save()

                # Return success response
                response = {"status": True,
                            "message": "User data updated successfully!!"}
                return Response(data=response, status=status.HTTP_202_ACCEPTED)

            else:
                # Return error response with serializer errors
                response = {"status": False,
                            "message": serializer.errors,
                            "data": None}
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {"status": False,
                        "message": "provide correct id to update profile",
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        If the request is sent by authorized User then delete
        User Profile else send the error response.
        """
        if User.objects.filter(id=pk).exists():
            user = User.objects.get(id=pk)
            user.delete()

            # Return success response
            response = {"status": True,
                        "message": "User data of given id deleted"}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            # Return error response with serializer errors
            response = {"status": False,
                        "message": "provide correct user id to delete",
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        old_password = request.data.get("password")
        new_password = str(request.data.get("newpassword"))

        if username is None or old_password is None or new_password is None:
            response = {
                        "status": False,
                        "message": "Provide username,password and newpassword",
                        "data": None
                    }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user from the database
        if User.objects.filter(username=username).exists():

            user = User.objects.get(username=username)
            # Check if the old password matches the user's password
            if user.check_password(old_password):
                # Set the user's new password
                user.set_password(new_password)

                # Save the user object with the new password
                user.save()

                # Return success response
                response = {
                    "status": True,
                    "message": "Password Changed Successfully.",
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": False,
                    "message": "Please Provide correct password",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status": False,
                "message": "Provide Correct Credentials.",
                "data": None,
            }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)
