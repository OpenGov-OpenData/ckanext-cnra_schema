import ckanext.cnra_schema.cnra_schema_utils as cnra_schema_utils
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal, assert_false


class TestCnraSchemaUtils(object):

    assert_dict_equal.__self__.maxDiff = None

    def test_delete_from_extras_success(self):
        package_dict = {'extras': [{'value':'x', 'key':'progress'}]}
        key = 'progress'

        cnra_schema_utils.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), [])

    def test_delete_from_extras_only_removes_key(self):
        package_dict = {'extras': [{'value': 'x', 'key': 'progress'},{'value': 'y', 'key': 'new_key'}]}
        key = 'progress'

        cnra_schema_utils.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), [{'value': 'y', 'key': 'new_key'}])

    def test_delete_from_extras_failure(self):
        package_dict = {'extras': [{'value': 'x', 'key': 'progress'}]}
        key = 'backup_contact_email'

        cnra_schema_utils.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), [{'value': 'x', 'key': 'progress'}])

    def test_delete_from_extras_missing_extras_fields(self):
        package_dict = {}
        key = 'backup_contact_email'

        cnra_schema_utils.delete_existing_extra_from_package_dict(key, package_dict)

        assert_dict_equal(package_dict, {})

    def test_get_time_date_and_time_dict_success_timestamp(self):
        date_timestamp = ['2010-07-23T14:19:59Z']
        new_date_timestamp = cnra_schema_utils.get_date_and_time_dict(date_timestamp)

        assert_equal(new_date_timestamp, '{\"date\": \"2010-07-23\", \"time\": \"14:19:59\"}')

    def test_get_time_date_and_time_dict_success_only_date(self):
        date_timestamp = ['2010-07-23']
        new_date_timestamp = cnra_schema_utils.get_date_and_time_dict(date_timestamp)

        assert_equal(new_date_timestamp, '{\"date\": \"2010-07-23\", \"time\": \"\"}')

    def test_get_time_date_and_time_dict_success_year_less_than_1900_with_timestamp(self):
        date_timestamp = ['1850-07-23T14:19:59Z']
        new_date_timestamp = cnra_schema_utils.get_date_and_time_dict(date_timestamp)

        assert_equal(new_date_timestamp, '{\"date\": \"1850-07-23\", \"time\": \"14:19:59\"}')

    def test_get_time_date_and_time_dict_success_year_less_than_1900_without_timestamp(self):
        date_timestamp = ['1850-07-23T']
        new_date_timestamp = cnra_schema_utils.get_date_and_time_dict(date_timestamp)

        assert_equal(new_date_timestamp, '{\"date\": \"1850-07-23\", \"time\": \"\"}')

    def test_get_time_date_and_time_dict_failure_empty_string(self):
        date_timestamp = ''
        new_date_timestamp = cnra_schema_utils.get_date_and_time_dict(date_timestamp)

        assert_equal(new_date_timestamp, '{\"date\": \"\", \"time\": \"\"}')

    def test_get_time_date_and_time_dict_failure_unknown_string(self):
        date_timestamp = 'fasdfa'
        new_date_timestamp = cnra_schema_utils.get_date_and_time_dict(date_timestamp)

        assert_equal(new_date_timestamp, '{\"date\": \"\", \"time\": \"\"}')

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
