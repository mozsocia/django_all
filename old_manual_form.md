```html

<form method="post" novalidate>
    {% csrf_token %}

    {{ form.non_field_errors }}

    {% for hidden_field in form.hidden_fields %}
    {{ hidden_field.errors }}
    {{ hidden_field }}
    {% endfor %}

    <table border="1">
        {% for field in form.visible_fields %}
        <tr>
            <th>{{ field.label_tag }}</th>
            <td>
                {{ field.errors }}
                {{ field }}
                {{ field.help_text }}
            </td>
        </tr>
        {% endfor %}
    </table>



    <button type="submit">Submit</button>
</form>



<form method="post" novalidate>

    {% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
    {% endfor %}


    <button type="submit">Submit</button>
</form>
```

```html

<form method="post" novalidate>
    {% csrf_token %}

    {{ form.non_field_errors }}

    {% for hidden_field in form.hidden_fields %}
    {{ hidden_field.errors }}
    {{ hidden_field }}
    {% endfor %}

    <table border="1">
        {% for field in form.visible_fields %}
        <tr>
            <th>{{ field.label_tag }}</th>
            <td>
                {{ field.errors }}
                {{ field }}
                {{ field.help_text }}
            </td>
        </tr>
        {% endfor %}
    </table>



    <button type="submit">Submit</button>
</form>



<form method="post" novalidate>

    {% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
    {% endfor %}


    <button type="submit">Submit</button>
</form>
````
