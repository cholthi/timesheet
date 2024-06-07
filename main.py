#!/usr/bin/python3
""" Test script to generate excel"""
import timesheet
from excel_store import ExcelStorage
import xlsxwriter


def run():
    output_path = "For Afrika Staff Timesheet.xlsx"
    path = "Juba_Sept_2023_Staff_Allocation.xlsx"
    s = ExcelStorage(path)
    workbook = xlsxwriter.Workbook(output_path)
    for _, staff in s.all().items():
        worksheet = workbook.add_worksheet(staff.name)
        timesheet.write_excel(workbook, worksheet, output_path, staff)
    workbook.close()

