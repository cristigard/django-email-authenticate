from django.shortcuts import render,redirect
from .models import CustomUser
from .admin import UserCreationForm
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin



def home(request):
	return render(request, 'users/home.html')


def register(request):
	form = UserCreationForm()
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'users/register.html', {'form':form})


@login_required()
def profile(request):
	form = UserUpdateForm(instance = request.user)
	if request.method == "POST":
		form = UserUpdateForm(request.POST, request.FILES, instance = request.user)
		if form.is_valid():
			print(request.FILES.get('image'))
			form.save()
			return redirect('profile')
	else:
		form = UserUpdateForm(instance = request.user)

	return render(request, 'users/profile.html', {'form':form})


class UserLoginView(LoginView):
	template_name = 'users/login.html'
	fields = '__all__'
	# redirect_authenticated_user = True 
	# def get_success_url(self): # + redirect_authenticated_user = True -> send to other view if user is already auth and try to access login page
	# 	return reverse_lazy('home')


class UserLogoutView(LogoutView):
	next_page = 'home'


class UserChangePassView(LoginRequiredMixin, PasswordChangeView):   
	template_name = 'users/password_change_form.html'
	success_url = reverse_lazy('password_change_done')

class UserChangePassDoneView(LoginRequiredMixin, PasswordChangeDoneView):
	template_name = 'users/password_change_done.html'

