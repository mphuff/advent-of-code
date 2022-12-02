from enum import Enum
import sys
import csv


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    # Determines whether this shape beats the other one
    def defeats_other(self, other_shape):
        if self.name == other_shape.name:
            return Score.DRAW

        if self == Shape.ROCK and other_shape == Shape.SCISSORS:
            return Score.WIN
        elif self == Shape.SCISSORS and other_shape == Shape.PAPER:
            return Score.WIN
        elif self == Shape.PAPER and other_shape == Shape.ROCK:
            return Score.WIN

        return Score.LOSS


class Score(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


class InputToShape(Enum):
    A = Shape.ROCK
    B = Shape.PAPER
    C = Shape.SCISSORS
    X = Shape.ROCK
    Y = Shape.PAPER
    Z = Shape.SCISSORS


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    running_computer_score = 0
    running_my_score = 0

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            print(',,,,,'.join(row))
            opponent_shape = InputToShape.__getitem__(row[0]).value
            my_shape = InputToShape.__getitem__(row[1]).value
            print(opponent_shape)
            print(my_shape)

            # outcome will be a Score object, returned by defeats_other method
            outcome = my_shape.defeats_other(opponent_shape)
            print("outcome = %s" % outcome)

            score_this_round = outcome.value + my_shape.value
            running_my_score += score_this_round

    print("My final score = %s" % running_my_score)