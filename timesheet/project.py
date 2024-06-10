#!/usr/bin/python3
"""Project codes class"""
from datetime import datetime

expected_monthly_hours = 168
expected_weekly_hours = 40

class Project():
    """Represent a staff project"""
    def __init__(self, *args, **kwargs):
        """Init for Project"""
        if kwargs:
            if kwargs.get("code", None) is not None:
                self.code = kwargs.get("code")
            if kwargs.get("salary_allocation", None) is not None:
                self.salary_allocation = float(kwargs.get("salary_allocation"))
            if kwargs.get("start_date", None) is not None:
                self.start_date = kwargs.get("start_date")
        else:
            self.code = args[0]
            self.salary_allocation = args[1]
            self.start_date = datetime.now()

    def set_start_date(self, start):
        """Set the day of the month the project will start
        This is used to calculate when to start recording the working hours
        in a month boundary
        """
        self.start_date = start

    def get_monthly_hours(self):
        """Get total monthly hours worked by project allocation"""
        return float(self.salary_allocation * expected_monthly_hours)

    def get_weekly_hours(self):
        """Get total weekly hours expected by project allocation"""
        return float(self.salary_allocation * expected_weekly_hours)
