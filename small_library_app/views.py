#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from models import *
from forms import *
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
# import logging

def home(request):
	books = Book.objects.all()
	return render(request, 'home.html', {'books': books} )

def show_book(request, book_id):
    return render(request, 'show_book.html',{'book': Book.objects.get(id=book_id)}) 

def new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            ISBN = form.cleaned_data['ISBN']
            link = form.cleaned_data['link']
            published = form.cleaned_data['published']
            # description = request.FILES['description']
            new_book = Book(author=author, title=title, ISBN=ISBN, published=published, link=link)
            new_book.save()
            return HttpResponseRedirect('/small_library_app/home/')
        else:
            return render(request, 'new_book.html', {'form' : form})
    else:
        form = BookForm()
    return render(request, 'new_book.html', {'form' : form})

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('small_library_app.views.home')

def new_review(request, book_id):
    boo = Book.objects.get(id=book_id)

    if request.method == "POST":
        rf = ReviewForm(request.POST)
        if rf.is_valid():
            review = rf.save(commit=False)
            review.published = timezone.now()
            review.book = boo
            review.save()

            return HttpResponseRedirect('/small_library_app/show_book/%s' % book_id)

    else:
        rf = ReviewForm()

    args = {}
    args.update(csrf(request))
    args['book'] = boo
    args['form'] = rf

    return render(request, 'new_review.html', args)

def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews':reviews})

def show_review(request, review_id):
    return render(request, 'show_review.html', {'review': Review.objects.get(id=review_id)}) 

def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return HttpResponseRedirect('/small_library_app/show_review/%s' % review_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form})

def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    review.delete()
    return redirect('small_library_app.views.home')
