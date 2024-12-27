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
    post =  get_object_or_404(Post,
                              publish__year=year,
                              publish__month=month,
                              publish__day=day,
                              slug=post,
                              status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    return (render(request,
                   'blog/post/detail.html',
                   {'posta':post, 'comments':comments, 'form':form}))

from .forms import EmailPostForm
# from django.core.mail import send_mail

def post_share(request, post_id):
    sent = False
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if (request.method == 'POST'):
        form = EmailPostForm(request.POST)
        if (form.is_valid()):
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']} comments: {cd['comments']}"
            )
            sent = True
    else:
        form = EmailPostForm()
    return (render(request,
                   'blog/post/share.html',
                   {'post': post,'form':form, 'sent': sent}))

from django.views.decorators.http import require_POST
from .forms import CommentForm

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comments = None
    form = CommentForm(data=request.POST)
    if (form.is_valid()):
        comments = form.save(commit=False) #to not save it to database directyl, cause we will modify here on the post before submitting here
        comments.post = post
        comments.save() #saved to the db
    return (render(request,
                   'blog/post/comment.html',
                   {'post':post, 'form':form, 'comments':comments}))