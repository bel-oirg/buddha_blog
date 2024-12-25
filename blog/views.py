from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

#some exception could be used EmptyPage, PageNotAnInteger

from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# EQUIVALENT

def post_list(request):
    posts_list = Post.published.all()

    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    #we could use except : with no exception
    
    return render(request, 'blog/post/list.html', {'posts' : posts})

def post_detail(request, year, month, day, post):
    post =  get_object_or_404(Post, publish__year=year, publish__month=month, publish__day=day, slug=post, status=Post.Status.PUBLISHED)
    # try:
    #     post = Post.published.get(id=id)
    # except:
    #     raise Http404("Post not found")
    return (render(request, 'blog/post/detail.html', {'posta':post}))

