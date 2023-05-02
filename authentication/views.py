import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from authentication.serializers import RegistrationSerializer
from authentication.models import VerifyOtp, UserActivationOtp
from rest_framework.permissions import IsAuthenticated
from services.send_mail import send_mail
import threading


class RegisterView(APIView):
    """
    API endpoint for register User either Employee or Manager.
    It returns success response of getting email for verify otp or error.
    """

    def post(self, request):
        # Validate user registration data with serializer
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Create a new user with validated data
            user = serializer.save()

            # set user activation False
            user.is_active = False
            user.save()

            # generate random otp
            otp = random.randint(1000, 9999)

            # Save the OTP to the database
            Otp = UserActivationOtp(user=user, otp=otp)
            Otp.save()

            # Send an email to the user containing the OTP
            threading.Thread(
                target=send_mail,
                kwargs={
                    "subject": "OTP For Activation of account",
                    "content": f"Here is your OTP For Activation of account {otp}",
                    "recipient_list": [user.email]
                }).start()

            # Return a success response.
            response = {
                "status": True,
                "message": "Email Sent!!verify otp to active your account",
                "data": None
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            # Return error response with serializer errors
            response = {"status": False,
                        "message": serializer.errors,
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpUserActivationView(APIView):
    """
    API endpoint for Resend OTP.
    It returns success response of email getting otp or error message.
    """
    def post(self, request):

        # retrieve email id entered by user
        email = request.data.get("email")

        # Check if email was provided in the request
        if email is None:
            response = {
                "status": False,
                "message": "Provide email address!!",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_200_OK)

        # Check if a user with that email exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Generate a random 4-digit OTP
            otp = random.randint(1000, 9999)

            # Save the OTP to the database
            resend_otp = UserActivationOtp(user=user, otp=otp)
            resend_otp.save()

            # Send an email to the user containing the OTP
            threading.Thread(
                target=send_mail,
                kwargs={
                    "subject": "OTP For Activation of account",
                    "content": f"Here is your OTP For Activation of account {otp}",
                    "recipient_list": [user.email]
                }).start()
            # Return a success response.
            response = {
                "status": True,
                "message": "Email Sent!!verify otp to active your account",
                "data": None
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # If no user with that email exists, return an error message
            response = {
                "status": False,
                "message": "Provide correct email id!!",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserActivationOtpView(APIView):
    """
    API endpoint for verification of registered User.
    It returns success response of verify otp or error.
    """

    def post(self, request):

        # Retrieve the otp entered by user
        user_otp = request.data.get("otp")

        # check if the user not entered data
        if user_otp is None:
            response = {"status": False,
                        "message": "Provide OTP!!",
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # Get the VerifyOtp object with the given OTP
        if UserActivationOtp.objects.filter(otp=user_otp).exists():
            otp = UserActivationOtp.objects.get(otp=user_otp)
            user = otp.user

            # If user is verified then set user activation status to True
            if user:
                user.is_active = True
                user.save()

                # Delete the otp so further reuse of otp is not possible
                otp.delete()

                # Return a success response.
                response = {
                    "status": True,
                    "message": "OTP Verified!!Registration is successfull!!",
                    "data": None
                }
                return Response(data=response, status=status.HTTP_200_OK)

            else:
                response = {
                    "status": False,
                    "message": "User does not exist",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the OTP is incorrect, return an error message
            response = {"status": False,
                        "message": "OTP is incorrect!!",
                        "data": None}

            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.User can be authenticated using email and password.
    If user is verified then get token key otherwise get error.
    """

    def post(self, request):
        # Getting the detail entered by user
        email = request.data.get("email")
        password = request.data.get("password")

        # check if the user not entered data
        if email is None or password is None:
            response = {
                "status": False,
                "message": "Provide email and password",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # Login logic using AuthTokenSerializer
        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            data = {"username": username, "password": password}
            serializer = AuthTokenSerializer(data=data)
            if serializer.is_valid():
                user = serializer.validated_data["user"]

                # generate or get token for user
                token, _ = Token.objects.get_or_create(user=user)
                token.save()
                # Return success response
                response = {
                    "status": True,
                    "message": "Login is Successful!!",
                    "data": {"token": token.key},
                }
                return Response(data=response, status=status.HTTP_202_ACCEPTED)
            else:
                response = {
                    "status": False,
                    "message": "Provide correct password",
                    "data": None,
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status": False,
                "message": "Provide correct email address",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    """
    API endpoint for Reset password.
    It returns success response of email getting otp or error message.
    """

    def post(self, request):
        # retrieve email id entered by user
        email = request.data.get("email")

        # Check if email was provided in the request
        if email is None:
            response = {
                "status": False,
                "message": "Provide email address!!",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with that email exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Generate a random 4-digit OTP
            otp = random.randint(1000, 9999)
            generated_otp = otp

            # Save the OTP to the database
            Forget_password = VerifyOtp(user=user, otp=generated_otp)
            Forget_password.save()

            # Send an email to the user containing the OTP
            threading.Thread(
                target=send_mail,
                kwargs={
                    "subject": "OTP For resetting password",
                    "content": f"Here is your OTP For Reset Password {otp}",
                    "recipient_list": [user.email]
                }).start()

            # Return a success response.
            response = {
                "status": True,
                "message": "Email sent to Reset your password!!",
                "data": None
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # If no user with that email exists, return an error message
            response = {
                "status": False,
                "message": "Provide correct email id!!",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpForgetPasswordView(APIView):
    """
    API endpoint for Resend OTP.
    It returns success response of email getting otp or error message.
    """
    def post(self, request):

        # retrieve email id entered by user
        email = request.data.get("email")

        # Check if email was provided in the request
        if email is None:
            response = {
                "status": False,
                "message": "Provide email address!!",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_200_OK)

        # Check if a user with that email exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Generate a random 4-digit OTP
            otp = random.randint(1000, 9999)

            # Save the OTP to the database
            resend_otp = VerifyOtp(user=user, otp=otp)
            resend_otp.save()

            # Send an email to the user containing the OTP
            threading.Thread(
                target=send_mail,
                kwargs={
                    "subject": "OTP For reseting password",
                    "content": f"Here is your OTP For Reset Password {otp}",
                    "recipient_list": [user.email]
                }).start()
            # Return a success response.
            response = {
                "status": True,
                "message": "Email sent to Reset your password!!",
                "data": None
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # If no user with that email exists, return an error message
            response = {
                "status": False,
                "message": "Provide correct email id!!",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    """
    This view handles verifying an OTP of Forget Password user.
    If the otp is verified then generate new token else get error message.
    """

    def post(self, request):
        # get the otp entered by user
        new_otp = request.data.get("otp")

        # check if user not entered data
        if new_otp is None:
            response = {"status": False,
                        "message": "Provide OTP!!",
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # Get the Verifyotp object with the given OTP
        if VerifyOtp.objects.filter(otp=new_otp).exists():
            forget_password = VerifyOtp.objects.get(otp=new_otp)
            user = forget_password.user

            if user:
                # Delete the user's old auth token and generate a new one
                token = Token.objects.get(user=forget_password.user)
                token.delete()
                forget_password.delete()
                token = Token.objects.create(user=user)
                token.save()
                # Return a success response.
                response = {
                    "status": True,
                    "message": "OTP Verified SuccessFully!!",
                    "data": {"token": token.key},
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": False,
                    "message": "User does not exist",
                    "data": None,
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the OTP is incorrect, return an error message
            response = {"status": False,
                        "message": "OTP is incorrect!!",
                        "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):

    # Allow only authenticated users
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        # retrieve username and new password from user entered data
        username = request.data.get("username")
        new_password = request.data.get("newpassword")

        if username is None or new_password is None:
            response = {
                "status": False,
                "message": "Provide username and newpassword.",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # Get the user object based on the username
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            # Set the user's password to the new password and save
            user.set_password(new_password)
            user.save()

            # Return a success response.
            response = {
                "status": True,
                "message": "Password Changed Successfully.",
                "data": None
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": False,
                "message": "Provide Correct username.",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    """
    API view for user logout.
    User can logout by deleting the authentication token.
    """

    def post(self, request):

        # Get the user's token
        token = Token.objects.get(user=request.user)
        token.delete()

        # Return success response
        response = {"status": True,
                    "message": "Logout is Successful!!",
                    "data": None}
        return Response(data=response, status=status.HTTP_200_OK)
