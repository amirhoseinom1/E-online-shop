from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Product
from .models import Comment
from .forms import CommentForm



class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create(
                email=cd['email'],
                phone_number=cd['phone'],
                full_name=cd['full_name']
            )
            user.set_password(cd['password'])
            user.save()
            messages.success(request, 'Account created successfully ', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form':form})



class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Email or password is incorrect', 'danger')
        return render(request, self.template_name, {'form': form})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are logged out successfully', 'success')
        return redirect('home:home')




class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is waiting for approval.')
        else:
            messages.error(request, 'Something went wrong. Please try again.')

        return redirect('home:product_detail', slug=product.slug)

