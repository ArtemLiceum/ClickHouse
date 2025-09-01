from django.urls import path
from .views import TopProductsAPIView, AvgCheckAPIView, PopularByAgeAPIView

urlpatterns = [
    path('top_products/', TopProductsAPIView.as_view(), name='top_products'),
    path('avg_check/', AvgCheckAPIView.as_view(), name='avg_check'),
    path('popular_by_age/', PopularByAgeAPIView.as_view(), name='popular_by_age'),
]
