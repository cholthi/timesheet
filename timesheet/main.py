#!/usr/bin/python3
""" Test script to generate excel"""
import timesheet.timesheet as timesheet
from timesheet.excel_store import ExcelStorage
import xlsxwriter


def generate(input_path, output_path, salary_date):
    timesheet.now = salary_date
    s = ExcelStorage(input_path)
    workbook = xlsxwriter.Workbook(output_path)
    for _, staff in s.all().items():
        worksheet = workbook.add_worksheet(staff.name)
        timesheet.write_excel(workbook, worksheet, output_path, staff)
    workbook.close()

