import string

class passport:
    required_keys = [
        "byr",      # Birth Year
        "iyr",      # Issue Year
        "eyr",      # Expiration Year
        "hgt",      # Height
        "hcl",      # Hair Color
        "ecl",      # Eye Color
        "pid"       # Passport ID
    ]
    info = None

    def __init__(self, passport_text):
        self.info = dict()
        self.parse(passport_text)
    
    def keyValid(self):
        return all([x in self.info.keys() for x in self.required_keys])

    def _v_Year(self, val, min, max):
        if len(val) != 4:
            return False
        if all(x in string.digits for x in val):
            if int(val) >= min and int(val) <= max:
                return True
        return False

    def _v_hgt(self, val):
        units = val[-2:]
        if units not in ['cm', 'in']:
            return False
        num = val[:-2]
        if not all(x in string.digits for x in num):
            return False
        if units == 'cm':
            return True if int(num) >= 150 and int(num) <= 193 else False
        if units == 'in':
            return True if int(num) >= 59 and int(num) <= 76 else False
    
    def _v_color(self, val):
        if val[0] != '#':
            return False
        if not all(x in string.hexdigits for x in val[1:]):
            return False
        return False if len(val) != 7 else True

    def valueValid(self):
        if self.keyValid():
            if not self._v_Year(self.info['byr'], 1920, 2002): return False
            if not self._v_Year(self.info['iyr'], 2010, 2020): return False
            if not self._v_Year(self.info['eyr'], 2020, 2030): return False
            if not self._v_hgt(self.info['hgt']): return False
            if not self._v_color(self.info['hcl']): return False
            if self.info['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                return False
            if len(self.info['pid']) != 9:
                return False
            if not all([x in string.digits for x in self.info['pid']]):return False
            return True
        else: return False

    def parse(self, passport_text: str):
        """
        passport is one passport entry with or without newlines
        """
        fields = passport_text.split()
        for field in fields:
            key, value = field.split(':')
            self.info[key] = value

if __name__ == "__main__":
    with open('day4.in') as f:
        # Passports are separated by two newlines
        passport_text_list = f.read().split("\n\n")
    passports1 = []
    passports2 = []
    for passport_text in passport_text_list:
        p = passport(passport_text)
        if p.keyValid():
            passports1.append(p)
        if p.valueValid():
            passports2.append(p)
    print(f"Day 4 Part 1: { len(passports1) } of { len(passport_text_list)} are valid.")
    print(f"Day 4 Part 2: { len(passports2) } of { len(passport_text_list)} are valid.")