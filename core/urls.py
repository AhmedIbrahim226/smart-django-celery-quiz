from django.contrib import admin
from django.urls import path, include
from users.views import login_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', login_view, name='login-view'),
    path('admin/', admin.site.urls),

    path('instructor/', include('users.urls')),
    path('quiz/', include('quiz.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
