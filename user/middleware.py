from django.http import HttpResponse

class MediaAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the requested URL is under /media/government_id_photos/
        if request.path.startswith('/media/government_id_photos/'):
            # If user is not authenticated, redirect to login page
            if not request.user.is_authenticated:
                message = "You don't have permission to access this page."
                return HttpResponse(message, status=403)
            # If user is authenticated but doesn't have permission, return permission denied
            elif not request.user.has_perm('user.view_government_id_photos'):
                return HttpResponse("You don't have permission to access this page", status=403)  # 403 Forbidden
        
        return self.get_response(request)
