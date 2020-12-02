from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import (authenticate,
                                 login as auth_login,logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import (CreateUserForm,
                    UpdateUserForm,
                    Userupdateprofile,
                    CreatePost,
                    CommentsPost)
from .models import profile as pf,Post,Comments,friends
from django.db.models import Q

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username').lower()
                print(username)
                form.save()
                messages.SUCCESS = (request, 'Acount Created')
                return redirect('/login')
            else :
                error = form.errors
                print(error.as_data)
                messages.info(request, error)
                # return redirect('/')
                # return render(request,'index.html',{'form':form,'error':error})
        form = CreateUserForm()
        return render(request,'register.html',{'form':form})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            '''
            this block will check the POST request
            '''
            # path = request.path
            print(request.POST['username'])
            username = request.POST['username']
            password = request.POST['pass']
            user = authenticate(request,username=username,password=password)

            if user is not None:
                auth_login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')
                # return render(request,'login.html')
        else:
            print('No Post request')
        return render(request,'login.html')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('/login') 

@login_required
def profile(request,id):
    user_data = User.objects.get(pk=id)
    userprofile = pf.objects.get(user=user_data)
    form = UpdateUserForm(instance=user_data)
    Profileform = Userupdateprofile(instance=userprofile)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST,instance=user_data)
        Profileform = Userupdateprofile(request.POST, request.FILES, instance=userprofile)  
        if form.is_valid():
            Profileform.save()
            form.save()
            print("Details Saved")

            return redirect('/')   
            # messages.SUCCESS = (request, 'Details Saved')
        if form.errors:
            print(form.errors)
            messages.info(request,form.errors)
    context = {
        'form':form,
        'profile':Profileform  
    }
    return render(request,'profile.html',context)

@login_required
def home(request):
    PostCreateform = CreatePost()
    CommentsPostform = CommentsPost()
    if request.method == "POST":
        # print(request.POST)
        # print(request.FILES)
        PostCreateform = CreatePost(request.POST,request.FILES)
        if PostCreateform.is_valid():
            myform=PostCreateform.save(commit=False)
            myform.user=request.user
            myform.save()
            messages.info(request,"Post Created")
            return redirect('/')
        else:
            print(PostCreateform.errors)
    post = Post.objects.all()
    comment_Post = Comments.objects.all()
    context = {
        'form':PostCreateform,
        'Post':post,
        'comment_Post':comment_Post,
        'Commentform':CommentsPostform
    }
    return render(request,'home.html',context)

@login_required
def Mypost(request):
    comment_Post = Comments.objects.all()
    post = Post.objects.all()
    CommentsPostform = CommentsPost()
    context = {
        'Post':post,
        'comment_Post':comment_Post,
        'Commentform':CommentsPostform
    }
    return render(request,'MyPost.html',context)

@login_required
def addcomments(request,id):
    getPost = Post.objects.get(pk=id)
    print(id)
    print(request.POST)
    if request.method == "POST":
        CommentsPostform = CommentsPost(request.POST)
        if CommentsPostform.is_valid():
            myform=CommentsPostform.save(commit=False)
            myform.post= getPost
            myform.user=request.user
            myform.save()
            return redirect('/')


@login_required
def delete_comment(request,id):
    print(id)
    getcomments = Comments.objects.get(pk=id)
    getcomments.delete()
    return redirect('/')


@login_required
def findothers(request):
    user = User.objects.all()
    # filter friends data   
    friend = friends.objects.filter(current_user=request.user)
    print(friend)
    findotherdata = []
    for data in friend:
        if data.current_user == request.user and data.status != "Ignore":
            print(data.friend_user)
            findotherdata.append(data.friend_user)
    friend = friends.objects.filter(friend_user=request.user)
    print(friend)
    for data in friend:
        if data.friend_user == request.user and data.status != "Ignore":
            if data.current_user in findotherdata:
                continue
            else:
                findotherdata.append(data.current_user)
    return render(request,'findothers.html',{'user':user,'findotherdata':findotherdata})


@login_required
def sendfriendrequset(request,user_id,friends_id):
    userdata = User.objects.get(pk=user_id)
    frienddata = User.objects.get(pk=friends_id)
    sendrequest = friends.objects.create(current_user=userdata,friend_user=frienddata,status="Requested")
    print('friend requset send ') 
    return redirect('/findothers')


def getfriendrequest(request):
    getfriendrequest = friends.objects.filter(friend_user=request.user,status="Requested")
    return render(request,'friendrequest.html',{'getfriendrequest':getfriendrequest})


@login_required
def friend(request):
    friend = friends.objects.filter(current_user=request.user,status='Confirmed')
    print(friend)
    friend2 = friends.objects.filter(friend_user=request.user,status='Confirmed')
    print(friend2)
    context = {
        'friends':friend,
        'friend2':friend2
    }
    return render(request,'Friends.html',context)

@login_required
def accept_friendrequest(request,friendstable_id):
    print(friendstable_id)
    getfrienddata = friends.objects.get(pk=friendstable_id)
    getfrienddata.status = "Confirmed"
    getfrienddata.save()
    return redirect('/getfriendrequest')

@login_required
def unfriend(request,friendstable_id):
    print('id',friendstable_id)
    getfrienddata = friends.objects.get(pk=friendstable_id)
    getfrienddata.status = "Ignore"
    getfrienddata.save()
    return redirect('/friends')

@login_required
def updateLike(request,id):
    getpost = Post.objects.get(pk=id)
    # print(getpost.postLikes.all())
    if request.user.profile in getpost.postLikes.all():
        getpost.postLikes.remove(request.user.profile)
    else:
        getpost.postLikes.add(request.user.profile)
    return redirect('/')

def datafriends(request):
    friend = friends.objects.filter(
        Q(current_user=request.user)
        | Q(friend_user=request.user)
    )[1]
    return HttpResponse(friend.friend_user)
