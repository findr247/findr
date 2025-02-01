from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from core.models import ItemImage, Item, Location, User, ClaimItem, ItemProof
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views, authenticate, login
from .forms import CustomAuthenticationForm
from django.forms import ValidationError


# Custom test function to check if user is an admin
def admin_check(user):
    return user.is_staff


class CustomLoginView(auth_views.LoginView):
    template_name = 'signin-ad.html'
    authentication_form = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.GET.get('next', '/staff/'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user is not None and user.is_staff:
            login(self.request, user)
            return redirect(self.request.GET.get('next', '/staff/'))
        else:
            form.add_error(None, ValidationError("Only staff members can log in."))
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@user_passes_test(admin_check, login_url='/staff/login/')
def dashboard(request):
    items = Item.objects.all().order_by('-id')[:12]
    stat = {

        'lost': Item.objects.filter(status="lost").count(),
        'found': Item.objects.filter(status="found").count(),
        'claimed': Item.objects.filter(status="found", claimed_by__isnull=False).count(),
    }
    return render(request, 'dashboard.html', {'stat': stat, 'recent': items})


@user_passes_test(admin_check, login_url='/staff/login/')
def item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item-detail-ad.html', {'item': item})


def items_list(request):
    status = request.GET.get('status', None)
    if status:
        items = Item.objects.filter(status=status) if not status == 'claimed' else ClaimItem.objects.all()
        return render(request, 'items-ad.html', {'items': items, 'status': status})
    else:
        items = Item.objects.all()
        return render(request, 'items-ad.html', {'items': items, 'all': 'All '})


def item_claimed(request, claim_id):
    item = ClaimItem.objects.get(id=claim_id)
    return render(request, 'claimed.html', {'item': item})


def users(request):
    Users_list = User.objects.all()
    return render(request, 'user-ad.html', {'users': Users_list})
