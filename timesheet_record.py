#!/usr/bin/python3
"""Represents a timesheet record of staff single project"""
from helpers import date_iter


class TimesheetRecord():
    """ Timesheet record """
    def __init__(self, date, hours):
        """ init timesheet record"""
        self.date = date
        self.hours = hours
