from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Comment
from .forms import CommentForm


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        search_query = request.GET.get('search')
        if search_query:
            products = products.filter(name__icontains=search_query)
        return render(request, 'home/home.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        comments = Comment.objects.filter(product=product, is_active=True)
        form = CommentForm()
        return render(request, 'home/product_detail.html', {
            'product': product,
            'comments': comments,
            'form': form
        })


class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)

        search_query = request.GET.get('search')
        if search_query:
            products = products.filter(name__icontains=search_query)


        paginator = Paginator(products, 8)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'home/product_list.html', {'page_obj': page_obj})



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
