import numpy as np
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from io import BytesIO

from .background_runer import perform_task
from .models import ItemImage, Item, Location, User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ItemForm, SignInForm
from .text_filter import search_items
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse

# Create your views here.
from django.conf import settings
import os
import zipfile
import io



def home(request):
    perform_task(8, priority=10)
    return render(request, 'index.html')


def signup_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(next_url) if next_url else redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signin_view(request):
    next_url = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(next_url) if next_url else redirect('home')
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url) if next_url else redirect('home')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


@login_required
def report_item(request, item_id=None):
    item = get_object_or_404(Item, id=item_id) if item_id else None

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item, user=request.user)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            saved_item = form.save()
            return redirect(f'/items/{saved_item.id}')

    else:
        form = ItemForm(instance=item, user=request.user)

    return render(request, 'report.html',  {'form': form})


@login_required
def claim_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'claim.html', {'item': item})


# def upload(request):
#     if request.method == 'POST' and request.FILES['image_file']:
#         # Get the uploaded image file
#         image_file = request.FILES['image_file']
#
#         # Read the image file into memory using BytesIO
#         img_data = image_file.read()
#         img_bytes_io = BytesIO(img_data)
#
#         # Use OpenCV's imdecode to read the image from byte stream
#         img_array = np.asarray(bytearray(img_bytes_io.read()), dtype=np.uint8)
#         img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Decode as color image
#         img = cv2.resize(img, (224, 224))
#
#         img = np.array(img)
#
#         filter_model = cache.get('filter_model')
#         data = filter_model.nearest_neighbors(img)
#         print(data)
#
#         # Return the shape of the NumPy array (image dimensions)
#         return render(request, 'filter.html', {'data': data})
#
#     return render(request, 'inde.html')


def new(request):
    if request.method == 'POST':
        data = request.POST
        location, created = Location.objects.get_or_create(name=data.get('location'))
        # category, created = Category.objects.get_or_create(name=data.get('category'))
        item = Item.objects.create(name=data.get('name'), location=location, description=data.get('description'),
                                   reported_by=User.objects.get(id=1))
        images = request.FILES.getlist('images')
        for image in images:
            ItemImage.objects.create(item=item, image=image)

    return render(request, 'new.html', )


def download_db_and_media(request):
    # Paths to the SQLite database and media folder
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')  # Adjust as per your setup
    media_path = settings.MEDIA_ROOT  # Path to the media folder

    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add SQLite database to the ZIP file
        if os.path.exists(db_path):
            zip_file.write(db_path, arcname='db.sqlite3')
        else:
            return HttpResponse("Database file not found.", status=404)

        # Add all files in the media folder to the ZIP file
        for root, dirs, files in os.walk(media_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, media_path)  # Preserve folder structure
                zip_file.write(file_path, arcname=arcname)

    zip_buffer.seek(0)

    # Serve the ZIP file as a downloadable response
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="backup.zip"'
    return response


def item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    # keywords = extract_object_keywords(item.description)
    # if item.status == 'lost':
    #     item.relatives.set(search_items(item))
    #     item.save()

    return render(request, 'item-details.html', {'item': item})


def cse_view(request):

    return JsonResponse({}, status=200)
