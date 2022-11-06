import argparse
import histogram as hist


class Main01:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Argument parser")
        parser.add_argument("-p", "--Path", help="Path argument", required=True, type=str)
        parser.add_argument("-n", "--Number", help="Number argument", required=False, type=int, default=10)
        parser.add_argument("-m", "--MinimumLetters", help="MinimumLetters argument", required=False, type=int,
                            default=0)
        argument = parser.parse_args()
        self.path_to_file = argument.Path
        self.numbers = argument.Number
        self.minimum_letters = argument.MinimumLetters
        histogram = hist.Histogram(self.path_to_file, self.numbers, self.minimum_letters)
        histogram.load_file()
        histogram.pring_histogram()


if __name__ == '__main__':
    app = Main01()
