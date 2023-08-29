# manual form rendering with error

```py
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

```py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs['class'] = 'text-input-class'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'textarea-class'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'select-class'
                
            # Check for errors and add a special class to fields with errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' error-class'

    class Meta:
        model = Post
        fields = ('title', 'content')

```
```py
from django.shortcuts import render, redirect
from .forms import PostForm

urlpatterns = [
    path('create/', create_post, name='create_post'),
]
```

```py
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_post')  # Redirect to a view displaying all posts
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


from django.shortcuts import get_object_or_404

def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)  # Redirect to the post detail view
    else:
        form = PostForm(instance=post)
    
    return render(request, 'update_post.html', {'form': form})

```

====================== error showing -->
```html
    {% if form.errors %}
    <ul class="errors">
        {% for field, field_errors in form.errors.items %}
        {% for error in field_errors %}
        <li>{{ field }}: {{ error }}</li>
        {% endfor %}
        {% endfor %}
    </ul>
    {% endif %}
```

### create_post.html -->
```html

======================== bootstrap 5 =======================

<form method="post">
    {% csrf_token %}

    <div class="mb-3">
        <label class="form-label">Full Name</label>
        <input type="text" name="{{ form.full_name.html_name }}" class="form-control "/>
    </div>


    <div class="mb-3">
        <label class="form-label">{{ form.full_name.label }}</label>
        <input type="text" name="{{ form.full_name.html_name }}" class="form-control "/>
    </div>


    <div class="mb-3">
        <label class="form-label">User</label>
        <select class="form-select"  name="{{ form.user.name }}" required>
            {% for user_choice in form.user.field.choices %}
                <option value="{{ user_choice.0 }}" >{{ user_choice.1 }}</option>
            {% endfor %}
        </select>
    </div>


    <div class="mb-3 {% if form.title.errors %} has-error {% endif %}">
        <label for="{{ form.title.id_for_label }}" class="form-label">{{ form.title.label }}</label>
        <input type="text" name="{{ form.title.html_name }}" class="form-control " id="{{ form.title.id_for_label }}" />
      
        {% if form.title.errors %}
        <div class="invalid-feedback custom-error-class">
            {% for error in form.title.errors %}
            <span>{{ error }}</span>
            {% endfor %}
        </div>
        {% endif %}
      
    </div>

    <button type="submit" class="btn btn-primary">Create</button>
</form>


==============================  bootstrap 4 =======================

<form method="post">
    {% csrf_token %}

  <div class="form-group ">
        <label >Full Name</label>
        <input type="text" name="{{ form.full_name.html_name }}" class="form-control"/>  
  </div>

  <div class="form-group ">
        <label >{{ form.full_name.label }}</label>
        <input type="text" name="{{ form.full_name.html_name }}" class="form-control"/>  
  </div>



    <div class="form-group {% if form.title.errors %}has-error{% endif %}">
        <label for="{{ form.title.id_for_label }}" >{{ form.title.label }}</label>
        <input type="text" name="{{ form.title.html_name }}" class="form-control {% if form.title.errors %}is-invalid{% endif %}" id="{{ form.title.id_for_label }}" />
      
        {% if form.title.errors %}
        <div class="invalid-feedback ">
            {% for error in form.title.errors %}
            <span>{{ error }}</span>
            {% endfor %}
        </div>
        {% endif %}
      
    </div>

 

    <button type="submit" class="btn btn-primary">Create</button>
</form>


```

### update_post.html --> 

```html
=========================== bootstrap 5 ========================

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}

        <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" name="{{ form.full_name.name }}" value="{{ form.full_name.value }}" class="form-control">
        </div>

        <div class="mb-3">
            <label class="form-label">{{ form.full_name.label }}</label>
            <input type="text" name="{{ form.full_name.name }}" value="{{ form.full_name.value }}" class="form-control">
        </div>


        <div class="mb-3">
            <label class="form-label">User</label>
            <select class="form-select"  name="{{ form.user.name }}" required>
                {% for user_choice in form.user.field.choices %}
                    <option value="{{ user_choice.0 }}" {% if user_choice.0 == form.user.value %}selected{% endif %}>{{ user_choice.1 }}</option>
                {% endfor %}
            </select>
        </div>



    
        <div class="mb-3">
            <label for="{{ form.full_name.id_for_label }}" class="form-label">Full Name</label>
            <input type="text" name="{{ form.full_name.name }}" value="{{ form.full_name.value }}" class="form-control">
            {% if form.full_name.errors %}
                <div class="invalid-feedback">
                    {% for error in form.full_name.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    
    <!-- Repeat the above block for other fields -->
    
    <button type="submit" class="btn btn-primary">Update Payment</button>
</form>    

========================  bootstrap 4 ======

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    
        <div class="form-group">
            <label for="{{ form.full_name.id_for_label }}" >Full Name</label>
            <input type="text" name="{{ form.full_name.name }}" value="{{ form.full_name.value }}" class="form-control">
            {% if form.full_name.errors %}
                <div class="invalid-feedback">
                    {% for error in form.full_name.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    
    <!-- Repeat the above block for other fields -->
    
    <button type="submit" class="btn btn-primary">Update Payment</button>
</form>

```


================================================
===============================================
===============================================

## full form
```html

<form method="post">
    {% csrf_token %}

    {% for field in form %}
        {% if field.is_hidden %}
            {{ field }}
        {% else %}
            <div class="form-group {% if field.errors %}has-error{% endif %}">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                    <div class="custom-error-class">
                        {% for error in field.errors %}
                            <span>{{ error }}</span>
                        {% endfor %}
                    </div>
                {% endif %}
                {% if field.help_text %}
                    <span class="helper-text">{{ field.help_text }}</span>
                {% endif %}
            </div>
        {% endif %}
    {% endfor %}

    {% if form.non_field_errors %}
        <div class="custom-error-class">
            {% for error in form.non_field_errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% endif %}

    {% for hidden_field in form.hidden_fields %}
        {{ hidden_field }}
    {% endfor %}

    <button type="submit">Create</button>
</form>
```
