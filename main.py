from postfix_notation import PostfixNotation

# Relative file path to CSV file
csv_file = 'rpn_examples.csv'

pn = PostfixNotation(csv_file).run()
