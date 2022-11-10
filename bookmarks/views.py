from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse

from bookmarks.forms import BookmarkModelForm
from bookmarks.models import Bookmark

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class BookmarkList(generic.ListView):
    template_name = 'bookmarks/bookmark_list.html'
    queryset = Bookmark.objects.all()

@method_decorator(login_required, name='dispatch')
class BookmarkListByTag(generic.ListView):
    template_name = 'bookmarks/bookmark_list.html'

    def get_queryset(self):
        tag = self.request.GET.get('tag')
        queryset = Bookmark.objects.filter(tags__name__in=[tag])
        return queryset

@method_decorator(login_required, name='dispatch')
def create_bookmark(request):
    form = BookmarkModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('bookmarks'))
    context = {
        'form': form
    }
    return render(request, 'bookmarks/create_bookmark.html', context)

@method_decorator(login_required, name='dispatch')
def edit_bookmark(request, slug):
    bookmark = get_object_or_404(Bookmark, slug=slug)
    form = BookmarkModelForm(request.POST or None, instance=bookmark)
    if form.is_valid():
        form.save()
        return redirect(reverse('bookmarks'))
    context = {
        'form': form
    }
    return render(request, 'bookmarks/create_bookmark.html', context)

@method_decorator(login_required, name='dispatch')
def delete_bookmark(request, slug):
    bookmark = get_object_or_404(Bookmark, slug=slug)
    bookmark.delete()
    return redirect(reverse('bookmarks'))
