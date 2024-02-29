Certainly! To achieve this, you can create a Django ModelForm for your Blog model and then handle the form validation and response in your Django view. Here's a basic example:

Assuming your Blog model looks like this:

```python
# models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    email = models.EmailField()
```

```py
# mixins.py
class JsonErrorsMixin:
    def json_errors(self):
        return {field: self.errors[field][0] for field in self.errors}


```

You can create a corresponding ModelForm in your forms.py:

```python
# forms.py
from django import forms
from .models import *
from .mixins import JsonErrorsMixin

class BlogForm(JsonErrorsMixin,forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

```

Now, in your views.py, you can handle the form submission and return JSON responses for success or failure:
```py
# decorators.py
import json
from django.http import JsonResponse

def process_json_data(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                # Attempt to decode JSON data
                request_data = json.loads(request.body.decode('utf-8'))
                request.json_data = request_data
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'errors': 'Invalid JSON data'}, status=400)

        return view_func(request, *args, **kwargs)

    return wrapper

```
```py
# urls.py
from django.urls import path
from .views import *

urlpatterns = [

    path('blogs/', blog_index, name='blog_index'),
    path('blogs/create/', post_blog, name='blog_create'),
]
```

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import BlogForm
from .decorators import process_json_data
from pprint import pprint

@require_GET
def blog_index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs})


@require_POST
@process_json_data
def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.json_data)
        if form.is_valid():
            blog = form.save()
            return JsonResponse({'success': True, 'id': blog.id}, status=201)
        else:
            return JsonResponse({'success': False, 'errors': form.json_errors()}, status=400) 

    return JsonResponse({'success': False, 'errors': 'Invalid request method'}, status=405)  
```

Make sure to include the appropriate URL patterns in your `urls.py` to route the API request to this view.

Now, when you use fetch API to send data to your Django backend, you can check the JSON response for success or error messages.

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog Form</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

  <style>
    .alert-box {
      border-radius: 0.35rem !important;
      margin-bottom: 0.5rem !important;
    }

    #alert-container {
      z-index: 99;
      top: 2%;
    }

    .error {
      display: block;
    }
  </style>

</head>

<body>
  <div id="alert-container" class="position-fixed end-0 p-3"></div>

  <div class="container">

    <form id="blogForm">

      <div class="mb-2">
        <label for="title" class="form-label">Title:</label>
        <input type="text" id="title" name="title" class="form-control">
      </div>

      <div class="mb-2">
        <label for="details" class="form-label">Details:</label>
        <textarea id="details" name="details" class="form-control"></textarea>
      </div>

      <div class="mb-2">
        <label for="email" class="form-label">Email:</label>
        <input type="text" id="email" name="email" class="form-control">
      </div>

      <br>

      <button type="button" onclick="submitForm()" class="btn btn-primary">Submit</button>
    </form>

  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
    crossorigin="anonymous"></script>

  <script>

    function showAlert(message, alertType = 'success') {
      const alertContainer = document.getElementById('alert-container');

      // Create Bootstrap alert element
      const alertElement = document.createElement('div');
      alertElement.classList.add('alert', `alert-${alertType}`, 'fade', 'show', 'py-3', 'px-4', 'alert-box');
      alertElement.role = 'alert';
      alertElement.innerHTML = `
  <strong>${message}</strong>
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

      // Append alert to container
      alertContainer.appendChild(alertElement);

      // Remove the alert after a few seconds (optional)
      setTimeout(() => {
        alertElement.remove();
      }, 5000); // Remove after 5 seconds
    }

    function clearErrors() {
      const errorParagraphs = document.querySelectorAll('.error');
      errorParagraphs.forEach(paragraph => paragraph.remove());
    }

    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }


    function submitForm() {
      // Clear previous errors
      clearErrors();

      const form = document.getElementById('blogForm');
      const formData = new FormData(form);

      // Get authentication cookie
      const csrftoken = getCookie('csrftoken');
      const sessionid = getCookie('sessionid');

      fetch('/blogs/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Cookie': `csrftoken=${csrftoken}; sessionid=${sessionid}`
        },
        body: JSON.stringify(Object.fromEntries(formData))
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showAlert('Blog submitted successfully! Blog ID: ' + data.id, 'success');
          } else {
            // Display errors and create <p> tags dynamically
            Object.keys(data.errors).forEach(fieldName => {
              const input = form.querySelector(`[name="${fieldName}"]`);
              const errorParagraph = document.createElement('div');
              errorParagraph.textContent = data.errors[fieldName];
              errorParagraph.classList.add('error', 'invalid-feedback');
              input.insertAdjacentElement('afterend', errorParagraph);
            });

            showAlert('Failed to submit blog. See errors next to the fields.', 'danger');
          }
        })
        .catch(error => console.error('Error:', error));
    }


  </script>

</body>

</html>

```

----
-----

### How to do usually post form content-type:multipart/form-data


Yes, you can use `FormData` directly in the `fetch` call instead of converting it to JSON using `JSON.stringify(Object.fromEntries(formData))`. When sending data using `FormData`, the `Content-Type` header should be set to `'multipart/form-data'`, and you don't need to manually convert it to JSON.

Here's the modified `fetch` call:

```javascript
fetch('/blogs/create/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': csrftoken,
    'Cookie': `csrftoken=${csrftoken}; sessionid=${sessionid}`
  },
  body: formData  // Use FormData directly
})
```

This way, you're sending the form data in its native format without converting it to JSON. The server should be able to handle the form data appropriately. Remember to adjust your server-side code to handle form data instead of JSON if needed.

in view
```py
def post_blog(request):
    pprint(request.POST)
```
