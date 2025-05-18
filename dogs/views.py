from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView


from dogs.models import Breed, Dog
from dogs.forms import DogForm


def index(request):
    context = {
        'object_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная',
    }
    return render(request, 'dogs/index.html', context=context)


def breeds_list_view(request):
    context = {
        'object_list': Breed.objects.all(),
        'title': 'Питомник - Все наши породы',
    }
    return render(request, 'dogs/breeds.html', context=context)


# список собак конкретной породы
def breed_dogs_list_view(request, pk: int):
    breed_object = Breed.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(breed_id=pk),
        'title': f'Собаки породы - {breed_object.name}',
        'breed_pk': breed_object.pk,
    }
    return render(request, 'dogs/dogs.html', context=context)


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - все наши собаки',
    }
    template_name = 'dogs/dogs.html'



# Create Read Update Delet (CRUD)
class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку',
    }
    success_url = reverse_lazy('dogs:dogs_list')


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Подробная информация {object_}'
        return context_data


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Изменить собаку {object_}'
        return context_data
    
    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])


class DogDeleteView(DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:dogs_list')
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Удалить собаку {object_}'
        return context_data

