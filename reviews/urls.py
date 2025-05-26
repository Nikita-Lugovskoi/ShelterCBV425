from django.urls import path

from reviews.apps import ReviewsConfig

from reviews.views import ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewUpdateView, \
                          ReviewDetailView, ReviewDeleteView 

app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews_list'),
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='reviews_deactivated_list'),
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    path('detail/', ReviewDetailView.as_view(), name='review_detail'),
    path('update/', ReviewUpdateView.as_view(), name='review_update'),
    path('delete/', ReviewDeleteView.as_view(), name='review_delete'),
]
