import re

from utils import *
from reader import Reader


ERROR_MESSAGE = '#ERR'


class PostfixNotation(Reader):

    """ Takes in a CSV file in Postnix notation and solves it. """

    def __init__(self, file):
        super().__init__(file)

        self.file = file
        self.data = []

        # An easy way to call the operations by string-type.
        # The second value is the number of inputs to include in the function
        self.operations = {
            '+':    [add, 2],
            '-':    [subtract, 2],
            '*':    [multiply, 2],
            '/':    [divide, 2],
            '^':    [power, 2],
            '!':    [factorial, 1],
            'ABS':  [absolute_value, 1],
            'ACOS': [acos, 1],
            'ASIN': [asin, 1],
            'ATAN': [atan, 1],
            'COS':  [cos, 1],
            'COSH': [cosh, 1],
            'LOG':  [log, 1],
            'SIN':  [sin, 1],
            'SINH': [sinh, 1],
            'SQRT': [square_root, 1],
            'TAN':  [tan, 1],
            'TANH': [tanh, 1],
        }

    def convert_cell_references(self, expression):
        """ Finds and replaces all cell references in a given expression. """

        # Loop through the expression to find and convert cell references
        for i in range(len(expression)):

            # We'll only touch cell references
            if self.is_cell_reference(expression[i]):

                # Get the column/row values
                column, row = self.get_cell_reference_indexes(expression[i])

                try:
                    # Grab the referenced value
                    referenced_value = self.data[row][column]

                    # Check if the cell being referenced is also referencing a cell.
                    # This may also include multiple references, or references as
                    # part of a normal expression, so we'll have to do it for all
                    # values in the reference value.
                    split_referenced_value = referenced_value.split()

                    for value in split_referenced_value:
                        if self.is_cell_reference(value):
                            return False

                    # Make sure the input value is not an error
                    if referenced_value != ERROR_MESSAGE:
                        # Replace the cell reference with the referenced value
                        expression[i] = referenced_value

                except IndexError:
                    # The column or row referenced doesn't exist,
                    # so the whole expression will result in an error
                    return [ERROR_MESSAGE]

        return expression

    @staticmethod
    def get_cell_reference_indexes(reference):
        """ Returns a column, row pair based on the LETTER NUMBER notation
        (A2, B4, etc - letters refer to columns, numbers to rows). """

        # Separate the letters and numbers in the cell reference
        column_part = ''.join([char for char in reference if char.isalpha()])
        row_part = ''.join([char for char in reference if char.isdigit()])

        # Convert the column part from letters to a number
        column_index = 0
        for char in column_part:
            column_index = column_index * 26 + (ord(char.upper()) - ord('A') + 1)

        # Convert the row part to an integer
        row_index = int(row_part)

        # Return the column and row indices (subtracting 1 to convert to zero-based index if needed)
        return column_index - 1, row_index - 1

    @staticmethod
    def is_cell_reference(value):
        """ A quick check if a given value is a cell reference. """

        # Define the regular expression pattern for the cell reference format
        pattern = re.compile(r'^\s*[a-zA-Z]\s*[0-9]\s*$')

        # Check if the value matches the pattern
        return pattern.match(value)

    def perform_operation(self, expression):
        """ Performs a single operation in a given expression. """

        # Iterate through each element and its index in 'expression'
        for i in range(len(expression)):

            # Check if the value is in 'self.operations'
            if expression[i] in self.operations:

                # Grab operator
                operator = expression.pop(i)

                # If it is, perform operation
                operation = self.operations[operator][0]
                n_inputs = self.operations[operator][1]

                # Expressions have either 1 or 2 inputs,
                # and need to be handled slightly differently
                if n_inputs == 1:
                    input1 = float(expression.pop(i - 1))
                    result = operation(input1)
                    expression.insert(i - 1, result)

                elif n_inputs == 2:
                    input2 = float(expression.pop(i-1))
                    input1 = float(expression.pop(i-2))
                    result = operation(input1, input2)
                    expression.insert(i-2, str(result))

                return expression

    def print_output(self):
        """ Print the output of the data to console. """

        for row in self.data:

            # Print each string row-by-row
            row_output = ''
            for cell in row:
                row_output += cell + ','

            # Remove the final ','
            row_output = row_output.rstrip(',')

            print(row_output)

    def run(self):

        # Grab the data from the CSV file
        self.data = self.read_csv_file()

        # Will end once all cells have been solved
        self.solve()

        # Do it once more to fill in any references that can't be made,
        # E.g. self referencing cells or circular referencing cells
        self.solve(final_lap=True)

        self.print_output()

    def solve(self, final_lap=False):
        """ Run until the program stops finding solutions. """

        while True:

            # To handle references to cells that haven't been solved yet, the
            # program will repeatedly run until there are no more available solutions
            solution_counter = 0

            # Solve expressions, row-by-row
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):

                    # Split the expression into strings, by 1 or more spaces
                    expression = self.data[i][j].split()

                    # Check for any cell references in the expression
                    expression = self.convert_cell_references(expression)

                    if expression is not False:
                        # Solve the expression if possible, otherwise return #ERR
                        solution = self.solve_expression(expression)

                        # Check if a new solution was found
                        solution_counter += (self.data[i][j] != solution)

                        # Update the result
                        self.data[i][j] = str(solution)

                    elif final_lap:

                        # If a cell reference hasn't been discovered by now, give up on it
                        self.data[i][j] = ERROR_MESSAGE


            # i.e. there's no more available solutions left
            if solution_counter == 0 or final_lap:
                break

    def solve_expression(self, expression):
        """ Iteratively solves all of the operations in a given expression. """

        try:
            # Repeatedly solve each operation until only the final result remains...
            while len(expression) > 1:
                expression = self.perform_operation(expression)

            # Finally, grab the solution
            solution = expression[0]

            # Make sure it's numeric
            if is_number(solution):
                return solution
            else:
                return ERROR_MESSAGE

        except TypeError:
            return ERROR_MESSAGE
