from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from core.models import ItemImage, Item, Location, User, ClaimItem, ItemProof
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views, authenticate, login
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        'verify': ClaimItem.objects.filter(is_rejected=False, more_info=False, item__claimed_by__isnull=True).count()
    }
    return render(request, 'dashboard.html', {'stat': stat, 'recent': items})


@user_passes_test(admin_check, login_url='/staff/login/')
def item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        claim = ClaimItem.objects.get(id=request.POST.get('item_id'))
        print(request.POST)
        if request.POST.get('approved'):
            item.claimed_by = claim.claimed_by
            item.save()
            send_claim_status_email(claim, 'approved')
        if request.POST.get('rejected'):
            claim.is_rejected = True
            claim.save()
            send_claim_status_email(claim, 'rejected')
        if request.POST.get('request'):
            claim.more_info = True
            claim.save()
            send_claim_status_email(claim, 'request')
        return redirect('items_ad')
    return render(request, 'item-detail-ad.html', {'item': item})


@user_passes_test(admin_check, login_url='/staff/login/')
def items_list(request):
    status = request.GET.get('status', None)
    if status:
        items = Item.objects.filter(status=status) if not status == 'claimed' else ClaimItem.objects.all()
        return render(request, 'items-ad.html', {'items': items, 'status': status})
    else:
        items = Item.objects.all()
        return render(request, 'items-ad.html', {'items': items, 'all': 'All '})


def users(request):
    Users_list = User.objects.all()
    return render(request, 'user-ad.html', {'users': Users_list})


def send_claim_status_email(claim, claim_status):
    # Define status colors
    status_colors = {
        "approved": "green",
        "rejected": "red",
        "request": "orange"
    }

    # Render the HTML template
    html_message = render_to_string('email-status.html', {
        'user_name': claim.claimed_by.username,
        'item_name': claim.item.name,
        'claim_status': claim_status,
        'status_color': status_colors.get(claim_status, "black"),
        'finder': claim.item.reported_by,
        'claim_url': f'https://finduil.vercel.app/profile/'
    })

    plain_message = strip_tags(html_message)

    send_mail(
        subject=f"Your Lost & Found Claim - {claim_status}",
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[claim.claimed_by.email],
        html_message=html_message
    )
