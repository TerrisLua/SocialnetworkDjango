from celery import shared_task
from .models import *
from PIL import Image as img
import io
from django.core.files.uploadedfile import SimpleUploadedFile
# I wrote this code

@shared_task
def make_thumbnail(profile_pk):
    profile = AppUser.objects.get(pk=profile_pk)
    image = img.open(profile.profile_picture.path)

    x_scale_factor = image.size[0] / 100
    thumbnail = image.resize((100, int(image.size[1] / x_scale_factor)))

    byteArr = io.BytesIO()
    thumbnail.save(byteArr, format="JPEG")

    # Adjust the filename for the thumbnail
    file_name = "thumb_" + profile.profile_picture.name.split("/")[-1]
    file = SimpleUploadedFile(file_name, byteArr.getvalue(), content_type="image/jpeg")

    profile.profile_picture.save(file_name, file, save=True)
# end of code I wrote
