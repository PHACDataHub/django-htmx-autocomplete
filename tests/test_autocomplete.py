"""
Autocomplete tests
"""
from autocomplete import HTMXAutoComplete


def test_classes_generate_routes():
    """Creating Autocomplete subclasses automatically generates routes"""
    class Test(HTMXAutoComplete): # pylint: disable=unused-variable
        """test case 1"""
        name = "test1"
        def get_items(self, search=None, values=None):
            return []
    class Test2(HTMXAutoComplete): # pylint: disable=unused-variable
        """test case 2"""
        name = "test"
        def get_items(self, search=None, values=None):
            return []

    urls = HTMXAutoComplete.url_dispatcher('test')
    assert len(urls) == 2
