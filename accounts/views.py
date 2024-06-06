from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from books.models import Book

from .forms import RegisterForm
from .models import User

# Create your views here.


@login_required
def logout(request):
    auth_logout(request=request)
    return redirect(reverse_lazy("accounts:login"))


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"

    def form_valid(self, form):
        form = form
        return super().form_valid(form)


class AllBooksView(LoginRequiredMixin, ListView):
    template_name = "accounts/all_books.html"
    model = Book
    context_object_name = "books"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Book.objects.all()
        elif not user.is_student:
            return Book.objects.filter(facolty=user.facolty)
        else:
            return redirect(reverse_lazy("books:home"))
