from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile,Post,Comments

class CreateUserForm(UserCreationForm):
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input100'}),required=True,)
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}),required=True,)
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}),required=True,)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}),required=True,)
	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class UpdateUserForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input100'}),required=True)
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}),required=True)
	class Meta:
		model = User
		fields = ['username','email']

		
class Userupdateprofile(forms.ModelForm):
	class Meta:
		model = profile
		fields = ['image']

class CreatePost(forms.ModelForm):
	postImage = forms.ImageField( required=False)
	class Meta:
		model = Post
		fields = ['postImage','postText']

class CommentsPost(forms.ModelForm):
	commentText = forms.CharField( label="" ,widget=forms.Textarea(attrs={"placeholder":"Enter Comments",'class':'w-100',"rows":2, "cols":20}))
	class Meta:
		model = Comments
		fields = ['commentText']