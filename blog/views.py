from django.urls import reverse_lazy
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
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
