from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # This is creating a form from the form data sent in the request
        place = form.save(commit=False) # make a model (place) object from the form
        place.user = request.user
        if form.is_valid(): # validation against DB constrains
            place.save()  # saves place to db
            return redirect('place_list') # reloads home page

    # If no a POST, or the form is not valid, render the page
    # with the form to add a new place, and list of places  
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() #uses HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) #dictionary data


@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list') # redirect to wishlist places


def about(request):
    author = 'Suban'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Do this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()
    
    # if POST request, validate form data and update.
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)
    
    else:
        # if Get request, show Place info and optional form
        # If place is visited, show form; if place is not visited, no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/wishlist.html', {'place': place, 'review_form': review_form })
        else:
            return render(request, 'travel_wishlist/wishlist.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect(place_list)
    else:
        return HttpResponseForbidden()
    