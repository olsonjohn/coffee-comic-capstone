from django.shortcuts import HttpResponseRedirect, reverse, render
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View, FormView
from ComicBaseApp.models import ComicComment, ComicUser, ComicBook
from ComicBaseApp.forms import CommentForm, SignUpForm, LoginForm


import requests
import environ

env = environ.Env()
environ.Env.read_env()


class AddCommentView(FormView):
    def get(self, request):
        template_name = 'form.html'
        form = CommentForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            post_user = ComicUser.objects.filter(
                username=request.user.username).first()
            # fix to be preselected on click
            post_comic = ComicBook.objects.all().first()
            data = form.cleaned_data
            new_comment = ComicComment.objects.create(
                comment=data['comment'],
                user=post_user,
                comic_book_title=post_comic
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
            new_user = ComicUser.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))


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
                username=data.get('username'),
                password=data.get('password')
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



def index(request):
    html = 'index.html'
    BASE_URL = 'https://comicvine.gamespot.com/api/'
    END_POINT = 'issues/'
    QUERY = 'field_list=image,name,id,api_detail_url'
    url = f"{BASE_URL}{END_POINT}?format=json&api_key={env('API_KEY')}&{QUERY}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    info = response.json()
    issue_results = info['results']
    context = {'issue': issue_results}
    return render(request, html, context)

# def add_favorite(request, id):
#     current_user = ComicUser.objects.get(name=request.user.display_name)
#     comic = ComicBook.objects.get(id=id)
#     current_user.favorites.add(comic)
#     current_user.save()

#     return HttpResponseRedirect(reverse('home'))

def profile_view(request, username):
    user = ComicUser.objects.filter(username=username).first()
    # favorites = user.favorites.all()
    return render(request, 'profile.html', {'user': user})



def e404(request, exception):
    html = '404.html'
    response = (render(request, html))
    response.status_code = 404
    return response

def e500(request):
    html = '500.html'
    response = (render(request, html))
    response.status_code = 500
    return response


class ComicDetailView(View):
    
    def api_call(self, id):
        BASE_URL = 'https://comicvine.gamespot.com/api/'
        END_POINT = f'issue/4000-{id}'
        # QUERY = 'field_list=image,name,id,[issue_number],volume,description, person_credits'
        QUERY = ""
        url = f"{BASE_URL}{END_POINT}?format=json&api_key={env('API_KEY')}&{QUERY}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        info = response.json()
        issue_results = info['results']
        return issue_results


    def add_database(self, id):
        comic = self.api_call(id)
        ComicBook.objects.create(
           name = comic["name"],
           author = comic["person_credits"][0]["name"],
           description = comic["description"],
        #    published_date = comic.published_date,
        #    publisher =
           volume = comic["volume"]["name"],
           issue = comic["issue_number"],
           image = comic["image"]["thumb_url"],
           #is_checked_out           
        )        
    

    def get(self, request, id):
        html = 'comic_detail.html'        
        issue_results = self.api_call(id)
        context = {'issue': issue_results}        
        return render(request, html, context)

    def post(self, request, id):
        html = 'comic_detail.html'    
        issue_results = self.api_call(id)
        
        if not ComicBook.objects.filter(name=issue_results["name"]).first():
            self.add_database(id)
        breakpoint()
        fav_comic = ComicBook.objects.filter(name=issue_results["name"])
        cuser = ComicUser.objects.get(id=request.user.id).first()
        
        # add comic to user's favorites 
        # Currently adding to all users favorites
        cuser.favorites.add(fav_comic)
        cuser.save()

        context = {'issue': issue_results}     
        return render(request, html, context)
        
