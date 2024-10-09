# django-htmx-autocomplete

This Django app provides an autocomplete widiget component powered by
[htmx](https://htmx.org/) featuring multiselect, search and is completely extensible.

## Quick start

1. Add "autocomplete" to your `INSTALLED_APPS` setting like this:

   ```python
   # settings.py
   INSTALLED_APPS = [
       ...
       'django.contrib.staticfiles',  # also required
       'autocomplete',
   ]
   ```

1. Include the autocomplete urls like this:

   ```python
   # urls.py
   ...
    from autocomplete import urls as autocomplete_urls

   urlpatterns = [
       # ...
        path("ac/", autocomplete_urls),
   ]
   ```

1. Create an autocomplete class that extends `autocomplete.ModelAutocomplete`,

   ```python
   from django forms
   from django.db import models
   from autocomplete import Autocomplete, AutocompleteWidget

   class Person(models.Model):
       name = models.CharField(max_length=60)

   class Team(models.Model):
        team_lead = models.ForeignKey(
            Person, null=True, on_delete=models.SET_NULL, related_name="lead_teams"
        )

       members = models.ManyToManyField(Person)

   class PersonAutocomplete(ModelAutocomplete):
       model = Person
       search_attrs = [ 'name' ]


   class MultipleFormModel(forms.ModelForm):
   """Multiple select example form using a model"""
       class Meta:
           """Meta class that configures the form"""
           model = Team
           fields = ['team_lead', 'members']
           widgets = {
                'team_lead': AutocompleteWidget(
                    ac_class=PersonAutocomplete,
                ),
               'members': AutocompleteWidget(
                    ac_class=PersonAutocomplete,
                    options={"multiselect": True},
               )
           }
   ```

1. Make sure your templates include HTMX.

   > **Note**
   > Bootstrap is included in this example styling, however it is not required.

   ```django
   {% load autocomplete %}
   {% load static %}
   <!doctype html>
   <html lang="en">
     <head>
       <!-- Bootstrap -->
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet"
   integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
     </head>
     <body>
       <h1>Example base html template</h1>
       <!-- Bootstrap -->
       <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
       <!-- htmx -->
       <script src="https://unpkg.com/htmx.org@1.8.3" integrity="sha384-e2no7T1BxIs3ngCTptBu4TjvRWF4bBjFW0pt7TpxOEkRJuvrjRt29znnYuoLTz9S" crossorigin="anonymous"></script>
       <!-- htmx csrf -->
       <script>
         document.body.addEventListener('htmx:configRequest', (event) => {
           event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
         });
       </script>
     </body>
   </html>
   ```

## Using the widget

- The widget will receive its name, required-ness and disabled-ness from the form field, these work out of the box, including for formsets and prefixed forms.
- Options that can be tweaked on the fly via widget `options` are,
  - multiselect
    - If you want to use the widget in on a multiple-choice field (e.g. a many-to-many field), you can pass an options dict with `multiselect=True` in it
  - placeholder
    - default: ""
  - component_prefix
    - this is for a niche use-case where you want multiple inputs with the same `name` attribute. In that case and you don't set unique prefixes, the autocomplete widget may not work correctly due to duplicate HTML IDs.

Other options are set less dynamically, by customizing the the autocomplete class...

## Autocomplete class customization

### `minimum_search_length`

default: 3

example:

```python
class MyAC(Autocomplete):
    minimum_search_length = 2
```

### `max_results`

This library does not yet support pagination, but it will efficiently limit results and tell the user there how many results are missing.

```python
class MyAC(Autocomplete):
    max_results = 10

```

### `component_prefix`

- In addition to widget options, you can also set the `component_prefix` option on the class itself. Widget options will take precedence over the class.
- default: ""

### `placeholder`

- In addition to widget options, you can also set the `placeholder` option on the class itself. Widget options will take precedence over the class.
- default: ""

### Translation strings

You can customize the translation strings used in the autocomplete widget by overriding class variables on your autocomplete class,

- `no_result_text`
  - default: "No results found."
- `narrow_search_text`
  - default: "Showing %(page_size)s of %(total)s items. Narrow your search for more results."
- `type_at_least_n_characters`
  - default: "Type at least %(n)s characters"

note that the `%(n)s` and `%(page_size)s` and `%(total)s` are placeholders that will be replaced with the actual values at runtime. If you write your own strings, make sure to use the `%(n)s` rather than `%(n)d`. Variables are converted to strings so the integer formatter will not work.

example:

```python
class MyAC(Autocomplete):
    no_result_text = "No results found"
    narrow_search_text = "Please narrow your search"
    type_at_least_n_characters = "Type at least %(n)s characters"
```

### Authentication-aware behaviour

Autocomplete adds 2 new views that any user, including non-authenticated users, can access. Autocomplete classes have a `auth_check` method you can override to add authentication checks. For example, if you want to restrict access to a certain autocomplete to only authenticated users, you can do the following,

```python
class MyAC(Autocomplete):
    # ...

    @staticmethod
    def auth_check(request):
        if not request.user.is_authenticated:
            raise PermissionDenied("Must be logged in")

```

This is a common enough use case that we've added a setting shortcut. Add `AUTOCOMPLETE_BLOCK_UNAUTHENTICATED=False` in your settings and all autocomplete views will require authentication by default.

## Non model approach

The model autocomplete is a subclass of the more generic `autocomplete.Autocomplete` class. You can use this class to create an autocomplete that does not rely on a model. There are two important methods to provide,

1. `search_items(cls, search, context)`
   - Must return an iterable of `{ key: string, label: string }` dictionaries. This iterable must allow slicing and len() to be called on it.
2. `get_items_from_keys(cls, keys, context)`
   - Must return a list of `{ key: string, label: string }` dictionaries. This list must be the same length as the input keys list.
   - This is used to render existing items in the autocomplete widget.

The context argument is a simple namespace type:

```python
@dataclass
class ContextArg:
    request: HttpRequest
    client_kwargs: django.http.QueryDict
    # this is a redundant reference to request.GET
```

We may add additional attributes on this object in the future.

If you're still using models but want different logic than the model-autocomplete, consider cracking open the `ModelAutocomplete` class and seeing how it works. It's probably easier to override its particular methods than to start from scratch and implement an efficient iterable that wraps querysets.

## Tip: Custom Autocomplete base class

If you have several autocompletes in your project, we recommend creating a base autocomplete class that extends `autocomplete.Autocomplete` and using that as your project-wide base class. Here you can customize translation strings, authentication-aware behaviour, min-search-length, max-results-count, etc. This way, you're also insulated from changes in our defaults.

# Contributing

To set up the development environment, follow these steps:

```bash
# from root of project,
pip install -r requirements.txt

# running tests,
python manage.py test tests/

# running app locally
python manage.py migrate
python manage.py runscript sample_app.dev_script
python manage.py runserver
```
