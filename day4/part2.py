import re
import sys


def main():
    with open(sys.argv[1]) as f:
        batch = f.read()

    validators = {
        'byr': validate_byr,
        'iyr': validate_iyr,
        'eyr': validate_eyr,
        'hgt': validate_hgt,
        'hcl': validate_hcl,
        'ecl': validate_ecl,
        'pid': validate_pid,
        'cid': lambda value: True
    }
    required_fields = set(validators.keys())
    required_fields.remove('cid')

    fields_regex = re.compile(r'([a-z]{3}):(\S+)\s*', re.M)
    valid_count = 0
    passports = batch.split('\n\n')
    for passport in passports:
        matches = fields_regex.findall(passport)
        fields_present = set(match[0] for match in matches)
        if fields_present.issuperset(required_fields):
            if all(validators[field](value) for field, value in matches):
                valid_count += 1

    print(valid_count)


def try_parse_int(value):
    try:
        return True, int(value)
    except:
        return False, None


def validate_byr(value):
    success, year = try_parse_int(value)
    return success and 1920 <= year <= 2002

def validate_iyr(value):
    success, year = try_parse_int(value)
    return success and 2010 <= year <= 2020

def validate_eyr(value):
    success, year = try_parse_int(value)
    return success and 2020 <= year <= 2030

def validate_hgt(value):
    if value.endswith('cm'):
        success, height_cm = try_parse_int(value[:-2])
        return success and 150 <= height_cm <= 193
    elif value.endswith('in'):
        success, height_in = try_parse_int(value[:-2])
        return success and 59 <= height_in <= 76
    return False

hair_color_regex = re.compile(r'#[0-9a-f]{6}')
def validate_hcl(value):
    return hair_color_regex.fullmatch(value) is not None

valid_eye_colors = { 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' }
def validate_ecl(value):
    return value in valid_eye_colors

passport_regex = re.compile(r'\d{9}')
def validate_pid(value):
    return passport_regex.fullmatch(value) is not None

if __name__ == '__main__':
    main()
