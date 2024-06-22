from .serializer import *
from .models import *
from .serializer import *
from .tasks import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# I wrote this code

# A function-based view that requires the user to be authenticated
@api_view(["GET"])
def user_detail(request, username):
    # Try to get the AppUser by the username
    try:
        app_user = AppUser.objects.get(user__username=username)
    except AppUser.DoesNotExist:
        return Response(status=404)

    # Count the media posts for this user
    media_post_count = MediaPost.objects.filter(user=app_user).count()

    # Prepare and return the response data
    data = {
        "id": app_user.user.id,
        "username": app_user.user.username,
        "status_update": app_user.status_update,
        "organisation": app_user.organisation,
        "media_post_count": media_post_count,
    }
    return Response(data)
# end of code I wrote
