```html
{% if form.errors %}

<div class="alert alert-danger session-alert">
  Whoops! Something went wrong.
</div>


<div class="session-alert  alert alert-danger alert-details">
  <div >
    <ul class="p-1 text-danger">

      {% for field, field_errors in form.errors.items %}
      {% for error in field_errors %}
      <li >{{ field }}: {{ error }}</li>
      {% endfor %}
      {% endfor %}

    </ul>
  </div>
</div>

{% endif %}
```

```css
<style>
  .session-alert {
    display: none;
    position: fixed;
    top: 10px;
    right: 20px;
    z-index: 9999;
    opacity: .9;
  }
  .alert-details {
    top: 70px;
    padding: 10px;
    padding-left: 30px;
  }
</style>
```

```js
<script>
      // Get all elements with the session-alert class
      const sessionAlerts = document.querySelectorAll('.session-alert');

      // Loop through all session alert elements
      sessionAlerts.forEach(sessionAlert => {

        sessionAlert.style.display = 'inline';

        // Add a transition effect to the alert
        sessionAlert.style.transition = 'transform 0.7s ease';

        // Slide the alert in from the right
        sessionAlert.style.transform = 'translateX(170%)';

        // Wait for 100ms to allow the slide-in effect to take place
        setTimeout(() => {
          // Slide the alert back to its original position
          sessionAlert.style.transform = 'translateX(0)';
        }, 100);

        // Wait for 5 seconds before sliding the alert out
        setTimeout(() => {
          // Slide the alert out to the right
          sessionAlert.style.transform = 'translateX(170%)';

          // Wait for 500ms to allow the slide-out effect to take place
          setTimeout(() => {
            // Remove the alert from the DOM
            sessionAlert.remove();
          }, 500);
        }, 5000);
      });
</script>

````
