import re
import sys

def main():
    with open(sys.argv[1]) as f:
        batch = f.read()

    required_fields = { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' }

    fields_regex = re.compile(r'([a-z]{3}):\S+\s*', re.M)
    valid_count = 0
    passports = batch.split('\n\n')
    for passport in passports:
        fields_present = set(fields_regex.findall(passport))
        if fields_present.issuperset(required_fields):
            valid_count += 1

    print(valid_count)



if __name__ == '__main__':
    main()
