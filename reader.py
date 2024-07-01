import csv


class Reader:

    """ A parent class that could be extended to include other reader types. """

    def __init__(self, file):

        self.file = file
        self.data = []

    def read_csv_file(self):
        # Read in the CSV file
        with open(self.file, newline='') as f:
            return [[cell for cell in row] for row in csv.reader(f)]
