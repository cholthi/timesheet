#!/usr/bin/python3
"""Represents a calender monthly timesheet"""
import xlsxwriter
import datetime
from timesheet.helpers import date_iter, days_in_month, box, write_instructions
from xlsxwriter.utility import xl_rowcol_to_cell

timesheet = {}
now = datetime.datetime(2023, 9, 23)
admin_items = [
        "Paid Leave",
        "Sick Leave",
        "Unpaid Leave",
        "Statutory Holiday",
        "Other"
        ]

def write_excel(workbook, worksheet, file_name, staff):
    """Write staff timesheet data to an excel file"""

    worksheet.set_column('A:AI', 3)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 17.88)
    worksheet.set_column('D:D', 16)
    worksheet.set_row(12, 30)

    # Create header
    merge_format = workbook.add_format(
            {'bold': 1,
             'align': 'center',
            }
            )
    monthly_info_format = workbook.add_format({
        'font_size': 7,
        'valign': 'vcenter',
        'text_wrap': True,
        })
    month_format = workbook.add_format({'bold': 1,
        'align': 'left',
        'border': 1,
        })
    date_format = workbook.add_format({
        'num_format': 'mmm-yy',
        'font_size': 11,
        'border': 1,
        })

    monthly_info_format.set_rotation(90)
    # Top header
    worksheet.merge_range("B1:AJ1", "ForAfrika South Sudan", merge_format)
    worksheet.merge_range("B2:AJ2", "Staff Timesheet", merge_format)
    worksheet.merge_range('A4:A6', 'Monthly Info', monthly_info_format)
    worksheet.write(3, 1, 'Month:', month_format)
    worksheet.write_datetime(3, 2, now, date_format)

    # Prepared by box
    border_top = workbook.add_format({
        'top': 2,
        })
    border_bottom = workbook.add_format({
        'bottom': 2,
        })
    border_left = workbook.add_format({
        'left': 2,
        })
    border_right = workbook.add_format({
        'right': 2,
        })
    for col in range(2, 14):
        worksheet.write(7, col, None, border_top)
        worksheet.write(14, col, None, border_bottom)

    for row in range(7, 15):
        worksheet.write(row, 2, None, border_left)
        worksheet.write(row, 14, None, border_left)
    prepared_by_format = workbook.add_format({
        'bold': 1,
        'font_size': 11,
        'top': 1,
        'left': 1,
        })
    prepared_by_items_format = workbook.add_format({
        'left': 1,
        'align': 'center',
        'font_size': 10,
        })
    worksheet.write(7, 2, 'Prepared by:', prepared_by_format)
    worksheet.write(9, 2, 'Name:', prepared_by_items_format)
    worksheet.write(11, 2, 'Position:', prepared_by_items_format)
    worksheet.write(12, 2, 'Signature:', prepared_by_items_format)
    worksheet.write(13, 2, 'Date:', prepared_by_items_format)

    # staff name
    worksheet.write(9, 3, staff.name, prepared_by_items_format)
    # staff position
    worksheet.write(11, 3, staff.position, prepared_by_items_format)

    # Approved By box
    row_start = 7
    col_start = col + 2
    row_stop = 14
    col_stop = col_start + 15
    box(workbook, worksheet, row_start, col_start, row_stop, col_stop)

    worksheet.write(7, col_start + 1, 'Approved by:', prepared_by_format)
    worksheet.write(9, col_start + 1, 'Name:', prepared_by_items_format)
    worksheet.write(11, col_start + 1, 'Position:', prepared_by_items_format)
    worksheet.write(12, col_start + 1, 'Signature:', prepared_by_items_format)
    worksheet.write(13, col_start + 1, 'Date:', prepared_by_items_format)

     # staff name
    worksheet.write(9, col_start + 2, "Moses Iga", prepared_by_items_format)
    # staff position
    worksheet.write(11, col_start + 2, "Acting Finance Manager", prepared_by_items_format)


    msg1 = 'I have first hand knowledge of this  employee activities and have reviewed the allocation of hours worked,'
    msg2 = 'which was based on actual activities or percentage of activities and dertermined after- the-fact.'
    msg3 = 'I consider this to be a fair allocation of hours worked by this employee during the month of,'
    bold_format = workbook.add_format({'bold': 1})
    worksheet.write(3, 15, msg1, bold_format)
    worksheet.write(4, 15, msg2, bold_format)
    worksheet.write(5, 15, msg3, bold_format)
    
    write_staff_timesheet(workbook, worksheet, staff) 

def write_staff_timesheet(workbook, worksheet, staff):
    """Write a single staff timesheet"""
    header = ["No", "Description", "Code", ""]
    sub_header = ["A", "Projects", "", ""]
    header_format = workbook.add_format({
        'border': 1,
        'bold': 1,
        'font_size': 10,
        })
    for col in range(0,4):
        worksheet.write(16, col, header[col], header_format)
        worksheet.write(18, col, sub_header[col], header_format)
    projects_format = workbook.add_format({
        'font_size': 14,
        'font': 'Calibri Light',
        'bold': 1,
        'text_wrap': True,
        })
    row = 19
    for project in staff.projects:
        if len(project.name) > 32:
            worksheet.set_row(row, len(project.name) + 15)
            worksheet.write(row, 1, project.name, projects_format)
        else:
            worksheet.write(row, 1, project.name, projects_format)
        worksheet.write(row, 2, project.code, projects_format)
        row += 1
    calendar_format = workbook.add_format({
        'font_size': 10,
        'bold': 1,
        'border': 1,
        })
    weekend_format = workbook.add_format({
        'bg_color': '#808080',
        'border': 1,
        'font_size': 10,
        'bold': 1,
        })
    row = 16
    col = 4
    for date in date_iter(now.year, now.month):
        if date.weekday() < 5:
            worksheet.write(row, col, date.strftime('%a'), calendar_format)
            worksheet.write(row + 1, col, date.day, calendar_format)
        else:
            worksheet.write(row, col, date.strftime('%a'), weekend_format)
            worksheet.write(row + 1, col, date.day, weekend_format)
        col += 1
    total_hours = workbook.add_format({
        'font_size': 9,
        'bold': 1,
        'text_wrap': True,
        'border': 1,
        'valign': 'vcenter',
        })
    worksheet.merge_range(row, col + 1, row + 1, col + 1, 'Total Hours Worked', total_hours)
    staff_timesheet = staff.get_monthly_timesheet(now)
    row = 19
    col = 4
    ts_hours_format = workbook.add_format({
        'font_size': 8,
        'border': 1,
        })
    total_hours_sum_format = workbook.add_format({
        'bold': 1,
        'font_size': 8,
        'border': 1,
        })
    ts_weekend_format = workbook.add_format({
        'bg_color': '#808080',
        'border': 1,
        'font_size': 8,
        })
    for p_ts in staff_timesheet:
        col = 4
        for date in date_iter(now.year, now.month):
            hour = p_ts[date.day - 1] or None
            if date.weekday() < 5:
                worksheet.write(row, col, hour, ts_hours_format)
            else:
                # Weekend
                worksheet.write(row, col, None, ts_weekend_format)
            cell_1 = xl_rowcol_to_cell(row, 4)
            cell_2 = xl_rowcol_to_cell(row, days_in_month(date) + 4) # why 4? coz of extra empty column AI
            col += 1
        # Write the project total formula
        worksheet.write_formula(row, col + 1, f"=SUM({cell_1}:{cell_2})", ts_hours_format)
        row += 1
    # Write Administration part    
    empty_line_format = workbook.add_format({
        'border': 1,
        })
    admin_format = workbook.add_format({
        'bold': 1,
        'font_size': 10,
        'border': 1,
        })
    admin_item_format = workbook.add_format({
        'font_size': 10,
        'border': 1,
        })
    # Write empty row
    for col in range(0, 35):
        worksheet.write(row, col, None, empty_line_format)
    col = 0
    worksheet.write(row + 1, col, 'B', admin_format)
    worksheet.write(row + 1, col + 1, 'Administration', admin_format)
    calendar_format = workbook.add_format({
        'font_size': 10,
        'bold': 1,
        'border': 1,
        })
    weekend_format = workbook.add_format({
        'bg_color': '#808080',
        'border': 1,
        'font_size': 10,
        'bold': 1,
        })
    col = 4
    row += 1
    old_row = row
    for row in range(row, row + 8):
        for date in date_iter(now.year, now.month):
            if date.weekday() < 5:
                worksheet.write(row, col, None, calendar_format)
            else:
                worksheet.write(row, col, None, weekend_format)
            cell_1 = xl_rowcol_to_cell(row, 4)
            cell_2 = xl_rowcol_to_cell(row, days_in_month(date) + 4)
            col += 1
        worksheet.write(row, col + 1, f"=SUM({cell_1}:{cell_2})", ts_hours_format)
        col = 4

    col = 1
    for item in admin_items:
        worksheet.write(old_row + 2, col, item, admin_item_format)
        old_row += 1
    # Total row
    row = old_row + 2
    worksheet.write(row, 1, 'Total', admin_format)
    # Set column D17 background to gray
    bg_color = workbook.add_format({
        'bg_color': '#A6A6A6',
        'border': 1,
        })
    for row in range(16, row + 1):
        worksheet.write(row, 3, None, bg_color)

    # Total hours worked sum formula
    col = days_in_month(date) + 5
    cell_1 = xl_rowcol_to_cell(19, col)
    cell_2 = xl_rowcol_to_cell(row - 1, col)
    worksheet.write_formula(row, col, f"=SUM({cell_1}:{cell_2})", total_hours_sum_format)

    # Daily hours worked total sum formula
    for col in range(4, days_in_month(date) + 4):
            cell_1 = xl_rowcol_to_cell(19, col)
            cell_2 = xl_rowcol_to_cell(row - 1, col)
            worksheet.write_formula(row, col, f"=SUM({cell_1}:{cell_2})", total_hours_sum_format)
            box(workbook, worksheet, row + 2, 24, row + 5, 35)
    summary_format = workbook.add_format({
        'font_size': 10,
        })
    summary_total_format = workbook.add_format({
        'bg_color': "#ffff00",
        'font_size': 10,
        })
    worksheet.write(row + 3, 25, "Regular hours - current month", summary_format)
    worksheet.write(row + 4, 25, "Varaince", summary_format)
    worksheet.write(row + 3, 34, 21, admin_item_format)
    worksheet.write(row + 4, 35, 0.00, summary_total_format)
    cell_1 = xl_rowcol_to_cell(row + 3, 34)
    worksheet.write_formula(row + 3, 35, f"=SUM({cell_1} * 8)", summary_format)
    row += 6

    # Instructions
    write_instructions(workbook, worksheet, row)
