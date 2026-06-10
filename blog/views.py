from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 5
    queryset = BlogPost.objects.filter(is_published=True).order_by("-created_at")


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        old_views = obj.views_count
        obj.views_count += 1
        obj.save(update_fields=["views_count"])

        if old_views < 100 <= obj.views_count:
            self.send_email(obj)

        return obj

    def send_email(self, post):
        subject = "Congratulations! Your blog has been viewed over 100 times!"
        post_url = self.request.build_absolute_uri(reverse("blog:blog_detail", args=[post.pk]))

        message = f"Статья '{post.title}' (ID: {post.pk}) набрала 100+ просмотров!\n" f"Ссылка на статью: {post_url}\n"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["kartograff13@gmail.com"]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"Ошибка отправки email: {e}")


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "blog.add_blogpost"
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "blog.change_blogpost"
    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "blog.delete_blogpost"
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
    context_object_name = "post"
