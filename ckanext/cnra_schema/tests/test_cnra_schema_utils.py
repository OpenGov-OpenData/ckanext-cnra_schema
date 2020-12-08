import ckanext.cnra_schema.cnra_schema_utils as cnra_schema_utils
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal, assert_false


class TestCnraSchemaUtils(object):

    assert_dict_equal.__self__.maxDiff = None

    def test_convert_list_to_string_success_single_item_list(self):
        list_to_convert = ['test']
        converted_str = cnra_schema_utils.convert_list_to_string(list_to_convert)

        assert_equal(converted_str, 'test')

    def test_convert_list_to_string_success_multi_item_list_no_delimiter(self):
        list_to_convert = ['test1', 'test2']
        converted_str = cnra_schema_utils.convert_list_to_string(list_to_convert)

        assert_equal(converted_str, 'test1 test2')

    def test_convert_list_to_string_success_multi_item_list_no_delimiter(self):
        list_to_convert = ['test1', 'test2']
        converted_str = cnra_schema_utils.convert_list_to_string(list_to_convert, ', ')

        assert_equal(converted_str, 'test1, test2')

    def test_convert_list_to_string_failure_string(self):
        list_to_convert = 'test1'
        converted_str = cnra_schema_utils.convert_list_to_string(list_to_convert)

        assert_equal(converted_str, 'test1')