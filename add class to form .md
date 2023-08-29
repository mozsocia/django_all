
```py
# forms.py
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
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
        model = Blog
        fields = ['title', 'content', 'category']  # Assuming 'category' is a choice field
```
