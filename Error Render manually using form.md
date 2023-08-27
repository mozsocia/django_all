```py
class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description']
```


```py
    path('add/', views.blog_add, name='blog_add'),
```

```py
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_add.html', {'form': form})
```


```html
<h1>Add Blog</h1>

{% if form.errors %}
<ul class="errors">
    {% for field, field_errors in form.errors.items %}
    {% for error in field_errors %}
    <li>{{ field }}: {{ error }}</li>
    {% endfor %}
    {% endfor %}
</ul>
{% endif %}
<form method="post">
    {% csrf_token %}
    <label for="id_title">Title:</label><br>
    <input type="text" id="id_title" name="title" ><br><br>
    
    <label for="id_description">Description:</label><br>
    <textarea id="id_description" name="description" rows="4" cols="50" ></textarea><br><br>
    
    <button type="submit">Save</button>
</form>
<a href="{% url 'blog_list' %}">Back to Blog List</a>
```
