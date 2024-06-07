#!/usr/bin/python3
"""Acts as storage for staff data in excel file"""
import pandas as pd
from staff import Staff
from project import Project
from datetime import datetime


class ExcelStorage():
    """ Staff excel adapter storage engine"""
    def __init__(self, path: str):
        self.path = path
        self._data = {}
        self._df = pd.read_excel(path, header=2)
        self._load()

    def all(self):
        return self._data

    def get_staff_by_name(self, name: str):
        """Get single staff object by staff name"""
        return self._data[name]

    def get_staffs_by_location(self, location: str):
        """Return list of all in staffs in the same location"""
        return [staff for staff in  self_data.values() if staff.location == location]

    def _load(self):
        """Load staff data from excell file"""
        if not self._data:
            col_names = self._df.columns.ravel()
            # Use first record to get project columns
            project_codes = col_names[2: len(self._df.loc[0])-1]
            coltypes = {p_name: float for p_name in project_codes}
            df = pd.read_excel(self.path, header=2, dtype=coltypes)
            for i in range(0, len(df)):
                row = df.loc[i]
                name, position = row["Row Labels"].split("_")
                staff = Staff(name, position, row["Location"])
                staff.projects = self._get_staff_projects(i, df)
                self._data[staff.name] = staff
                self._df = df

        

    def _get_staff_projects(self, index, df):
        """ Return of staff user projects allocation from excel"""
        col_names = df.columns.ravel()
        project_codes = col_names[2: len(df.loc[index])-1]
        projects = []
        for project_code in project_codes:
            project = Project(code=project_code, salary_allocation=round(
                df.loc[index][project_code], 2))
            project.set_start_date(datetime.now())
            projects.append(project)
        return projects
