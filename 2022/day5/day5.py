import csv
import sys


class CrateArrangement:

    def __init__(self, stacks):
        self.stacks = stacks

    def process_step(self, how_many, from_stack, to_stack):
        # print("Process step: %s to process, from %s to %s" % (how_many, from_stack, to_stack))
        for i in range(how_many):
            popped = self.stacks[from_stack].pop(0)
            # print("Popped %s from stack %s and appending to %s" % (popped, from_stack, to_stack))
            self.stacks[to_stack].insert(0, popped)
            # print("After process, stacks: %s" % self.stacks)

    def output_top(self):
        output = ""
        for stack in sorted(self.stacks.keys()):
            output += self.stacks[stack][0].replace("[", "").replace("]", "")
        return output


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        initialized_stacks = {}
        crate_arrangement = None
        for row in reader:
            column_num = 0
            # When I encounter empty row, stacks are fully initialized
            if len(row) == 0:
                print(initialized_stacks)
                crate_arrangement = CrateArrangement(initialized_stacks)
            # When crate arrangement is non-empty, now follow instructions
            elif crate_arrangement is not None:
                # parse instruction and pass to CrateArrangement
                # print(row)
                crate_arrangement.process_step(int(row[1]), int(row[3]), int(row[5]))
            else:
                for column in row:
                    column_num += 1
                    if column == 'xxx' or column.startswith('-'):
                        continue
                    if column_num not in initialized_stacks:
                        initialized_stacks[column_num] = []

                    initialized_stacks[column_num].append(column)

        print(crate_arrangement.output_top())