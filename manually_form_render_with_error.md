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
    class Meta:
        model = Post
        fields = ('title', 'content')


from django.shortcuts import render, redirect
from .forms import PostForm
```

```py
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


```

```html
  <form method="post">
            {% csrf_token %}
    
            <div class="form-group {% if form.title.errors %} has-error {% endif %}">
              
                <label for="{{ form.title.id_for_label }}">{{ form.title.label }}</label>
                <input type="text" name="{{ form.title.html_name }}" class="my-class" id="{{ form.title.id_for_label }}" />
              
                {% if form.title.errors %}
                <div class="custom-error-class">
                    {% for error in form.title.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% endif %}
              
            </div>
    
    
            <div class="form-group {% if form.content.errors %}has-error{% endif %}">
              
                <label for="{{ form.content.id_for_label }}">{{ form.content.label }}</label>
                <textarea name="{{ form.content.html_name }}" class="my-class" id="{{ form.content.id_for_label }}"></textarea>
              
                {% if form.content.errors %}
                <div class="custom-error-class">
                    {% for error in form.content.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% endif %}
              
            </div>
            <button type="submit">Create</button>
    </form>

```
