from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import F, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Category, Blog, Comment, Profile, BlogLike
from .forms import ProfileForm, BlogForm

# Home page - shows all blogs
def home_page(request):
    blogs = Blog.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    # Search and filter functionality
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'blog.html', context)

# Blog list page
def blog_list(request):
    blogs = Blog.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'blog.html', context)

# Blog detail page
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.status != 'published' and (not request.user.is_authenticated or blog.author != request.user):
        return redirect('blog_list')
    Blog.objects.filter(pk=pk).update(views=F('views') + 1)
    blog.refresh_from_db(fields=['views'])
    comments = blog.comment_set.all().order_by('-created_at')
    categories = Category.objects.all()
    
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            content = request.POST.get('comment', '')
            if content:
                Comment.objects.create(
                    content=content,
                    author=user,
                    blog=blog
                )
                messages.success(request, 'Izoh muvaffaqiyatli qo‘shildi.')
                return redirect('blog_detail', pk=pk)
        else:
            messages.error(request, 'Izoh qoldirish uchun tizimga kiring.')
            return redirect('blog_detail', pk=pk)
    
    context = {
        'blog': blog,
        'comments': comments,
        'categories': categories,
        'like_count': BlogLike.objects.filter(blog=blog).count(),
        'user_liked': request.user.is_authenticated and BlogLike.objects.filter(blog=blog, user=request.user).exists(),
    }
    return render(request, 'blog_detail.html', context)

# Categories page
def categories_page(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'categories.html', context)

# Category detail page
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    blogs = Blog.objects.filter(category=category, status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'category': category,
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog.html', context)

# Contact page
def contact_page(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # You can save this to a database or send an email
        if name and email and subject and message:
            messages.success(request, 'Xabaringiz yuborildi!')
            return redirect('contact')
        else:
            messages.error(request, 'Iltimos, barcha maydonlarni to‘ldiring.')
    
    context = {
        'categories': categories,
    }
    return render(request, 'contact.html', context)

# Register page
def register(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        # Validate inputs
        if not username or not email or not password or not password2:
            messages.error(request, 'Iltimos, barcha maydonlarni to‘ldiring.')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Parollar mos emas.')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, 'Parol kamida 6 ta belgidan iborat bo‘lsin.')
            return redirect('register')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu foydalanuvchi nomi band.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu email allaqachon ro‘yxatdan o‘tgan.')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, 'Hisob yaratildi! Endi tizimga kiring.')
        return redirect('login')
    
    context = {
        'categories': categories,
    }
    return render(request, 'register.html', context)

# Login page
def login_view(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Xush kelibsiz, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri.')
            return redirect('login')
    
    context = {
        'categories': categories,
    }
    return render(request, 'login.html', context)

# Logout page
def logout_view(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz!')
    return redirect('home')



@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    categories = Category.objects.all()
    user_blogs = Blog.objects.filter(author=request.user).order_by('-created_at')

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            blog_form = BlogForm()
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profil yangilandi.')
                return redirect('profile')
        elif 'blog_submit' in request.POST:
            blog_form = BlogForm(request.POST, request.FILES)
            profile_form = ProfileForm(instance=profile)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.author = request.user
                if not request.user.is_staff:
                    blog.status = 'draft'
                if not blog.excerpt:
                    blog.excerpt = (blog.content or '')[:300]
                blog.save()
                blog_form.save_m2m()
                messages.success(request, 'Blog yaratildi.')
                return redirect('profile')
        else:
            profile_form = ProfileForm(instance=profile)
            blog_form = BlogForm()
    else:
        profile_form = ProfileForm(instance=profile)
        blog_form = BlogForm()

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'blog_form': blog_form,
        'user_blogs': user_blogs,
        'categories': categories,
    }
    return render(request, 'profile.html', context)


@login_required
def blog_like(request, pk):
    blog = get_object_or_404(Blog, pk=pk, status='published')
    existing = BlogLike.objects.filter(blog=blog, user=request.user).first()
    if existing:
        existing.delete()
        messages.info(request, 'Like olib tashlandi.')
    else:
        BlogLike.objects.create(blog=blog, user=request.user)
        messages.success(request, 'Like qo‘shildi.')
    return redirect('blog_detail', pk=pk)


@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            updated = form.save(commit=False)
            if not request.user.is_staff:
                updated.status = blog.status
            if not updated.excerpt:
                updated.excerpt = (updated.content or '')[:300]
            updated.save()
            form.save_m2m()
            messages.success(request, 'Blog yangilandi.')
            return redirect('profile')
    else:
        form = BlogForm(instance=blog)

    context = {
        'form': form,
        'blog': blog,
        'categories': categories,
    }
    return render(request, 'blog_edit.html', context)


@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog o‘chirildi.')
        return redirect('profile')

    context = {
        'blog': blog,
        'categories': categories,
    }
    return render(request, 'blog_delete.html', context)
