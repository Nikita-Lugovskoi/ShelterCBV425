from django.urls import path
from dogs.apps import DogsConfig
from django.views.decorators.cache import cache_page, never_cache

from dogs.views import index, BreedsListView, DogBreedListVeiw, DogListView, DogCreateView, DogDetailView, DogUpdateView, \
                       DogDeleteView, DogDeactivetedListView, dog_toggle_activity

app_name = DogsConfig.name

urlpatterns = [
    # breeds
    path('', index, name='index'),
    path('breeds/', cache_page(1)(BreedsListView.as_view()), name = 'breeds'),
    
    #dogs
    path('breeds/<int:pk>/dogs/', DogBreedListVeiw.as_view(), name='breed_dogs'),
    path('dogs/', DogListView.as_view(), name='dogs_list'),
    path('dogs/', DogDeactivetedListView.as_view(), name='dogs_deactiveted_list'),
    path('dogs/create/', DogCreateView.as_view(), name='dog_create'),
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/update/<int:pk>', never_cache(DogUpdateView.as_view()), name='dog_update'),
    path('dogs/update/<int:pk>', dog_toggle_activity, name='dog_toggle_activity'),
    path('dogs/delete/<int:pk>', DogDeleteView.as_view(), name='dog_delete'),
]
