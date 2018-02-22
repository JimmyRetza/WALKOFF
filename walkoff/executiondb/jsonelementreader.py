from six import string_types
from uuid import UUID


class JsonElementReader(object):
    """
    Reads an ExecutionElement and converts it to JSON
    """

    @staticmethod
    def read(element):
        """
        Reads an ExecutionElement and converts it to JSON

        Args:
            element (ExecutionElement): The ExecutionElement

        Returns:
            (dict) The JSON representation of the ExecutionElement
        """
        from walkoff.executiondb.representable import Representable
        accumulator = {}
        for field, value in ((field, getattr(element, field)) for field in dir(element)
                             if not field.startswith('_')
                             and not callable(getattr(element, field))
                             and field != 'metadata'):
            if isinstance(value, Representable):
                accumulator[field] = JsonElementReader.read(value)
            elif isinstance(value, UUID):
                accumulator[field] = str(value)
            elif isinstance(value, list):
                JsonElementReader._read_list(field, value, accumulator)
            elif isinstance(value, dict):
                JsonElementReader._read_dict(field, value, accumulator)
            elif value is not None:
                accumulator[field] = value
        return accumulator

    @staticmethod
    def _read_list(field_name, list_, accumulator):
        accumulator[field_name] = []
        count = 0
        for list_value in list_:
            if list_value is not None:
                count += 1
                if not (isinstance(list_value, string_types) or type(list_value) in (float, int, bool)):
                    accumulator[field_name].append(JsonElementReader.read(list_value))
                else:
                    accumulator[field_name].append(list_value)

    @staticmethod
    def _read_dict(field_name, dict_, accumulator):
        from walkoff.executiondb.representable import Representable
        if dict_ and all(
                (isinstance(dict_value, Representable)) for dict_value in
                dict_.values()):
            accumulator[field_name] = [JsonElementReader.read(dict_value) for dict_value in dict_.values()]
        elif dict_ and all(isinstance(dict_value, list) for dict_value in dict_.values()):
            if all((isinstance(list_value, Representable) for list_value in dict_value) for dict_value in
                   dict_.values()):
                field_accumulator = []
                for dict_value in dict_.values():
                    list_acc = [JsonElementReader.read(list_value) for list_value in dict_value]
                    field_accumulator.extend(list_acc)
                accumulator[field_name] = field_accumulator
        elif field_name in ('position', 'value'):
            accumulator[field_name] = dict_
        else:
            accumulator[field_name] = [{'name': dict_key, 'value': dict_value} for dict_key, dict_value in dict_.items()
                                       if not isinstance(dict_value, Representable)]