```py
def home(request):
    # Fetch the first product from the Product table
    try:
        info = Information.objects.get()
        # Do something with 'info'
    except Exception:
        # Handle the case where no matching record is found
        print("No Information record found.")
        info = None
    first_product = Product.objects.first()

    # Serialize the first product into JSON format
    serialized_data = serialize('json', [first_product])
    


    # Pass the serialized data to the template
    return render(request, 'site/index.html', {'data': serialized_data, 'info': info})
```

```js
// index.html
<script>
  var alldata = JSON.parse("{{data | escapejs}}");
  console.log(alldata[0].fields)
</script>
```
