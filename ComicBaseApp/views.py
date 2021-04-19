from django.db.models.query_utils import check_rel_lookup_compatibility
from django.shortcuts import HttpResponseRedirect, reverse, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View, FormView, ListView
from ComicBaseApp.models import ComicComment, ComicUser, ComicBook, Hold
from ComicBaseApp.forms import CommentForm, SignUpForm, LoginForm
from pprint import pprint


import requests
import environ

env = environ.Env()
environ.Env.read_env()


class AddCommentView(FormView):
    def get(self, request, id):
        template_name = "form.html"
        form = CommentForm()
        return render(request, template_name, {"form": form})

    def post(self, request, id):
        form = CommentForm(request.POST)
        if form.is_valid():
            post_user = ComicUser.objects.get(username=request.user.username)
            # fix to be preselected on click
            post_comic = ComicBook.objects.get(id=id)
            data = form.cleaned_data
            new_comment = ComicComment.objects.create(
                comment=data["comment"], user=post_user, comic_book_title=post_comic
            )
            return redirect("comicinfo", id=id)


class SignupView(View):
    def get(self, request):
        template_name = "form.html"
        form = SignUpForm()
        return render(request, template_name, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = ComicUser.objects.create_user(
                username=data["username"],
                password=data["password"],
                display_name=data["display_name"],
                bio=data["bio"],
                email=data["email"]
            )
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))


class LoginView(View):
    def get(self, request):
        template_name = "form.html"
        form = LoginForm
        return render(request, template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def index(request):
    # # from our database and show them
    # BASE_URL = "https://comicvine.gamespot.com/api/"
    # END_POINT = "issues/"
    # QUERY = "field_list=image,name,id,api_detail_url"
    # url = f"{BASE_URL}{END_POINT}?format=json&api_key={env('API_KEY')}&{QUERY}"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    # }
    # response = requests.get(url, headers=headers)
    # info = response.json()
    # issue_results = info["results"]

    html = "index.html"
    books = ComicBook.objects.all()
    context = {"issue": books}
    return render(request, html, context)


def profile_view(request, username):
    

    user = ComicUser.objects.get(username=username)
    if user.checkedout_comic:
        checked_comic = ComicBook.objects.get(id=user.checkedout_comic.id)
    else:
        checked_comic = False
    hold_books = []
    for hold in user.holds.values():
        hold_books.append(ComicBook.objects.get(id=hold['comicbook_id']))
        
    return render(request, "profile.html", {"user": user, "holds": hold_books, "checked_comic": checked_comic})


def e404(request, exception):
    html = "404.html"
    response = render(request, html)
    response.status_code = 404
    return response


def e500(request):
    html = "500.html"
    response = render(request, html)
    response.status_code = 500
    return response


class AddFavoriteView(View):
    def get(self, request, id):
        html = "profile.html"
        fav_comic = ComicBook.objects.get(id=id)
        cuser = ComicUser.objects.get(id=request.user.id)
        # add comic to user's favorites
        # Currently adding to all users favorites
        cuser.favorites.add(fav_comic)
        cuser.save()
        return redirect(profile_view, username=request.user.username)


class ComicDetailView(View):

    def get(self, request, id):

        html = "comic_detail.html"
        book = ComicBook.objects.get(id=id)
        comments = ComicComment.objects.filter(comic_book_title=book)
        context = {"book": book, "comments": comments}
        return render(request, html, context)


class CheckoutView(View):
    def get(self, request, id):
        checked_out_comic = ComicBook.objects.get(id=id)
        cuser = ComicUser.objects.get(id=request.user.id)
        checked_out_comic.is_checked_out = True
        cuser.checkedout_comic = checked_out_comic
        cuser.save()
        checked_out_comic.save()
        return redirect("comicinfo", id=id)


class ReturnView(View):
    def get(self, request, id):
        checked_out_comic = ComicBook.objects.get(id=id)
        cuser = ComicUser.objects.get(id=request.user.id)
        checked_out_comic.is_checked_out = False
        cuser.checkedout_comic = None
        cuser.save()
        checked_out_comic.save()
        return redirect("profile_view", username=cuser.username)

class HoldView(View):
    def get(self, request, id):
        comic = ComicBook.objects.get(id=id)
        cuser = ComicUser.objects.get(id=request.user.id)
        h_comic = Hold.objects.create(
            comicbook=comic,
            user=cuser
            )
        cuser.holds.add(h_comic)
        cuser.save()
        return redirect(profile_view, username=request.user.username)


class AddToDB(View):
    def api_call(self, id):
        BASE_URL = "https://comicvine.gamespot.com/api/"
        END_POINT = f"issue/4000-{id}"
        # QUERY = 'field_list=image,name,id,[issue_number],volume,description, person_credits'
        QUERY = ""
        url = f"{BASE_URL}{END_POINT}?format=json&api_key={env('API_KEY')}&{QUERY}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        info = response.json()
        issue_results = info["results"]
        return issue_results

    def add_database(self, id):
        comic = self.api_call(id)
        pprint(comic)
        if comic["person_credits"] == []:
            author = ''
        else:
            author = comic["person_credits"][0]["name"]
        ComicBook.objects.create(
            name=comic["name"],
            author=author,
            description=comic["description"],
            published_date=comic["cover_date"],
            volume=comic["volume"]["name"],
            issue=comic["issue_number"],
            image=comic["image"]["thumb_url"],
            lg_image=comic["image"]["original_url"]
            #    is_checked_out
        )

    def get(self, request, id):
        comic_api = self.api_call(id)
        pprint(comic_api)
        if not ComicBook.objects.filter(name=comic_api["name"]).first():
            self.add_database(id)
        book = ComicBook.objects.get(name=comic_api["name"])
        print(book.id)
        print("add_database")

        return redirect("comicinfo", id=book.id)


class SearchResultsView(ListView):
    def get(self, request):
        html = "search.html"

        squery = self.request.GET.get('q')
        BASE_URL = "https://comicvine.gamespot.com/api/"
        END_POINT = "search/"
        QUERY = f"query={squery}&resources=issue"
        url = f"{BASE_URL}{END_POINT}?format=json&api_key={env('API_KEY')}&{QUERY}"
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        info = response.json()
        results = info["results"]        
        context = {"issues": results}
        return render(request, html, context)
        

