# This file serves as proxy for importing load-json.py
# Reference: https://stackoverflow.com/questions/8350853/how-to-import-module-when-module-name-has-a-dash-or-hyphen-in-it

tmp = __import__("tsv-2-json")
globals().update(vars(tmp))