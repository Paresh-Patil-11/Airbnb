from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Hotel, Comment
from .forms import HotelForm, CommentForm


def home(request):
    hotels = Hotel.objects.all()
    query = request.GET.get('q')
    if query:
        hotels = hotels.filter(
            Q(title__icontains=query) | 
            Q(location__icontains=query) | 
            Q(description__icontains=query)
        )
    return render(request, 'hotels/home.html', {'hotels': hotels})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    comments = hotel.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.hotel = hotel
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('hotel_detail', pk=hotel.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommentForm()
    
    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'comments': comments,
        'form': form
    })


@login_required
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, 'Hotel added successfully!')
            return redirect('hotel_detail', pk=hotel.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HotelForm()
    
    return render(request, 'hotels/add_hotel.html', {'form': form})


@login_required
def edit_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    
    if hotel.owner != request.user:
        messages.error(request, 'You can only edit your own hotels.')
        return redirect('hotel_detail', pk=hotel.pk)
    
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hotel updated successfully!')
            return redirect('hotel_detail', pk=hotel.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HotelForm(instance=hotel)
    
    return render(request, 'hotels/edit_hotel.html', {'form': form, 'hotel': hotel})


@login_required
def delete_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    
    if hotel.owner != request.user:
        messages.error(request, 'You can only delete your own hotels.')
        return redirect('hotel_detail', pk=hotel.pk)
    
    if request.method == 'POST':
        hotel.delete()
        messages.success(request, 'Hotel deleted successfully!')
        return redirect('home')
    
    return render(request, 'hotels/delete_hotel.html', {'hotel': hotel})


@login_required
def my_hotels(request):
    hotels = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotels/my_hotels.html', {'hotels': hotels})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Welcome {username}! Your account has been created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})