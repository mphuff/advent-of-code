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

    # Returns true if the max value of this elf range is less than the other; indicating
    # that the elves are mutually exclusive
    def elf_mutually_exclusive(self, other_elf):
        return self.max_val < other_elf.min_val


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile)

        fully_encompassed_pairs = []
        overlapping_pairs = []
        total_pairs = 0
        for row in reader:
            total_pairs += 1
            elf1 = ElfDetails(int(row[0].split('-')[0]),
                              int(row[0].split('-')[1]))
            elf2 = ElfDetails(int(row[1].split('-')[0]),
                              int(row[1].split('-')[1]))

            if elf1.elf_encompasses_other(elf2) or elf2.elf_encompasses_other(elf1):
                fully_encompassed_pairs.append({'elf1': elf1, 'elf2': elf2})

            # Part 2 - determine mutual exclusivity
            if elf1.elf_mutually_exclusive(elf2) or elf2.elf_mutually_exclusive(elf1):
                overlapping_pairs.append({'elf1': elf1, 'elf2': elf2})

        print("Total pairs = %s" % total_pairs)
        print("Overlapping elf pairs = %s" % len(fully_encompassed_pairs))
        print("Overlapping elf pairs = %s" % (total_pairs - len(overlapping_pairs)))
