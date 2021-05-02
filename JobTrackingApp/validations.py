import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_duration(value):
    pattern = re.compile(r"^((?P<h>\d+)\s?h[a-zA-Z]*)?\s?((?P<m>\d+)\s?m[a-zA-Z]*)?$")
    result = pattern.match(value)
    if result:
        if result.groupdict().get("h", False) or result.groupdict().get("m", False):
            pass
        else:
            raise ValidationError(
                _('%(value)s is not valid. Example of valid format:"2h45min"'),
                params={"value": value},
            )
    else:
        raise ValidationError(
            _('%(value)s is not valid. Example of valid format:"2h45min"'),
            params={"value": value},
        )


def format_duration(value):
    pattern = re.compile(r"^((?P<h>\d+)\s?h[a-zA-Z]*)?\s?((?P<m>\d+)\s?m[a-zA-Z]*)?$")
    result = pattern.match(value)
    data_value = ""
    if result:
        hours = result.groupdict().get("h", False)
        minutes = result.groupdict().get("m", False)
        if hours:
            data_value += f"{hours}h "
        if minutes:
            data_value += f"{minutes}min"
    return data_value


def fix_phone_number(phone_number):
    if phone_number:
        pattern = re.compile(r"^(\+?1?)\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*$")
        results = pattern.match(phone_number)
        country_code = "+1"
        group_list = results.groups()
        area_code = group_list[1]
        left_phone_number = group_list[2]
        right_phone_number = group_list[3]
        formed_phone_number = f"+1-{area_code}-{left_phone_number}-{right_phone_number}"
        return formed_phone_number
    else:
        return ""


if __name__ == "__main__":
    phone_number = "(323)-626-8959"
    print(fix_phone_number(phone_number))
