In Django, you can restrict access to certain URLs for guest users by using a middleware. Middleware in Django provides a way to process requests and responses globally before they reach the view functions.

Here's an example of how you can create a middleware to restrict login and signup URLs for guest users:

1. Create a new file called `middleware.py` in your Django project's directory (if it doesn't already exist).

2. In `middleware.py`, define a class called `RestrictGuestMiddleware`:

```python
from django.shortcuts import redirect
from django.urls import reverse

class RestrictGuestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            restricted_urls = [reverse('login'), reverse('signup')]  # Replace 'login' and 'signup' with your actual URL names
            if request.path in restricted_urls:
                return redirect('home')  # Replace 'home' with the URL where you want to redirect guest users
        return self.get_response(request)
```

3. Save the `middleware.py` file.

4. Open your project's `settings.py` file.

5. Locate the `MIDDLEWARE` setting and add the path to your middleware class at the beginning of the list:

```python
MIDDLEWARE = [
    'myproject.middleware.RestrictGuestMiddleware',
    # Other middleware classes...
]
```

Make sure to replace `'myproject.middleware.RestrictGuestMiddleware'` with the actual path to your `RestrictGuestMiddleware` class.

6. Save the `settings.py` file.

Now, whenever a guest user tries to access the login or signup URLs, they will be redirected to the specified URL (e.g., 'home'). You can modify the middleware class to suit your specific needs, such as adding more restricted URLs or changing the redirect URL.
