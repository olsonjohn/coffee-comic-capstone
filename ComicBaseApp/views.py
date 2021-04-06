from django.shortcuts import HttpResponseRedirect, reverse, render

from ComicBaseApp.models import ComicComment, ComicUser, ComicBook
from ComicBaseApp.forms import CommentForm

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_user = ComicUser.objects.filter(username=request.user.username).first()
            # fix to be preslected on click
            post_comic = ComicBook.objects.all().first()
            data = form.cleaned_data
            new_comment = ComicComment.objects.create(
                comment = data['comment'],
                user = post_user,
                comic_book_title = post_comic
            )
            return HttpResponseRedirect(reverse('/'))
    
    form = CommentForm()
    return render(request, 'form.html', {'form': form})
    