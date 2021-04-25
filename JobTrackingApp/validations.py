import re


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
