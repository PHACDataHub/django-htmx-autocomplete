from autocomplete import HTMXAutoComplete

from .models import Person

data = [
    {"value": "1", "label": "Newsome Instruments Ltd"},
    {"value": "2", "label": "Dixon Refrigeration Ltd"},
    {"value": "3", "label": "Quirke Skips Ltd"},
    {"value": "4", "label": "Talisman Costume Hire Ltd"},
    {"value": "5", "label": "Hallworth Carpenters Ltd"},
    {"value": "6", "label": "Peel Building Materials Ltd"},
    {"value": "7", "label": "Ainsley Meat Wholesalers Ltd"},
    {"value": "8", "label": "Earl Recreational Vehicles Ltd"},
    {"value": "9", "label": "Crocket Footwear Ltd"},
    {"value": "10", "label": "Ashton Plant Hire Ltd"},
    {"value": "11", "label": "Valley Home Services Ltd"},
    {"value": "12", "label": "Keaton Engineering Ltd"},
    {"value": "13", "label": "Edwards Developments Ltd"},
    {"value": "14", "label": "Leary Car Repairs Ltd"},
    {"value": "15", "label": "Yeoman Fitness Products Ltd"},
    {"value": "16", "label": "Crocket Office Furniture Ltd"},
    {"value": "17", "label": "Walcott Beauty Treatments Ltd"},
    {"value": "18", "label": "Malloney Tractors Ltd"},
    {"value": "19", "label": "Sterling Fruit Importers Ltd"},
    {"value": "20", "label": "Tattershall Car Repairs Ltd"},
    {"value": "21", "label": "Lyons Reproductions Ltd"},
    {"value": "22", "label": "Elgar Freight Ltd"},
    {"value": "23", "label": "West Point Luxury Cars Ltd"},
    {"value": "24", "label": "Summit Printing Ltd"},
    {"value": "25", "label": "Alexander Lab Equipment Ltd"},
    {"value": "26", "label": "Goodacre Camping Supplies Ltd"},
    {"value": "27", "label": "Hunt Footwear Ltd"},
    {"value": "28", "label": "Eckard Printing Ltd"},
    {"value": "29", "label": "Fisher Design Ltd"},
    {"value": "30", "label": "Grady,Fine Accountancy Services Ltd"},
    {"value": "31", "label": "Reeve Locksmiths Ltd"},
    {"value": "32", "label": "Eagle Skips Ltd"},
    {"value": "33", "label": "Adkinson Demolition Ltd"},
    {"value": "34", "label": "Pendrick Skips Ltd"},
    {"value": "35", "label": "Jarvis Agency Ltd"},
    {"value": "36", "label": "East View Automations Ltd"},
    {"value": "37", "label": "Mack Fabrics Ltd"},
    {"value": "38", "label": "Bainbridge Construction Ltd"},
    {"value": "39", "label": "North Side Camping Supplies Ltd"},
    {"value": "40", "label": "Gatley Furniture Ltd"},
    {"value": "41", "label": "Addler Disposal Ltd"},
    {"value": "42", "label": "Cromwell Cleaners Ltd"},
    {"value": "43", "label": "Craft Building Materials Ltd"},
    {"value": "44", "label": "Knowles Showrooms Ltd"},
    {"value": "45", "label": "Allen Luxury Cars Ltd"},
    {"value": "46", "label": "Thistlemoor Builders Ltd"},
    {"value": "47", "label": "Valley Kitchens Ltd"},
    {"value": "48", "label": "Dobson Cosmetics Ltd"},
    {"value": "49", "label": "West View Hire Cars Ltd"},
    {"value": "50", "label": "Bentley Meat Wholesalers Ltd"},
]


class GetItemsAutoComplete(HTMXAutoComplete):
    name = "getitems"
    minimum_search_length = 0

    def get_items(self, search=None, values=None, request=None):
        if values:
            return list(filter(lambda x: x.get("value") in values, data))

        if search:
            return list(filter(lambda x: x.get("label").startswith(search), data))

        if search == "":
            return list(data)

        return []


class ModelAutoComplete(HTMXAutoComplete):
    name = "model"
    minimum_search_length = 0

    class Meta:
        model = Person


class GetItemsMultiAutoComplete(HTMXAutoComplete):
    name = "getitems_multi"
    multiselect = True
    minimum_search_length = 0

    def get_items(self, search=None, values=None, request=None):
        if values:
            return list(filter(lambda x: x.get("value") in values, data))

        if search:
            return list(filter(lambda x: x.get("label").startswith(search), data))

        if search == "":
            return list(data)

        return []


class ModelMultiAutoComplete(HTMXAutoComplete):
    name = "model_multi"
    multiselect = True
    minimum_search_length = 0

    class Meta:
        model = Person
