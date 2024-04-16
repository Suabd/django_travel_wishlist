from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # This is creating a form from the form data sent in the request
        place = form.save() # make a model (place) object from the form
        if form.is_valid(): # validation against DB constrains
            place.save()  # saves place to db
            return redirect('place_list') # reloads home page
        
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() #uses HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) #dictionary data


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

    return redirect('place_list') # redirect to wishlist places




def about(request):
    author = 'Suban'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})