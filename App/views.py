from django.shortcuts import render,redirect
from .forms import CreateUserForm,UpdateUserForm,Userupdateprofile,CreatePost,CommentsPost
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import profile as pf,Post,Comments

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

def Mypost(request):
    post = Post.objects.all()
    context = {
        'Post':post
    }
    return render(request,'MyPost.html',context)

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

def delete_comment(request,id):
    print(id)
    getcomments = Comments.objects.get(pk=id)
    getcomments.delete()
    return redirect('/')