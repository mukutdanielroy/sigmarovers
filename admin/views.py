from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os

# @login_required
# @user_passes_test(lambda u: u.is_staff)
def serve_government_id_photo(request, filename):
    print(filename)
    government_id_photos_folder = os.path.join(settings.MEDIA_ROOT, 'government_id_photos')
    file_path = os.path.join(government_id_photos_folder, filename)

    if not os.path.exists(file_path):
        raise Http404("File does not exist")

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='image/jpeg')  # Adjust content type based on your file type
        return response