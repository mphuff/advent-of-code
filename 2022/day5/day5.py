import csv
import sys
import copy


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

    def process_step_v2(self, how_many, from_stack, to_stack):
        if how_many == 1:
            self.process_step(how_many, from_stack, to_stack)
        else:
            temp_list = []
            for i in range(how_many):
                temp_list.append(self.stacks[from_stack].pop(0))
            temp_list.reverse()
            for val in temp_list:
                self.stacks[to_stack].insert(0, val)

    def output_top(self):
        output = ""
        for stack in sorted(self.stacks.keys()):
            output += self.stacks[stack][0].replace("[", "").replace("]", "")
        return output


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    # NOTE: Updated input file to ensure consistent array sizing
    # Blank column values I expect 'xxx' as a value
    # Column 'number' rows are just ignored but prefixed when with a '-' as well
    # Sample input file (exclude comment prefix):
    # xxx [D] xxx
    # [N] [C] xxx
    # [Z] [M] [P]
    # -1- -2- -3-
    #
    # move 1 from 2 to 1
    # move 3 from 1 to 3
    # move 2 from 2 to 1
    # move 1 from 1 to 2
    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        initialized_stacks = {}
        crate_arrangement_pt1 = None
        crate_arrangement_pt2 = None
        for row in reader:
            column_num = 0
            # When I encounter empty row, stacks are fully initialized
            if len(row) == 0:
                print(initialized_stacks)
                crate_arrangement_pt1 = CrateArrangement(initialized_stacks)
                crate_arrangement_pt2 = CrateArrangement(copy.deepcopy(initialized_stacks))
            # When crate arrangement is non-empty, now follow instructions
            elif crate_arrangement_pt1 is not None:
                # parse instruction and pass to CrateArrangement
                crate_arrangement_pt1.process_step(int(row[1]), int(row[3]), int(row[5]))
                crate_arrangement_pt2.process_step_v2(int(row[1]), int(row[3]), int(row[5]))
            else:
                for column in row:
                    column_num += 1
                    if column == 'xxx' or column.startswith('-'):
                        continue
                    if column_num not in initialized_stacks:
                        initialized_stacks[column_num] = []

                    initialized_stacks[column_num].append(column)

        print("Step 1 crate_arrangement = %s" % crate_arrangement_pt1.output_top())
        print("Step 2 crate_arrangement = %s" % crate_arrangement_pt2.output_top())
