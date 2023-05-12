from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomJWT, SignupView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', CustomJWT.as_view(), name='token'),
    path('', include(router.urls)),
]
