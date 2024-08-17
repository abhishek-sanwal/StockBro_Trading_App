
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def signup(request):

    form = UserCreationForm(request.POST or None)

    if form.is_valid():

        form.save()

        return redirect("login")

    return render(request,
                  template_name="authy/signup.html",
                  context={
                      "form": form
                  })
