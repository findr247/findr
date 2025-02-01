# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

import json
from .models import Location, Item, ItemImage, UserProfile
from .text_filter import search_items


class JsonField(forms.Field):
    def __init__(self, *args, **kwargs):
        # kwargs['widget'] = JsonWidget()  # Attach the custom widget

        super().__init__(*args, **kwargs)

    def clean(self, value):
        # Convert input to a list of tags
        if isinstance(value, str):
            value = value.split(',')
        if not isinstance(value, list):
            raise forms.ValidationError("Invalid input. Must be a list of strings.")
        return value


class JsonWidget(forms.TextInput):
    template_name = "widgets/choose__js.html"

    def __init__(self, attrs=None):
        default_attrs = {"class": "choices-js"}

        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if isinstance(value, list):
            return ", ".join(value)
        return value




class SignUpForm(forms.ModelForm):
    # User fields
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    fullname = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your fullname'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a Password'})
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your Password'})
    )

    # UserProfile fields
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'})
    )

    matric_no = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Matric Number'})
    )

    class Meta:
        model = User
        fields = ['username', 'fullname', 'email', 'password', 'phone_number', 'matric_no']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def clean_password(self):
        """
        Validate the password using Django's built-in password validation.
        """
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def clean_fullname(self):
        """
        Validate the password using Django's built-in password validation.
        """
        fullname = self.cleaned_data.get("fullname")
        if len(fullname.split(' ')) > 1:
            return fullname
        else:
            raise forms.ValidationError('enter your fullname')


    def save(self, commit=True):
        # Save User
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])
        fullname = self.cleaned_data['fullname'].split(' ')
        print()
        user.first_name = fullname.pop(0)
        user.last_name = ' '.join(fullname)

        if commit:
            user.save()
            # Save UserProfile
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number'),
                matric_no=self.cleaned_data.get('matric_no')
            )

        return user


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the widget attributes for username and password fields
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ItemForm(forms.ModelForm):
    # Fields for the Location model
    location = forms.CharField(
        max_length=255, label="Location Name",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter the location where the item was lost or found'})
    )

    # Field for multiple file uploads
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'd-none', 'id': 'hidden-file-input'})
    )
    email = forms.EmailField(
        label="Your Email", required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Your email address'}),
    )
    phone = forms.CharField(
        label="Your Phone", required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
    )

    questions = JsonField(
        widget=JsonWidget(attrs={'class': 'form-control', "placeholder": "Add question..."})
    )

    answers = JsonField(
        widget=JsonWidget(attrs={'class': 'form-control', "placeholder": "Add answer..."})
    )

    removed = forms.CharField(
        widget=forms.HiddenInput(attrs= {'id': 'to-remove', 'value': '[]'}),
        required=False
    )

    class Meta:
        model = Item
        fields = ['name', 'description', 'status', 'location', 'images', 'email', 'phone', 'questions', 'answers',
                  'removed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Provide details like size, color, and any unique features.'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'claimed_by': forms.Select(attrs={'class': 'form-select'}),
        }

    # Set initial value for status field
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [('', 'Select...')] + self.fields['status'].choices
        self.fields['status'].initial = ''
        self.fields['email'].initial = self.user.email
        self.fields['phone'].initial = self.user.profile.phone_number if self.user.profile else ''

    def save(self, commit=True):
        # Save Item and Location
        item = super().save(commit=False)

        # Handle location
        # location_name = self.cleaned_data.get('location_name')
        # location, _ = Location.objects.get_or_create(name=location_name)
        # item.location = location
        item.reported_by = self.user
        item.contact_phone = self.cleaned_data.get('phone')
        item.contact_email = self.cleaned_data.get('email')

        if commit:
            item.save()

            # Handle multiple images
            images = self.files.getlist('images')  # Retrieve the list of uploaded images
            remove = self.cleaned_data.get('removed')  # Retrieve the list of uploaded images
            print('to remove')
            for x in ItemImage.objects.filter(image__in=json.loads(remove)):
                x.delete()
            for image in images:
                ItemImage.objects.create(image=image, item=item)
            print(images, remove)
            # for image_file in images:
            #     ItemImage.objects.create(item=item, image=image_file)
            #
            # if item.status == 'lost':
            #     item.relatives.set(search_items(item))
            #     item.save()

        return item

