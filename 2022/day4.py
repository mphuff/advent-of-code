import csv
import sys


class ElfDetails:

    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def __str__(self):
        return "%s - %s" % (self.min_val, self.max_val)

    # Returns size of range, inclusive
    # e.g. 6-6 range will return 1 for range size
    def get_range_size(self):
        return self.max_val - self.min_val + 1

    # Returns true if the range of this elf fully encompasses the range of the other elf
    # Example: this elf is 2-6, other elf is 6-6, will return true
    def elf_encompasses_other(self, other_elf):
        if self.get_range_size() >= other_elf.get_range_size():
            if self.min_val <= other_elf.min_val and self.max_val >= other_elf.max_val:
                return True

        return False


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile)

        overlapping_elf_pairs = []
        for row in reader:
            elf1 = ElfDetails(int(row[0].split('-')[0]),
                              int(row[0].split('-')[1]))
            elf2 = ElfDetails(int(row[1].split('-')[0]),
                              int(row[1].split('-')[1]))

            if elf1.elf_encompasses_other(elf2) or elf2.elf_encompasses_other(elf1):
                overlapping_elf_pairs.append({'elf1': elf1, 'elf2': elf2})

        print(len(overlapping_elf_pairs))
