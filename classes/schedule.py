from __future__ import annotations
from typing import TYPE_CHECKING
from copy import deepcopy
from pulp import LpVariable, LpAffineExpression
if TYPE_CHECKING:
    from course import CourseType, Course, Section
    from individual import Teacher, Student, Individual

# Class for storing the schedule associated with any sort of Individual. Uses a dictionary in order to prevent length overflows.
class Schedule:
    def __init__(self, tag: int, courseLength: int):
        self.sections = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
        self.lpVars = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
        self.tag = tag
        for index in self.lpVars.keys():
            ret = []
            for x in range(0, courseLength):
                name = "{TAG}_{INDEX}".format(TAG=str(self.tag), INDEX=str(index))
                newVar = LpVariable(name)
                ret.append(newVar)
            self.lpVars[index] = ret
    
    def __str__(self):
        ret = deepcopy(self.sections)
        for period in ret.keys():
            ret[period] = str(ret[period])
        return str(ret)

    def getOpenPeriods(self) -> list:
        """
        Returns list of open periods (ints).
        """
        ret = []
        for period in self.sections.keys():
            if self.section[period] == None:
                ret.append(period)
        return ret
    
    def getSections(self) -> dict:
        """
        Returns dict of current sections.
        """
        return self.sections
    
    def addSection(self, newSection: Section, pos: int) -> bool:
        """
        Adds a section at position pos. Does not work if the period is already filled. Returns True if successfully completed.
        """
        if self.sections[pos]==None and newSection not in self.sections.values():
            self.sections[pos] = newSection
            return True
        return False
    
    def removeSection(self, section: Section):
        """
        Removes a section by the Section object. Replaces with None.
        """
        if self.sections[section.period] == section:
            self.sections[section.period] = None

    def getValidityConstr(self):
        """
        Yields expressions of if periods have 0 or 1 class.
        """
        for period in self.sections.keys():
            section = self.sections[period]
            hasClass = 0
            if section.courseType!=Course.OFF: hasClass = 1
            yield (LpAffineExpression(self.lpVars[period]) <= hasClass)

    def haveTeachers(self):
        """
        Checks if all Sections have a qualified teacher.
        """
        ret = True
        for section in self.sections.values():
            if section.courseType != CourseType.OFF:
                yield ret == ret and section.isValid()
                # isValid checks teacher qualifications AND makes sure everything's right.
    
    
    
# https://github.com/henrymwestfall/course-scheduler
        