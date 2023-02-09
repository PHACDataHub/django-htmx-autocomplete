# django-htmx-autocomplete

This Django app provides a client-side autocomplete component powered by
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
    from autocomplete import HTMXAutoComplete

    urlpatterns = [
        ...
        *HTMXAutoComplete.url_dispatcher('ac'),
    ]
    ```

    This will add routes prefixed by `ac` to support component instances.

1. Use either the widget or class to create components!

    ```python
    from django forms
    from django.db import models
    from autocomplete import HTMXAutoComplete, widgets 
    
    # Example models
    class Person(models.Model):
        name = models.CharField(max_length=60)

    class Team(models.Model):
        name = models.CharField(max_length=60)
        members = models.ManyToManyField(Person)

    # Using the widget
    class MultipleFormModel(forms.ModelForm):
    """Multiple select example form using a model"""
        class Meta:
            """Meta class that configures the form"""
            model = Team
            fields = ['name', 'members']
            widgets = {
                'members': widgets.Autocomplete(
                    name='members',
                    options=dict(multiselect=True, model=Person)
                )
            }

    # Using the class
    class GetItemsMultiAutoComplete(HTMXAutoComplete):
        name = "members"
        multiselect = True

        class Meta:
            model = Person

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

## Customization

### Strings

The strings listed in the table below can be overriden by creating the appropriate 
template in your own project, matching the `autocomplete/strings/{name}.html` pattern.
By default all strings are available in both French and English.  

| Name              | Description                                                                                                                 | Default English                                                    | Default French                                                      |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| no_results        | Text displayed when no results are found.                                                                                   | No results found.                                                  | Aucun résultat trouvé.                                              |
| more_results      | When `max_results` is set, text displayed when there are additional results available.                                      | Displaying maximum {{ count }} out of {{ total_results }} results. | Affichage maximum de {{ count }} résultats sur {{ total_results }}. |
| available_results | Text anounced to sceen readers when results are available.  If max_results is set, the more_results text is spoken instead. | {{ count }} results available.                                     | {{ count }} résultats disponibles.                                  |
| nothing_selected  | Text anounced to screen readers when there are no selections.                                                               | Nothing selected.                                                  | Rien de sélectionné.                                                |

Individual instances can override strings by providing a dictionary of `custom_strings`.

```python
    class GetItemsMultiAutoComplete(HTMXAutoComplete):
        name = "members"
        multiselect = True
        custom_strings = {
            "no_results": "no results text",
            "more_results": _("More results text")
        }        

        class Meta:
            model = Person


```
