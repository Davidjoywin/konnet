from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


from user_auth import views


urlpatterns = [
    path("favivon.ico", RedirectView.as_view(url="blank_profile_pics.png")),
    path('__reload__/', include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('auth/', include('user_auth.urls')),
    path('', include('post.urls')),
]

handler404 = 'user_auth.views.page_not_found'

handler500 = 'user_auth.views.server_error'


# import time
# import threading

# def test():
#     while True:
#         time.sleep(10)
#         print("hello world")
    
# t1 = threading.Thread(target=test)
# t1.start()
