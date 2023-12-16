from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('books/', BookListView.as_view(), name='catalog'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author'),
    path('profile/', update_profile, name='profile'),
    path('profile/password-change/', UserPasswordChange.as_view(), name='password_update'),
    path('profile/favorites/', FavoritesView.as_view(), name='favorites'),
    path('register/', RegisterUser.as_view(), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
