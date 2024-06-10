#!/usr/bin/python3
"""Helper functions"""
import datetime
import calendar as c


instructions = [
        "Update the Monthly Info section",
        "Update dates to the appropriate days",
        "Update the number of working days for the month in the Self Check section under Days (the Hours will calculate automatically)",
        "Complete your hours worked per day, not to exceed 8 hours per day",
        "For ease of calculation, if required, use quarterly (0.25) hours (equivalent of 15 minutes) as your smallest increment",
        "Preparer:  Ensure that the Prepared by section is completed before submission for approval",
        "Preparer:  Ensure that the Variance in the Self Check section is zero",
        "Approver:  Ensure that the Approved by section is completed",
        "Approver:  Ensure that the Variance in the Self Check section is zero",
        "Percentage hours worked should be used to allocate salaries"
    ]

def date_iter(year, month):
    """Iterate over the dates in year, month combination"""
    for i in range(1, c.monthrange(year, month)[1] + 1):
        yield datetime.date(year, month, i)

def working_days_iter(monthly_hours):
    """Returns number of days assuming a hours expected per day is 8 hours"""
    while monthly_hours > 8:
        yield round(float(8), 2)
        monthly_hours -= 8
    yield round(float(monthly_hours), 2)

def days_in_month(date):
    """ Return the number of days in a month"""
    return c.monthrange(date.year, date.month)[1]

def build_timesheet(date):
    """Return a renderable representation of user timesheet"""
    from timesheet.timesheet_record import TimesheetRecord
    ts = []
    for d in date_iter(date.year, date.month):
        tr = TimesheetRecord(d, float(0))
        ts.append(tr)
    return ts

def add_to_format(existing_format, dict_of_properties, workbook):
    """Give a format you want to extend and a dict of the properties you want to
    extend it with, and you get them returned in a single format"""
    new_dict={}
    for key, value in existing_format.__dict__.items():
        if (value != 0) and (value != {}) and (value != None):
            new_dict[key]=value
    # del new_dict['escapes']

    return(workbook.add_format(dict(new_dict.items() | dict_of_properties.items())))

def box(workbook, sheet_name, row_start, col_start, row_stop, col_stop):
    """Makes an RxC box. Use integers, not the 'A1' format"""

    rows = row_stop - row_start + 1
    cols = col_stop - col_start + 1

    for x in range((rows) * (cols)): # Total number of cells in the rectangle

        box_form = workbook.add_format()   # The format resets each loop
        row = row_start + (x // cols)
        column = col_start + (x % cols)

        if x < (cols):                     # If it's on the top row
            box_form = add_to_format(box_form, {'top':2}, workbook)
        if x >= ((rows * cols) - cols):    # If it's on the bottom row
            box_form = add_to_format(box_form, {'bottom':2}, workbook)
        if x % cols == 0:                  # If it's on the left column
            box_form = add_to_format(box_form, {'left':2}, workbook)
        if x % cols == (cols - 1):         # If it's on the right column
            box_form = add_to_format(box_form, {'right':2}, workbook)

        sheet_name.write(row, column, "", box_form)

def write_instructions(workbook, worksheet, row):
    ins_format_header = workbook.add_format({
        'bold': 1,
        'italic': True,
        'font_size': 10,
        'border': 1
        })
    border_format = workbook.add_format({
        'top': 1,
        'bottom': 1,
        })
    ins_format = workbook.add_format({
        'font_size': 10,
        })
    for col in range(0, 24):
        worksheet.write(row, col, None, border_format)
    # Write the instruction header
    worksheet.write(row, 1, "Instructions", ins_format_header)
    row = row + 1
    for i, ins in enumerate(instructions):
        worksheet.write(row, 0, i + 1, ins_format)
        worksheet.write(row, 1, ins, ins_format)
        row += 1
