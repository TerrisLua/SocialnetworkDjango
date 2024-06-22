from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .model_factories import *
from .serializer import *

# I wrote this code

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = AppUserFactory()
        self.media_post = MediaPostFactory(user=self.user)
        self.friend_request = FriendRequestFactory(sender=self.user)
        self.image = ImageFactory()

    def tearDown(self):
        AppUser.objects.all().delete()
        MediaPost.objects.all().delete()
        FriendRequest.objects.all().delete()

    def test_create_app_user(self):
        self.assertEqual(AppUser.objects.count(), 2)

    def test_create_media_post(self):
        self.assertEqual(MediaPost.objects.count(), 1)  

    def test_create_friend_request(self):
        self.assertEqual(FriendRequest.objects.count(), 1)

    def test_create_image(self):  # New test for the Image model
        self.assertEqual(Image.objects.count(), 1)


class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = UserFactory.create(username="testuser", password="testpassword")
        self.app_user = AppUserFactory.create(user=self.user)

    def tearDown(self):
        AppUser.objects.all().delete()
        MediaPost.objects.all().delete()
        FriendRequest.objects.all().delete()

    def test_user_login_success(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 302)  # Successful login redirects
        self.assertRedirects(response, reverse("user_home", args=["testuser"]))

    def test_user_login_failure(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)  # Failed login returns to login page
        self.assertContains(response, "Invalid login details supplied.")

    def test_user_logout(self):
        self.client.login(username="testuser", password="testpassword")  # Log in user
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Successful logout redirects
        self.assertRedirects(response, reverse("index"))

    def test_user_home_authenticated(self):
        self.client.login(username="testuser", password="testpassword")  # Log in user
        response = self.client.get(reverse("user_home", args=["testuser"]))
        self.assertEqual(response.status_code, 200)

    def test_user_home_unauthenticated(self):
        response = self.client.get(reverse("user_home", args=["testuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User not authenticated.")

    def test_send_friend_request(self):
        self.client.login(username="testuser", password="testpassword")  # Log in user
        response = self.client.get(reverse("send_friend_request", args=[self.app_user.id]))
        self.assertEqual(response.status_code, 302)  # Successful friend request sends
        self.assertRedirects(response, reverse("user_home", args=[self.app_user.user.username]))

    def test_accept_friend_request(self):
        sender = AppUserFactory.create()
        friend_request = FriendRequestFactory.create(sender=sender, receiver=self.app_user)
        self.client.login(username="testuser", password="testpassword")  # Log in user
        response = self.client.get(reverse("accept_friend_request", args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)  # Successful friend request acceptance
        self.assertRedirects(response, reverse("user_home", args=[self.app_user.user.username]))

    def test_decline_friend_request(self):
        sender = AppUserFactory.create()
        friend_request = FriendRequestFactory.create(sender=sender, receiver=self.app_user)
        self.client.login(username="testuser", password="testpassword")  # Log in user
        response = self.client.get(reverse("decline_friend_request", args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)  # Successful friend request decline
        self.assertRedirects(response, reverse("user_home", args=[self.app_user.user.username]))

    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

class UserDetailAPITestCase(APITestCase):
    
    def setUp(self):
        # Initialize the API client
        self.client = APIClient()

        # Create a test user and an associated AppUser object using factories
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.app_user = AppUserFactory.create(user=self.user)

        # Create some media posts for this user
        MediaPostFactory.create_batch(5, user=self.app_user)

        # Generate a token for the user and set it in the client's headers
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_authenticated_user_detail(self):
        url = reverse('user_api', kwargs={'username': self.user.username})
        response = self.client.get(url)
        
        # Check if status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the data returned in the response matches the user's data
        self.assertEqual(response.data['id'], self.app_user.user.id)
        self.assertEqual(response.data['username'], self.app_user.user.username)
        self.assertEqual(response.data['status_update'], self.app_user.status_update)
        self.assertEqual(response.data['organisation'], self.app_user.organisation)
        self.assertEqual(response.data['media_post_count'], 5)


# end of code I wrote
