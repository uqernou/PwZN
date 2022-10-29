import argparse
import histogram as hist


class Main01:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Argument parser")
        parser.add_argument("-p", "--Path", help="Example: Path argument", required=True)
        parser.add_argument("-n", "--Number", help="Example: Number argument", required=False, default="10")
        parser.add_argument("-m", "--MinimumLetters", help="Example: MinimumLetters argument", required=False, default="0")

        argument = parser.parse_args()
        status = False
        if argument.Path:
            print("You have used '-p' or '--Path' with argument: {0}".format(argument.Path))
            self.path_to_file = argument.Path
            status = True
        if argument.Number:
            print("You have used '-m' or '--MinimumLetters' with argument: {0}".format(argument.Number))
            self.numbers = argument.Number
        if argument.MinimumLetters:
            print("You have used '-n' or '--Number' with argument: {0}".format(argument.MinimumLetters))
            self.minimum_letters = argument.MinimumLetters
        if not status:
            print("You have to use, at least '-p' or '--Path' argument")
            return
        histogram = hist.Histogram(self.path_to_file, self.numbers, self.minimum_letters)
        histogram.load_file()
        histogram.pring_histogram()

if __name__ == '__main__':
    app = Main01()
