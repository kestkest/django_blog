import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, decorators, mixins
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.template.loader import render_to_string, get_template
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from posts.models import Post, Tag, PostComment
from notifications.models import Notification, Action
from .forms import PostForm, PostCommentForm

User = get_user_model()


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    paginate_orphans = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context.update({'popular_tags': Tag.popular()})
        return context


class UserPostListView(ListView):
    model = Post
    paginate_by = 15
    template_name = 'posts/users_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        author = User.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(author=author)


class ByTagUserPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/post_by_user_and_tag.html'
    paginate_by = 15

    def get_queryset(self):
        author = User.objects.get(slug=self.kwargs['slug'])
        tags = Tag.objects.filter(name=self.kwargs['name'])
        tags_filtered = tags.filter(post__author=author)
        posts_ids = [tag.post.id for tag in tags_filtered]
        posts = Post.objects.filter(id__in=posts_ids)
        return posts


class PostDetailView(DetailView):

    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        form = PostCommentForm()
        # print(self.object.author.actions.all())
        comments = PostComment.objects.filter(post=self.object)
        comment_count = len(comments)
        views = self.object.add_view()
        author_slug = self.object.author.slug
        # following = self.request.user.followees.filter(slug=author_slug).exists()
        isfollowing = self.request.user.is_following(author_slug) if self.request.user.is_authenticated() else False

        context.update({'comments': comments, 'comments_count': comment_count, 'views': views})
        context.update({'isfollowing': isfollowing, 'form': form})
        return context


class PostUpdateView(mixins.UserPassesTestMixin, UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'posts/post_update.html'

    def form_valid(self, form):
        instance = form.save()
        tags = form.cleaned_data['tags']
        instance.create_tags(tags)
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

    def get_initial(self):
        initial = super().get_initial()
        tag_names = [tag.name for tag in Tag.objects.filter(post=self.object)]
        initial['tags'] = ' '.join(tag_names)
        print(self.object)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag_names = [tag.name for tag in Tag.objects.filter(post=self.object)]
        context.update({'tags': tag_names})
        return context


@login_required(login_url=settings.LOGIN_URL)
def add_commment(request, *args, **kwargs):
    if request.method == "POST" and request.is_ajax():
        form = PostCommentForm(request.POST)
        if form.is_valid():
            parent_id = int(form.cleaned_data['parent'])
            post_slug = request.POST.get('slug')
            post = Post.objects.get(slug=post_slug)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            if not parent_id:
                comment.path = []
                comment.save()
                comment.path.append(comment.id)
                comment.depth = 0
                notification = Notification(
                        from_user=request.user,
                        to_user=post.author,
                        post=post,
                        comment=comment,
                        notification_type=Notification.COMMENTED
                )
                notification.save()
                path = comment.path
            else:
                parent = PostComment.objects.get(pk=parent_id)
                comment.path = parent.path[:]
                path = parent.path
                comment.depth = parent.depth + 1
                comment.save()
                comment.path.append(comment.id)
                notification = Notification(
                        from_user=request.user,
                        to_user=comment.author,
                        post=post,
                        notification_type=Notification.REPLIED
                )

                notification.save()
            comment.content_object = notification

            comment.save()
            url = 'cid' + comment.path_as_string()
            print(url)
            html = render_to_string('comment_wrapper.html', {'post': post, 'comment': comment,
                                                             'user': request.user, 'url': url})
            return JsonResponse({'html': html, 'parent': parent_id, 'path': path, 'url': url})
    return redirect(reverse('posts:index'))


@login_required(login_url=settings.LOGIN_URL)
def add_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            tags = form.cleaned_data['tags']
            post.save()
            post.create_tags(tags)
            action = Action.objects.create(content_object=post, user=request.user, action=Action.POSTED)
            # print(action)
            return redirect(post.get_absolute_url())
    return render(request, 'posts/post_create.html', {'form': form})


class PostDeleteView(mixins.UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('posts:index')

    def test_func(self):
        return self.request.user == self.get_object().author
