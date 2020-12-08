from six import text_type


def convert_list_to_string(list_to_convert, delimiter=' '):
    if isinstance(list_to_convert, list):
        converted_str = delimiter.join(text_type(x) for x in list_to_convert)
        return converted_str

    return list_to_convert
