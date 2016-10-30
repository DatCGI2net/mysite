from django.shortcuts import get_object_or_404, render,redirect

#from django.http import HttpResponse
#from django.template import loader
from .models import Post,Comment,Profile, Category, Tag
from django.contrib.auth import authenticate,login,logout
import re
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blog.forms import BootstrapAuthenticationForm
from django.views.generic.list import ListView


class CategoryView(ListView):
    
    template_name = "blog/category.html"
    
    def get_queryset(self):
        #return ListView.get_queryset(self)
        slug = self.kwargs.get('categorySlug', None)
        print 'self.kwargs:',  slug, self.kwargs
        
        category=get_object_or_404(Category, slug=slug)
        self.kwargs['category_ojbect'] = category
        print 'category:', category
        ##return category
    
        return category.post_set.all()
    
    def get_context_data(self, **kwargs):
        #return ListView.get_context_data(self, **kwargs)
        c = super(CategoryView, self).get_context_data(**kwargs)
        
        return c

class TagView(ListView):
    
    template_name = "blog/tag.html"
    
    def get_queryset(self):
        #return ListView.get_queryset(self)
        slug = self.kwargs.get('tagSlug', None)
        tag=get_object_or_404(Tag, slug=slug)
        self.kwargs['tag_ojbect'] = tag
        
        print 'tag:', tag
        ##return category
    
        return tag.post_set.all()
    
    
    def get_context_data(self, **kwargs):
        
        c = super(TagView, self).get_context_data(**kwargs)
        
        return c

def _get_category_list():
    
    return Category.objects.all()
    
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    latest_post_list=Post.objects.order_by('-pub_date')[:5]
    ##template=loader.get_template('blog/index.html')
    context={
        'latest_post_list': latest_post_list,
        'category_list': _get_category_list(),
    }
    return render(request,'blog/index.html',context)
    
def detail(request,post_id):
    post=get_object_or_404(Post, pk=post_id)
    
    return _renderPost(request, post)

def getPost(request, postSlug):
    
    post = get_object_or_404(Post, slug=postSlug)
    
    return _renderPost(request, post)
    
def _renderPost(request, post):
    
    comments = post.get_comments()
    count = len(comments)
    return render(request,'blog/post_detail.html',{'post': post, 'comment_count': count, 
                                                   'comments': comments,
                                                   'category_list': _get_category_list(),
                                                   })
    #return render(request,'blog/post_detail.html',{'post': post, 'comment_count': count, 'comments': comments})
    
def comments(request,post_id):
    pass

@login_required(login_url = '/blog/login/')
def comment(request,post_id):
    post=get_object_or_404(Post,pk=post_id)

    if len(request.POST):
        comment = Comment()
        profile = Profile.objects.get(pk=request.user.id)
        comment.commenter=profile
        comment.comments=request.POST.get('comments')
        comment.post=post
        comment.comment_date=timezone.now()
        comment.save()
    
    return redirect(post)
    
def login_user(request):
    
    error_str = ""
    if(len(request.POST)):
    
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                ## redirect_to
                url="/"
                if request.POST.get('next'):
                    url=request.POST.get('next')
                    if "login" in url:
                        url="/blog/"
                        
                if not url:
                    url="/blog/"
                    
                        
                return redirect(url)
                
            else:
                ##return render(request,'blog/login.html',{'error': 'disabled'})
                error_str ='disabled'
        else:
            ##return render(request,'blog/login.html',{'error': 'invalid account'})
            error_str ='invalid account'
    
    form = BootstrapAuthenticationForm()
        
    return render(request,'blog/login.html', {'form':form, 'error': error_str})
    
def logout_user(request):
    logout(request)
    form = BootstrapAuthenticationForm()
    return render(request,'blog/login.html', {'form':form, 'error': 'Please input your username and password'})
    
def about(request):

    pass
    
def contact(request):

    pass
    
    
    
    
    
    
    
