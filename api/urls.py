from django.urls import path, include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PostsViewSet, CommentViewsSet, GroupViewsSet, FollowViewsSet
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
comment_router = routers.NestedSimpleRouter(router, r'posts', lookup='posts')
comment_router.register(r'comments', CommentViewsSet, basename='comments') 
router.register('group', GroupViewsSet, basename='group')   
router.register('follow', FollowViewsSet, basename='follow')   


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(comment_router.urls)),
    
]