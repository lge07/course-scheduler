from __future__ import annotations
from typing import TYPE_CHECKING, List
from pulp import LpVariable, LpAffineExpression, value
from .schedule import Schedule
from .course import CourseType, Section
from utils import summation
from .individual import Individual
if TYPE_CHECKING:
    from .course import Course
class Teacher(Individual):
    def __init__(self, tag: int, allCourses: List[str], qualifications: List[str], openPeriods: list):
        super().__init__(tag, allCourses)
        self.qualifications = qualifications
        self.openPeriods = openPeriods
    
    def isQualified(self, courseCode: str) -> bool:
        """
        Returns whether a teacher is qualified for a particular courseCode.
        """
        
        return (courseCode in self.qualifications)
    
    def getOpenPeriods(self) -> List[int]:
        """
        Returns open periods numbers.
        """

        return self.openPeriods
    
    def isOpen(self, period: int) -> bool:
        """
        Returns whether a particular period is open.
        """

        return (period in self.openPeriods)

    def addSection(self, newSection: Section):
        """
        Adds a section to the schedule.
        """

        res = self.schedule.addSection(newSection)
        if res:
            self.openPeriods.remove(newSection.period)
            self.addToSection(newSection)
    
    def removeSection(self, section: Section):
        """
        Removes a section from the schedule.
        """

        self.schedule.removeSection(section)
        section.instructor = None
        self.openPeriods.append(section.period)
        self.openPeriods.sort()
    
    def getQualified(self):
        """
        Yields whether or not teacher is qualified for each class teaching.
        """

        currScheduleVals = list(self.schedule.getSections().values())
        for section in currScheduleVals:
            yield (section == None or self.isQualified(section.courseCode))
    
    def getQualificationVector(self) -> List[int]:
        """
        Returns (eager) of the teacher's qualifications
        """
        vector = [0] * len(self.allCourses)
        for course in self.qualifications:
            index = self.allCourses.index(course)
            vector[index] = 1

        return vector
    
    def getConstraints(self, allCourses: List[str]):
        """
        Yields constraints determining whether a teacher is qualified for a specific course.
        """
        
        for course in allCourses:
            isQualified = 0
            if course.courseCode in self.qualifications: 
                isQualified = 1
            
            ret = []
            for period in self.schedule.lpVars.keys():
                variable = self.schedule.lpVars[period][int(course.courseCode)]
                assert isinstance(variable, LpVariable)
                ret.append(variable)
            sum_of_ret = summation(ret)

            assert isinstance(sum_of_ret, LpAffineExpression)
            assert isinstance(sum_of_ret == isQualified, LpAffineExpression)

            yield (sum_of_ret <= isQualified)
    
    def addToSection(self, section: Section):
        section.changeInstructor(self)
    
    def getOpenScore(self) -> int:
        """
        Returns number of off periods
        """
        return len(self.openPeriods)

