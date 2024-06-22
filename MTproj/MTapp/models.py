from django.db import models
from django.contrib.auth.models import User  
# I wrote this code

# Model to extend the built-in User model
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the built-in User model
    status_update = models.TextField(blank=True, null=True)  # Status updates for the user, can be blank or null
    organisation = models.CharField(max_length=256, null=True, blank=True)  # Organisation info, can be blank or null
    image = models.ImageField(blank=False, default="defaultdp.jpg")  # Profile image, has a default value
    thumbnail = models.FileField(null=True)  # Thumbnail for the profile image, can be null
    friends = models.ManyToManyField("self", blank=True)  # Friends list, can be blank

    def __unicode__(self):
        return self.user.username 
    

# Model to store Image data
class Image(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)  # Image name, unique and indexed for fast lookup
    image = models.ImageField(blank=False)  # The actual image file
    thumbnail = models.FileField(null=True)  # A thumbnail for the image, can be null

    def __str__(self):
        return self.name  # String representation of the model

# Model to store media posts
class MediaPost(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)  # The user who made the post
    media = models.ImageField(blank=True)  # Media associated with the post, can be blank
    text_content = models.TextField(blank=True)  # Text content of the post, can be blank

    def __str__(self):
        return f"Media Post by {self.user.user.username}"  

# Model to store friend requests
class FriendRequest(models.Model):
    sender = models.ForeignKey(
        AppUser, related_name="sent_requests", on_delete=models.CASCADE
    )  # The user who sent the friend request
    receiver = models.ForeignKey(
        AppUser, related_name="received_requests", on_delete=models.CASCADE
    )  # The user who will receive the friend request
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the friend request was sent

# end of code I wrote
