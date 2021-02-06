# coding=utf-8

"""
Creates an xlsx file set up for analyzing WBs

Usage:
  make-template.py OUT (--conditions=<int>) (--ab=<str>...) (--loading-ctrl=<str>)
  make-template.py -h | --help
  make-template.py --version

Arguments:
  OUT  Where the file should be saved to


Options:
  -h --help  Show this screen.
  --conditions=<int>  [default: 2] The number of conditions.
  --ab=<str>  [default: Ab1] The name of each antibody
  --loading-ctrl=<str>  [default: GAPDH] The name of the loading control


Output:
  An XLSX file
"""

import xlsxwriter
from schema import Schema, And, Or, Use, SchemaError, Optional
from docopt import docopt
from pathlib import Path

arguments = docopt(__doc__, version='1.0')
schema_def = {
  'OUT': lambda x: len(x) >= 0,
  '--conditions': And(Use(int), lambda n: 0 < n, error='--conditions must be greater than 0'),
  '--ab': [ lambda x: len(x) >= 0 ],
  '--loading-ctrl': lambda x: len(x) >= 0,
  Optional('--help'): bool,
  Optional('--version'): bool
}

schema = Schema(schema_def)

try:
  arguments = schema.validate(arguments)
except SchemaError as error:
  print(error)
  exit(1)
  
out = Path(arguments['OUT']).resolve()

workbook = xlsxwriter.Workbook(str(out))

# Set up formatting
title_format = workbook.add_format({
  'bold': True,
  'bottom': 6,
  'right': 1,
  'top': 1,
  'text_wrap': True
})

condition_end_format = workbook.add_format({
  'bottom': 1
})

ab_end_format = workbook.add_format({
  'bottom': 6
})

merge_format = workbook.add_format({
  'valign': 'vcenter',
  'bottom': 6
})

worksheet = workbook.add_worksheet()

# Setup title bar
worksheet.write('A1', 'RPE-1 cells')
worksheet.write('A2', 'Condition')
worksheet.write('B2', 'Amt lysate')
worksheet.write('C2', 'Antibody')
worksheet.write('D2', 'S/B')
worksheet.write('E2', 'Area')
worksheet.write('F2', 'Mean gray')
worksheet.write('G2', 'IntDen')
worksheet.write('H2', 'Bkgd subtract')
worksheet.write('I2', 'Norm to ' + arguments['--loading-ctrl'])
worksheet.write('J2', 'Norm to (+) Ctrl')
worksheet.set_row(1, None, title_format)


def write_row(worksheet, s_row, b_row, b_format):
  worksheet.write('A' + s_row, 'Condition ' + str((i+1)))
  worksheet.write('D' + s_row, 'S')
  worksheet.write('D' + b_row, 'B')
  worksheet.write_formula('G' + s_row, '=E' + s_row + '*F' + s_row)
  worksheet.write_formula('G' + b_row, '=E' + b_row + '*F' + b_row)
  worksheet.write_formula('H' + s_row, '=G' + s_row + '-G' + b_row)
  worksheet.set_row(int(b_row)-1, None, condition_end_format)

# Add conditions
for ab_idx in range(0, len(arguments['--ab'])):
  start_row = 3+ab_idx*arguments['--conditions']*4 # 2 rows / condition, done twice (once for loading, once for Ab)
  # Loading control
  for i in range(0,arguments['--conditions']):
    s_row = str(start_row+i*2)
    b_row = str(start_row+1+i*2)
    write_row(worksheet, s_row, b_row, condition_end_format)
  worksheet.merge_range(start_row-1, 2, int(b_row)-1, 2, arguments['--loading-ctrl'], merge_format)
  worksheet.set_row(int(b_row)-1, None, ab_end_format)
  # Ab
  start_row += arguments['--conditions']*2
  for i in range(0,arguments['--conditions']):
    s_row = str(start_row+i*2)
    b_row = str(start_row+1+i*2)
    write_row(worksheet, s_row, b_row, condition_end_format)
  worksheet.merge_range(start_row-1, 2, int(b_row)-1, 2, arguments['--ab'][ab_idx], merge_format)
  worksheet.set_row(int(b_row)-1, None, ab_end_format)


workbook.close()

