from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Blog, Member, Request
from .models import Post
from datetime import datetime
from django.contrib.auth import logout
from welcome_page.models import Recent
from django.db.models import Q
from django.contrib import messages
from collections import deque

# Create your views here.

def popularSort(list):
    if len(list) == 0:
        return []
    return_list = [list[0]]
    for blog in list[1:]:
        if return_list[-1].number_users >= blog.number_users and len(return_list) < 5:
            return_list.append(blog)
        elif return_list[-1].number_users < blog.number_users:
            return_list.append(blog)
            cur_index = -1
            while len(return_list) >= (cur_index-1)*-1 and return_list[cur_index-1].number_users < blog.number_users:
                return_list[cur_index] = return_list[cur_index-1]
                return_list[cur_index-1] = blog
                cur_index-=1
        if len(return_list) > 5:
            return_list.pop()
    return return_list

def userAlgo(user):
    queue = deque(maxlen=10)
    for recent in Recent.objects.filter(user_for=user):
        blog = recent.recent_blog
        q = Q(Q(title__icontains=blog.title) | Q(description__icontains=blog.description))
        for i, q_blog in enumerate(Blog.objects.filter(q).all()):
            if i == 3:
                break
            if not Recent.objects.filter(user_for=user, recent_blog=q_blog):
                queue.append(q_blog)
    return queue

def index(request):
    user_blogs = []
    recents = []
    num_requests = 0
    if request.user not in User.objects.all():
        return redirect(reverse("sign_up"))
    elif not request.user.is_authenticated:
        return redirect(reverse("login"))
    if request.user.is_authenticated:
        for blog in Blog.objects.all():
            if blog.created_user == request.user:
                user_blogs.append(blog)
        for instance in Recent.objects.filter(user_for=request.user).all():
            if instance.recent_blog not in recents:
                recents.append(instance.recent_blog)
        popular = popularSort(Blog.objects.all())
        member = Member.objects.get(user=request.user)
        for _ in Request.objects.filter(user_to=member, status=0).all():
            num_requests +=1
        user_Algo = userAlgo(request.user)
        return render(request, "home/index.html", {
            "user" : request.user,
            "blogs" : Blog.objects.all(),
            "user_blogs": user_blogs,
            "recent_blogs": recents[len(recents)-3:len(recents)],
            "popular_blogs":popular,
            "user_Algo": user_Algo,
            "num_requests": num_requests
        })
def search(request):
    q_set = None
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(title__icontains=q) | Q(description__icontains=q))
        q_set = Blog.objects.filter(multiple_q)
    return render(request, "home/search.html",{
        "q_set" : q_set
    })
def requests(request):
    if request.method == "POST":
        result = request.POST["select"]
        ##print(Request.objects.get(id=result))
        result = result.split("-")#list[user_to, blog]
        print(result)
        user = Member.objects.get(id=result[0])
        blog = Blog.objects.get(id=result[1])
        if isinstance(result, list) and len(result) == 2:
            permission = Request.objects.get(user_from=result[0], blog=result[1])
            permission.status = 1
            permission.save()
            print("user", user)
            print("blog", blog)
            print(result[0], result[1])
            user.blog.add(blog)
            user.save()
        else:
            permission = Request.objects.get(user_from=result[0], blog=result[1])
            permission.status = 2
            permission.save()
    user = Member.objects.get(user=request.user)
    return render(request, "home/requests.html",{
        "permissions": Request.objects.filter(user_to=user).all()
    })
def blog_content(request, pk):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    blog = Blog.objects.get(id = pk)
    posts = blog.post.all()
    if request.method == "POST":
        txt_message = request.POST["message"]
        username = request.user.username
        post = Post.objects.create(username=username, txt_message=txt_message)
        post.save()
        blog.post.add(post)
        blog.save()
        cur_member = Member.objects.get(user=request.user)
        cur_member.blog.add(blog)
        cur_member.save()
        if not Recent.objects.filter(recent_blog=blog, user_for=request.user).exists():
            prev_users = blog.number_users
            blog.number_users = prev_users + 1
            blog.save()
        if Recent.objects.filter(recent_blog=blog, user_for=request.user).exists():
             Recent.objects.filter(recent_blog=blog, user_for=request.user).delete()
        history = Recent.objects.create(recent_blog=blog, user_for=request.user)
    if not blog.state:
        cur_member = Member.objects.get(user=request.user)
        creator = blog.created_user
        creator = Member.objects.get(user=creator)
        if (Request.objects.filter(user_from = cur_member, blog=blog, user_to=creator).exists()):
            if Request.objects.get(user_from = cur_member, blog=blog, user_to=creator).status == 0:
                messages.error(request, "Pending. Please wait")
            elif Request.objects.get(user_from = cur_member, blog=blog, user_to=creator).status == 2:
                messages.error(request, "Sorry, Request Denied")
            elif Request.objects.get(user_from = cur_member, blog=blog, user_to=creator).status == 1:
                return render(request, "home/blog_content.html", {
                    "posts" : posts,
                    "blog" : blog,
                    "username": request.user.username
                })
            return redirect(reverse("home"))
        if not Member.objects.filter(user= request.user, blog=blog).exists():
            print(blog.state)
            messages.error(request, "Cannot join requires permission. Permission of request created")
            permission = Request.objects.create(user_from=cur_member, blog=blog, user_to=creator, status=0)
            permission.save()
            return redirect(reverse("home"))
    return render(request, "home/blog_content.html", {
        "posts" : posts,
        "blog" : blog,
        "username": request.user.username
    })
def remove(request, pk, sk):
    blog = Blog.objects.get(id=pk)
    post = blog.post.get(id=sk)
    if request.method == "POST":
        cur_posts = blog.post.all()
        for post in cur_posts:
            if post.id == sk:
                post.delete()
        return redirect(reverse("blog_content", args=(blog.id,)))
    return render(request, "home/remove.html",{
        "blog":blog,
        "post":post
    })
def update(request, pk, sk):
    blog = Blog.objects.get(id=pk)
    post = blog.post.get(id=sk)
    if request.method == "POST":
        new_txt = request.POST["new-txt"]
        post.txt_message = new_txt
        post.save()
        return redirect(reverse("blog_content", args=(blog.id,)))
    return render(request, "home/update.html",{
        "blog":blog,
        "post":post
    })
def logout_user(request):
    logout(request)
    return redirect(reverse("login"))