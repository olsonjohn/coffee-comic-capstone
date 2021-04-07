from django.shortcuts import HttpResponseRedirect, reverse, render
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View, FormView
from ComicBaseApp.models import ComicComment, ComicUser, ComicBook 
from ComicBaseApp.forms import CommentForm, SignUpForm, LoginForm


# def add_comment(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             post_user = ComicUser.objects.filter(username=request.user.username).first()
#             # fix to be preslected on click
#             post_comic = ComicBook.objects.all().first()
#             data = form.cleaned_data
#             new_comment = ComicComment.objects.create(
#                 comment = data['comment'],
#                 user = post_user,
#                 comic_book_title = post_comic
#             )
#             return HttpResponseRedirect(reverse('/'))
    
#     form = CommentForm()
#     return render(request, 'form.html', {'form': form})

class AddCommentView(FormView):
    def get(self, request):
        template_name = 'form.html'
        form = CommentForm()
        return render(request, template_name, {'form': form})
    def post(self, request):
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
            return HttpResponseRedirect(reverse('home'))

class SignupView(View):
    def get(self, request):
        template_name = 'form.html'
        form = SignUpForm()
        return render(request, template_name, {'form': form})
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = ComicUser.objects.create_user(username=data['username'], password=data['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))




# def signup_view(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_user = ComicUser.objects.create_user(username=data['username'], password=data['password'])
#             login(request, new_user)
#             return HttpResponseRedirect(reverse("home"))

#     form = SignUpForm()
#     return render(request, "form.html", {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(
#                 request,
#                 username = data.get('username'),
#                 password = data.get('password')
#             )
#         if user:
#             login(request, user)
#             return HttpResponseRedirect(reverse('home'))
#     form = LoginForm()
#     return render(request, 'form.html', {'form': form})


class LoginView(View):
    def get(self, request):
        template_name = 'form.html'
        form = LoginForm
        return render(request, template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username = data.get('username'),
                password = data.get('password')
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
            

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def index(request):
    return render(request, 'index.html')