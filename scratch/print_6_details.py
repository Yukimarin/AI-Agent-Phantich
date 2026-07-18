import sys
import os
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Run the evaluation script internally or just import and print if possible
# Since evaluate_new_standards_v2.py prints it, let's copy the code or read and print from it.
# We will write a small script that reproduces the calculations specifically for the 6 target staff and outputs them clearly.
# Let's read the evaluate_new_standards_v2.py and run it to get the results as a dictionary.

# Let's execute evaluate_new_standards_v2.py and save the full result to a JSON file first.
# We'll edit evaluate_new_standards_v2.py to write a JSON file.
