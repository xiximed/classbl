from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('badword.urls'))
]
handler404 = 'badword.views.error_404_view'
# handler500 = 'badword.views.error_404_view'
#handler404 = views.error_404
