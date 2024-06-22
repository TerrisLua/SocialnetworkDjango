import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File
from .models import *

# I wrote this code

# Factory class for creating User model instances for testing
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Generates a sequence of usernames, each one being unique
    username = factory.Sequence(lambda n: f"user_{n}")
    # Generates a sequence of email addresses
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    # Sets the password for the created User instance
    password = factory.PostGenerationMethodCall("set_password", "password")


# Factory class for creating AppUser model instances for testing
class AppUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser

    # Creates a related User instance using the UserFactory
    user = factory.SubFactory(UserFactory)


# Factory class for creating MediaPost model instances for testing
class MediaPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MediaPost

    # Creates a related AppUser instance using the AppUserFactory
    user = factory.SubFactory(AppUserFactory)


# Factory class for creating FriendRequest model instances for testing
class FriendRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FriendRequest

    # Creates a related AppUser instance for the sender using the AppUserFactory
    sender = factory.SubFactory(AppUserFactory)
    # Creates a related AppUser instance for the receiver using the AppUserFactory
    receiver = factory.SubFactory(AppUserFactory)
    # Generates a fake timestamp within this year
    timestamp = factory.Faker("date_time_this_year")


# Factory class for creating Image model instances for testing
class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    # Generates a sequence of image names
    name = factory.Sequence(lambda n: f"image_{n}")
    # Generates a fake image for the Image instance
    image = factory.django.ImageField()
    # Generates a fake thumbnail for the Image instance
    thumbnail = factory.django.ImageField()

# end of code I wrote
