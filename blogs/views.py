from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    context_object_name = "post"
    template_name = "blogs/post_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Get likes count
        context["likes"] = models.PostLike.objects.filter(post=post).count()

        # Get all comments
        comments = models.Comment.objects.filter(post=post)
        context["comments"] = comments

        # Initialize forms
        context["post_comment_form"] = forms.PostCommentForm()
        context["post_comment_edit_form"] = forms.PostCommentEditForm()

        # Handle authenticated user specific data
        if self.request.user.is_authenticated:
            user_comment = comments.filter(user=self.request.user).first()
            context["user_comment"] = user_comment
            context["other_comments"] = comments.exclude(user=self.request.user)

            if user_comment:
                context["post_comment_edit_form"] = forms.PostCommentEditForm(
                    instance=user_comment
                )
        else:
            context["other_comments"] = comments
            context["user_comment"] = None

        return context


@login_required
def like_posts(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    like, created = models.PostLike.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        messages.success(request, "You have unliked the post.")

    liked = models.PostLike.objects.filter(user=request.user, post=post).exists()

    return render(
        request, "blogs/likes_htmx.html", {"likes": post.likes.count(), "liked": liked}
    )


def post_comment(request, pk):
    post = get_object_or_404(models.Post, id=pk)

    if request.method == "POST":
        form = forms.PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.created_at = datetime.datetime.now()
            comment.save()

            return redirect(reverse("post_detail", kwargs={"pk": pk}))
    else:
        form = forms.PostCommentForm()


def edit_comment(request, pk):
    comment = get_object_or_404(models.Comment, id=pk)

    # Ensure the user can only edit their own comments
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == "POST":
        form = forms.PostCommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(reverse("post_detail", kwargs={"pk": comment.post.id}))
    else:
        form = forms.PostCommentEditForm(instance=comment)


def delete_comment(request, pk):
    comment = get_object_or_404(models.Comment, id=pk)

    # Ensure the user can only delete their own comments
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    comment.delete()
    return redirect(reverse("post_detail", kwargs={"pk": comment.post.id}))
