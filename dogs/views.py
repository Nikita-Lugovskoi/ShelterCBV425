from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request  

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied


from dogs.models import Breed, Dog, DogParent
from dogs.forms import DogForm, DogParentForm
from users.models import UserRoles


def index(request):
    context = {
        'object_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная',
    }
    return render(request, 'dogs/index.html', context=context)


class BreedsListView(ListView):
    model = Breed
    extra_context = {
        'title': 'Все наши породы',
    }
    template_name = 'dogs/breeds.html'


class DogBreedListVeiw(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Собаки выбранной породы',
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get('pk'))
        return queryset 


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - все наши собаки',
    }
    template_name = 'dogs/dogs.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset
    
 
class DogDeactivetedListView(LoginRequiredMixin, ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - все наши собаки',
    }
    template_name = 'dogs/dogs.html'   
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


# Create Read Update Delet (CRUD)
class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create.html'
    extra_context = {
        'title': 'Добавить собаку',
    }
    success_url = reverse_lazy('dogs:dogs_list')
    
    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied
        self.object = form.save()
        self.object.owner = form.request.user
        self.object.save()
        return super().form_valid(form)
    

class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = context_data['object']
        context_data['title'] = f'Подробная информация {object_}'
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/update.html'
    
    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=2)
        if self.request.method == "POST":
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        object_ = self.get_object()
        context_data['title'] = f'Изменить собаку {object_}'
        context_data['formset'] = formset
        return context_data
    
    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

class DogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:dogs_list')
    permission_required = 'dogs.delete.dog'
    permission_denied_message = 'У вас нет нужных прав для данного действия!'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Удалить собаку {object_}'
        return context_data
    
    
def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:dogs_list'))

