"""
This module contains various decorators and mixins for authentication and permission handling, request method handling,
serialize and deserialize data, and API POST helper functions.
"""

# decorators.py
import json
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
import os

class DeleteOldImageFilesMixin:
    def delete(self, *args, **kwargs):
        # Delete old image file before deleting the instance
        for field in self._meta.fields:
            if isinstance(field, models.ImageField):
                file_field = getattr(self, field.name)
                if file_field:
                    # Delete old file
                    if os.path.isfile(file_field.path):
                        os.remove(file_field.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Delete old image file before saving the instance
        if self.pk:
            old_instance = self.__class__.objects.get(pk=self.pk)
            for field in self._meta.fields:
                if isinstance(field, models.ImageField):
                    old_file_field = getattr(old_instance, field.name)
                    new_file_field = getattr(self, field.name)
                    if old_file_field != new_file_field and old_file_field:
                        # Delete old file
                        if os.path.isfile(old_file_field.path):
                            os.remove(old_file_field.path)
        super().save(*args, **kwargs)

class DepthMixin:
    """
    A mixin that sets depth=1 for serialization (read operations)
    and depth=0 for deserialization (create/update operations).
    """
    def to_representation(self, instance):
        self.Meta.depth = 1
        return super().to_representation(instance)

    def to_internal_value(self, data):
        self.Meta.depth = 0
        return super().to_internal_value(data)

#  ============================= auth middleware =======================================
def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Replace 'login' with your login URL

        return view_func(request, *args, **kwargs)

    return wrapper


def guest_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'login' with your login URL

        return view_func(request, *args, **kwargs)

    return wrapper


def company_staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('panel_login')
        # Check if the user is a panel staff
        if not request.user.is_company_staff:
            # You can customize this redirect to a page indicating insufficient permissions
            return redirect('panel_login')

        return view_func(request, *args, **kwargs)

    return wrapper

def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('panel_login')
        # Check if the user is a panel staff
        if not request.user.is_superuser:
            # You can customize this redirect to a page indicating insufficient permissions
            return redirect('panel_login')

        return view_func(request, *args, **kwargs)

    return wrapper

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('panel_login')
        # Check if the user is a panel staff
        if not request.user.is_manager:
            # You can customize this redirect to a page indicating insufficient permissions
            return redirect('panel_login')

        return view_func(request, *args, **kwargs)

    return wrapper

def assitant_manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('panel_login')
        # Check if the user is a panel staff
        if not request.user.is_assitant_manager:
            # You can customize this redirect to a page indicating insufficient permissions
            return redirect('panel_login')

        return view_func(request, *args, **kwargs)

    return wrapper

from functools import wraps
from django.http import HttpResponseForbidden

def user_roles_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            if not any(getattr(user, role, False) for role in roles):
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# ================================= request method middleware ====================================

def process_json_data(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                request_data = json.loads(request.body.decode('utf-8'))
                request.json_data = request_data
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'errors': 'Invalid JSON data'}, status=400)

        return view_func(request, *args, **kwargs)
    
    return wrapper

def allow_only_GET(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'], content="<html><body><h1>Method Not Allowed</h1><p>This endpoint only allows GET requests.</p></body></html>")
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def allow_only_POST(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'], content="<html><body><h1>Method Not Allowed</h1><p>This endpoint only allows POST requests.</p></body></html>")
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def allow_only_content_JSON(view_func):
    def _wrapped_view(request, *args, **kwargs):

        if not request.content_type == 'application/json':
            return HttpResponseNotAllowed(['application/json'] ,content="<html><body><h1>Not Allowed</h1><p>This endpoint only allows JSON POST requests.</p></body></html>")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


## **************************************  mixins.py ******************************************************

from django import forms

class CustomFieldMixin(forms.ModelForm):
    img_class = 'img-class'
    choice_class = 'choice-class'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ImageField):
                field.widget.attrs.update({'class': self.img_class})
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs.update({'class': self.choice_class})


# sample use in the form

# class YourForm(CustomFieldMixin, forms.ModelForm):
#     img_class = 'custom-img-class'
#     choice_class = 'custom-choice-class'

#     class Meta:
#         model = YourModel
#         fields = '__all__'

class JsonErrorsMixin:
    def get_errors(self):
        errors_dict = {field: self.errors[field][0] for field in self.errors}
        return {
            'data': errors_dict,
            'has_errors': bool(errors_dict)
        }



## *********************** serilizer helpers ***********************

from django.db.models import Model
import json
from django.http import JsonResponse
from django.db.models.fields.files import FieldFile
from django.db.models.fields.related import ManyToManyField, ForeignKey, OneToOneField


def serialize_single_data(instance, include_reverse_relations=True, current_depth=0, max_depth=6):
    if not isinstance(instance, Model):
        raise ValueError("The instance must be a Django model instance.")
    
    if current_depth >= max_depth:
        return str(instance)
    
    data = {}
    opts = instance._meta
    
    for field in opts.get_fields():
        if field.is_relation:
            if isinstance(field, ManyToManyField):
                related_data = getattr(instance, field.name)
                data[field.name] = [serialize_single_data(obj, include_reverse_relations=False, 
                                                          current_depth=current_depth+1, max_depth=max_depth) 
                                    for obj in related_data.all()[:10]]  # Limit to first 10 related objects
            elif isinstance(field, (ForeignKey, OneToOneField)):
                related_instance = getattr(instance, field.name)
                if related_instance:
                    data[field.name] = serialize_single_data(related_instance, include_reverse_relations=False, 
                                                             current_depth=current_depth+1, max_depth=max_depth)
                else:
                    data[field.name] = None
        else:
            value = getattr(instance, field.name)
            if isinstance(value, FieldFile):
                data[field.name] = value.url if value else None
            else:
                data[field.name] = value
    
    if include_reverse_relations and current_depth < max_depth - 1:
        for relation in opts.related_objects:
            reverse_field_name = relation.get_accessor_name()
            if hasattr(instance, reverse_field_name):
                related_queryset = getattr(instance, reverse_field_name)
                if relation.one_to_one:
                    try:
                        related_instance = related_queryset.get()
                        data[reverse_field_name] = serialize_single_data(related_instance, include_reverse_relations=False, 
                                                                         current_depth=current_depth+1, max_depth=max_depth)
                    except relation.related_model.DoesNotExist:
                        data[reverse_field_name] = None
                else:
                    data[reverse_field_name] = [
                        serialize_single_data(related_instance, include_reverse_relations=False, 
                                              current_depth=current_depth+1, max_depth=max_depth)
                        for related_instance in related_queryset.all()[:10]  # Limit to first 10 reverse related objects
                    ]
    
    return data

def serialize_list_data(queryset, include_reverse_relations=True, max_depth=6):
    if not hasattr(queryset, '__iter__'):
        raise ValueError("The input must be an iterable (e.g., a queryset or list of model instances).")
    
    serialized_data = []
    for instance in queryset[:100]:  # Limit to first 100 instances
        if not isinstance(instance, Model):
            raise ValueError("All items in the iterable must be Django model instances.")
        serialized_instance = serialize_single_data(instance, include_reverse_relations, 
                                                    current_depth=0, max_depth=max_depth)
        serialized_data.append(serialized_instance)
    
    return serialized_data


# def blog_list(request):
#     blogs = Blog.objects.all()
#     serialized_blogs = serialize_list_data(blogs, max_depth=3)
#     return JsonResponse(serialized_blogs, safe=False)

# def brand_list(request):
#     brands = Brand.objects.all()
#     serialized_brands = serialize_list_data(brands, max_depth=2)
#     return JsonResponse(serialized_brands, safe=False)

# def tag_list(request):
#     tags = Tag.objects.all()
#     serialized_tags = serialize_list_data(tags, max_depth=4)
#     return JsonResponse(serialized_tags, safe=False)

# def blog_detail(request, pk):
#     blog = Blog.objects.get(id=pk)
#     serialized_blog = serialize_single_data(blog, max_depth=3)
#     return JsonResponse(serialized_blog)

# def brand_detail(request, pk):
#     brand = Brand.objects.get(id=pk)
#     serialized_brand = serialize_single_data(brand, max_depth=2)
#     return JsonResponse(serialized_brand)

# def tag_detail(request, pk):
#     tag = Tag.objects.get(id=pk)
#     serialized_tag = serialize_single_data(tag, max_depth=4)
#     return JsonResponse(serialized_tag)



## *********************** API POST  helpers ***********************


from ..forms import *
from ..models import *
from apps.helpers import *
from django.http import JsonResponse
from django.db import transaction
import json
from pprint import pprint
from decimal import Decimal
from apps.customers.models import *
from apps.main.models import *


from django import forms
import json

class MultipleFormsHandler:
    def __init__(self, form_class, data_list):
        self.forms = [form_class(item) for item in json.loads(data_list)]

    def __iter__(self):
        return iter(self.forms)

    def __getitem__(self, index):
        return self.forms[index]

    def is_multiple_valid(self):
        return all(form.is_valid() for form in self.forms)

    def get_errors_multiple(self):
        return [form.errors for form in self.forms if not form.is_valid()]

    def save(self, commit=True):
        return [form.save(commit=commit) for form in self.forms if form.is_valid()]

class RestApiModelForm(forms.ModelForm):
    @classmethod
    def create_multiple(cls, data_list):
        return MultipleFormsHandler(cls, data_list)

    def get_errors(self):
        return {field: self.errors[field][0] for field in self.errors}

"""
class OrderForm(RestApiModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['is_reseller', 'user', 'total_payment', 'discount', 'items_total', 'subtotal', 'total_points', 'referral_commision_amount', 'special_discount', 'used_amount_from_user']

class OrderItemForm(RestApiModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['user', 'order']

@allow_only_POST
def api_order_store_checkout(request):
    if request.user.is_authenticated:
        order_user = request.user
    else:
        order_user = None

    order_form = OrderForm(request.POST)
    order_item_data = request.POST.get('order_items', '[]')
    order_item_forms = OrderItemForm.create_multiple(order_item_data)

    if order_form.is_valid() and order_item_forms.is_multiple_valid():

        ## -------------- Database write start-------------
        try:
           
            with transaction.atomic():
              #  process data with model

                
                    
        except Exception as e:
            print("order  api post",e)
            return JsonResponse({'success': False, 'errors': str(e)}, status=400)
        ## -------------- Database write End-------------

        return JsonResponse({'success': True, 'message': 'Order Created Successfully ', 'id':order.id }, status=201)
    else:
        errors = {
            'form_errors': order_form.get_errors(),
            'other_errors': order_item_forms.get_errors_multiple()
        }

        return JsonResponse({'success': False, 'errors': errors}, status=400)
    """

