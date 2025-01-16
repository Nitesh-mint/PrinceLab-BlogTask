from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


from . import models
from . import forms


class Home(ListView):
    model = models.Post
    context_object_name = "posts"
    template_name = "blogs/home.html"
    paginate_by = 5

    def get_template_name(self):
        if self.request.htmx:
            return ["blogs/post_list_htmx.html"]
        return ["blogs/home.html"]

class PostDetailView(DetailView):
    model = models.Post
    context_object_name = 'post'
    template_name = 'blogs/post_detail_view.html'

    #show comments, and likes 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        likes = models.PostLike.objects.filter(post=post).count()
        comments = models.Comment.objects.filter(post=post)
        other_comments = comments.exclude(user=self.request.user)

        context['likes'] = likes
        context['comments'] = comments
        context['other_comments'] = other_comments
        context['post_comment_form'] = forms.PostCommentForm
        context['post_comment_edit_form'] = forms.PostCommentEditForm()
        if self.request.user.is_authenticated:
            user_comment = comments.filter(user=self.request.user).first()
            context['user_comment'] = user_comment
            context['post_comment_edit_form'] = forms.PostCommentEditForm(instance=user_comment)
        return context
 
@login_required
def like_posts(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    like, created = models.PostLike.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    liked = models.PostLike.objects.filter(user=request.user, post=post).exists()
    return render(request, 'blogs/likes_htmx.html', {'likes': post.likes.count(), 'liked': liked})

class PostCommentView(CreateView):
    model = models.Comment
    form_class = forms.PostCommentForm
    template_name = 'blogs/post_comment.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(models.Post, id=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.created_at = datetime.datetime.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the post detail page after commenting
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})


class EditCommentView(UpdateView):
    model = models.Comment
    form_class = forms.PostCommentEditForm
    template_name = 'blogs/post_comment_edit_view.html'


    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})

