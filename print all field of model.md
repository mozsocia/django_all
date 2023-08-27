```py
    blogone = Blog.objects.get(user=request.user)
    
    for field in Blog._meta.get_fields():
        if hasattr(blogone, field.name):
            field_value = getattr(blogone, field.name)
            print(f"{field.name}: {field_value}")
```
