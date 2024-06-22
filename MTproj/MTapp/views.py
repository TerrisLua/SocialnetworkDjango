from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from MTapp.models import *
from MTapp.forms import *
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserSearchForm
from django.contrib import messages
from .tasks import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
# I wrote this code

def index(request):
    # Render the index.html template
    return render(request, "index.html")

# Handle user registration
def register(request):
    if request.method == "POST":
        # Process POST request and validate forms
        user_form = UserForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "image" in request.FILES:
                profile.image = request.FILES["image"]
                profile.save()  # save the profile first to get the image path

                # Generate the thumbnail using the task
                make_thumbnail.delay(
                    profile.id
                )  # Assuming your AppUser model has an 'id' field

            # Add the status_update field
            profile.status_update = profile_form.cleaned_data["status_update"]

            profile.save()

            # Redirect to some location after registration
            return HttpResponseRedirect(reverse("index"))

    # For GET request, render the registration form
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )

# Chat room view
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

# Handle user login
def user_login(request):
    if request.method == "POST":
        # Retrieve username and password from POST data
        username = request.POST["username"]
        password = request.POST["password"]
        # Attempt to authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("user_home", args=[user.username]))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "login.html")

# Handle user logout
def user_logout(request):
    # Log the user out
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Display user's home page
def user_home(request, username):
    if request.user.is_authenticated:
        # Fetch the User and associated AppUser model for the given username
        users = User.objects.filter(username=username)
        user_not_found = False

        if len(users) == 0:
            user_not_found = True
            target_user = None
            profile = None
        else:
            target_user = users[0]
            profile = get_object_or_404(AppUser, user=target_user)

        # Initialize forms
        image_form = UpdateProfileImageForm(instance=profile)
        media_post_form = MediaPostForm()

        if request.method == "POST":
            if request.user.username != username:
                return HttpResponseForbidden(
                    "You don't have permission to perform this action."
                )

            print("Status Update Form Data:", request.POST)

            if "status_update" in request.POST:
                form = UpdateProfileStatusForm(request.POST, instance=profile)
                if form.is_valid():
                    form.save()
                    print("Status update saved successfully!")
                    messages.success(request, "Status update updated successfully!")
                else:
                    print("Status Update Form Validation Errors:", form.errors)

            if "image" in request.FILES:
                image_form = UpdateProfileImageForm(
                    request.POST, request.FILES, instance=profile
                )
                if image_form.is_valid():
                    image_form.save()
                    print("Image post uploaded successfully!")
                    messages.success(request, "Profile picture uploaded successfully!")
                    return HttpResponseRedirect(reverse("user_home", args=[username]))
                else:
                    print("Image Form Validation Errors:", image_form.errors)

            if "media" in request.FILES:
                media_post_form = MediaPostForm(request.POST, request.FILES)
                if media_post_form.is_valid():
                    media_post = media_post_form.save(commit=False)
                    media_post.user = request.user.appuser
                    media_post.save()
                    print("Media post uploaded successfully!", media_post.user)
                    messages.success(request, "Media post uploaded successfully!")
                    return HttpResponseRedirect(reverse("user_home", args=[username]))

        # Handle search form
        search_results = None
        form = UserSearchForm(request.GET or None)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_results = User.objects.filter(username__icontains=query)

        context = {
            "target_user": target_user,
            "profile": profile,
            "search_form": form,
            "search_results": search_results,
            "user_not_found": user_not_found,
            "image_form": image_form,
            "media_post_form": media_post_form,
            "friends": request.user.appuser.friends.all(),
            "pending_requests": FriendRequest.objects.filter(
                receiver=request.user.appuser
            ),
        }

        return render(request, "user_home.html", context)
    else:
        return HttpResponse("User not authenticated.")

# Send friend request to another user
def send_friend_request(request, user_id):
    user = request.user.appuser
    target_user = AppUser.objects.get(user__id=user_id)

    # Check if request already exists or if they are already friends
    if (
        user == target_user
        or FriendRequest.objects.filter(sender=user, receiver=target_user).exists()
        or user in target_user.friends.all()
    ):
        return HttpResponseRedirect(
            reverse("user_home", args=[target_user.user.username])
        )

    FriendRequest.objects.create(sender=user, receiver=target_user)
    return HttpResponseRedirect(reverse("user_home", args=[target_user.user.username]))

# Accept a friend request
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest, id=request_id, receiver=request.user.appuser
    )
    user = request.user.appuser
    sender = friend_request.sender

    user.friends.add(sender)
    sender.friends.add(user)

    friend_request.delete()

    return HttpResponseRedirect(reverse("user_home", args=[user.user.username]))

# Decline a friend request
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest, id=request_id, receiver=request.user.appuser
    )

    #Delete the friend request to decline it
    friend_request.delete()

    return HttpResponseRedirect(reverse("user_home", args=[request.user.username]))


# end of code I wrote

