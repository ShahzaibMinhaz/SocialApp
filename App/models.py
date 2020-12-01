from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to="profile_pics")

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    postText = models.CharField(max_length=100)
    postImage = models.ImageField(upload_to="post_pics")
    postLikes = models.ManyToManyField(profile)
    postdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.postText

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    commentText = models.CharField(max_length=50)
    commentdate = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.user.username

# class friendrequest(models.Model):
#     send = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
#     recieve = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever')


    # def __str__(self):
    #     return self.send.username

class friends(models.Model):
    status = (
        ("Requested", "requested"),
        ("Confirmed", "confirmed"),
        ("Ignore", "Ignore"),
    )
    current_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='current_user')
    friend_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend_user')
    status = models.CharField(max_length=20,choices=status,null=True)

    # def __str__(self):
    #     return self.send,username

