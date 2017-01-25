from django.views.generic import ListView, DetailView
from .models import Link
from django.contrib.auth import get_user_model

# Adds comment functionality including a random comment at the bottom of the page
from django_comments.models import Comment

class RandomComment(object):
    def get_context_data(self, **kwargs):
        context = super(RandomComment, self).get_context_data(**kwargs)
        context[u"quip"] = Comment.objects.order_by('?')[0]
        return context

class LinkListView(RandomComment, ListView):
    model = Link
    queryset = Link.with_votes.all()
    paginate_by = 5

class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

# Edit User Profile
from django.views.generic.edit import UpdateView
from .models import UserProfile
from .forms import UserProfileForm
from django.core.urlresolvers import reverse

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


# Create in CRUD
from django.views.generic.edit import CreateView
from .forms import LinkForm

# Read in CRUD (uses DetailView import)
class LinkDetailView(DetailView):
    model = Link

#Update and Delete in CRUD
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

class LinkEditView(UpdateView):
    model = Linkform_class = LinkForm

class LinkDeleteView(DeleteView):
    model = Link
    success_url = reverse_lazy("home")

class LinkCreateView(CreateView):
    model = Link
    form_class = LinkForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.score = 0
        f.submitter = self.request.user
        f.save()

        return super(CreateView, self).form_valid(form)