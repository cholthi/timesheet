#!/usr/bin/python3
"""Represent For Afrika payroll staff"""
import timesheet.helpers as helpers


class Staff():
    """ForAfrika payroll Staff"""
    def __init__(self, name, position, location):
        self.name = name
        self.position = position
        self.location = location
        self._projects = []

    def __repr():
        return f"({self.name}) at {self.location}"

    @property
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = value

    def monthly_hours_by_project(self, project_code: str) -> float:
        """Convert project percent allocation to hours worked in a month"""
        for project in self._projects:
            if project.code == project_code:
                return project.get_monthly_hours()
        return 0

    def weekly_hours_by_project(self, project_code: str) -> float:
        """Convert project percent allocation to hours wroked in a week"""
        for project in self._projects:
            if project.code == project_code:
                return project.get_weekly_hours()
        return 0
    def get_monthly_timesheet(self, date):
        """Get a user monthly timesheet representation"""
        ts = []
        expected_hours_per_day = 8
        monthly_timesheet = helpers.build_timesheet(date)
        for project in self.projects:
            project_worked_days = list(helpers.working_days_iter(self.monthly_hours_by_project(project.code)))
            # Sort them to get the fraction worked hours infront
            project_worked_days.sort()
            fraction_timesheet_index = None
            project_worked_days_index = 0
            p_ts = [0 for d in list(helpers.date_iter(date.year, date.month))]
            # Reset the wroking day index to 0
            current_day_index = None
            # For everyday of the month, check if we can enter a timesheet entry
            for d in helpers.date_iter(date.year, date.month):
                current_day_index = d.day - 1
                # if len(project_worked_days) == 0:
                #    break
                # No timesheet entry for wekend
                if d.weekday() > 4:
                    continue
                if project_worked_days_index > len(project_worked_days) - 1:
                    break
                if monthly_timesheet[d.day - 1].hours:
                    if monthly_timesheet[d.day - 1].hours == expected_hours_per_day:
                        continue
                    elif monthly_timesheet[d.day - 1].hours <= expected_hours_per_day:
                        if monthly_timesheet[d.day - 1].hours + project_worked_days[project_worked_days_index] == expected_hours_per_day:
                            monthly_timesheet[d.day - 1].hours += project_worked_days[project_worked_days_index]
                            p_ts[d.day - 1] = project_worked_days[project_worked_days_index]
                            project_worked_days_index += 1
                            current_day_index += 1
                        elif monthly_timesheet[d.day - 1].hours + project_worked_days[project_worked_days_index] < expected_hours_per_day:
                            monthly_timesheet[d.day - 1].hours += project_worked_days[project_worked_days_index]
                            p_ts[d.day - 1] = project_worked_days[project_worked_days_index]
                            project_worked_days_index += 1
                            current_day_index += 1
                            continue
                    elif monthly_timesheet[d.day - 1].hours + project_worked_days[project_worked_days_index] > expected_hours_per_day and fraction_timesheet_index:
                        diff_hour = expected_hours_per_day - monthly_timesheet[d.day - 1].hours
                        monthly_timesheet[d.day - 1].hours += diff_hour
                        project_worked_days[project_worked_days_index] -= diff_hour
                        if fraction_timesheet_index:
                            p_ts[fraction_timesheet_index] = diff_hour
                        fraction_timesheet_index = None
                else:
                    monthly_timesheet[d.day - 1].hours += project_worked_days[project_worked_days_index]
                    if monthly_timesheet[d.day - 1].hours != expected_hours_per_day:
                        # current project day timesheet is a fraction entry. We need to mark it to get back here
                        fraction_timesheet_index = d.day - 1
                    p_ts[d.day - 1] = project_worked_days[project_worked_days_index]
                    project_worked_days_index += 1
                    current_day_index += 1
            ts.append(p_ts)

        return ts
