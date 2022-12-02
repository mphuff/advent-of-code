from enum import Enum
import sys
import csv


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    # Specifies what shape this particular shape defeats as only one option is valid
    def beats(self):
        if self == Shape.ROCK:
            return Shape.SCISSORS
        elif self == Shape.PAPER:
            return Shape.ROCK
        elif self == Shape.SCISSORS:
            return Shape.PAPER

    # Specifies what shape this particular shape defeats as only one option is valid
    def loses_to(self):
        if self == Shape.SCISSORS:
            return Shape.ROCK
        elif self == Shape.ROCK:
            return Shape.PAPER
        elif self == Shape.PAPER:
            return Shape.SCISSORS

    # Determines whether this shape beats the other one
    def defeats_other(self, other_shape):
        if self.name == other_shape.name:
            return Score.DRAW

        if self.beats() == other_shape:
            return Score.WIN

        return Score.LOSS


class Score(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6

    def shape_from_desired_outcome(self, opponent_shape):
        if self == Score.DRAW:
            return opponent_shape
        elif self == Score.LOSS:
            # retrieve the shape that opponent shape defeats
            return opponent_shape.beats()
        elif self == Score.WIN:
            # retrieve the shape that this shape loses_to
            return opponent_shape.loses_to()


class InputToShape(Enum):
    A = Shape.ROCK
    B = Shape.PAPER
    C = Shape.SCISSORS
    X = Shape.ROCK
    Y = Shape.PAPER
    Z = Shape.SCISSORS


class OutcomeToScore(Enum):
    X = Score.LOSS
    Y = Score.DRAW
    Z = Score.WIN


def part1(input_csv):
    running_my_score = 0

    with open(input_csv) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            opponent_shape = InputToShape.__getitem__(row[0]).value
            my_shape = InputToShape.__getitem__(row[1]).value

            # outcome will be a Score object, returned by defeats_other method
            outcome = my_shape.defeats_other(opponent_shape)

            running_my_score += outcome.value + my_shape.value

    print("Part 1 final score = %s" % running_my_score)


def part2(input_csv):
    running_my_score = 0

    with open(input_csv) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            opponent_shape = InputToShape.__getitem__(row[0]).value
            desired_outcome = OutcomeToScore.__getitem__(row[1]).value

            my_shape = desired_outcome.shape_from_desired_outcome(opponent_shape)

            # outcome will be a Score object, returned by defeats_other method
            outcome = my_shape.defeats_other(opponent_shape)

            assert outcome == desired_outcome

            running_my_score += outcome.value + my_shape.value

    print("Part 2 final score = %s" % running_my_score)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    input_file = sys.argv.pop()
    part1(input_file)
    part2(input_file)