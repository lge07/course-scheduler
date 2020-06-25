from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum
from utils import summation
if TYPE_CHECKING:
    from individual import Teacher, Student, Individual
    from schedule import Schedule


# Defines classes relating to courses and sections.
# Courses represent an unscheduled verion of a generic class containing information regarding how it might be structured
# Section represents a scheduled version of a generic class containing information about the specific scheduled instance.

class CourseType(Enum):
    CORE = 0
    ELECTIVE = 1
    OFF = 2

class Course:
    def __init__(self, courseCode: str, courseType: CourseType):
        self.courseCode = courseCode
        self.qualifiedTeachers = []
        self.potentialPeriods = []
        self.reqTotalStudents = 0
        self.courseType = courseType


    def __eq__(self, other) -> bool:
        """
        Tests whether Course is equivalent to other Course.

        __eq__ allows for use within ==, remove from list, etc.
        """
        if isinstance(other, Course):
            return self.courseCode == other.courseCode
        return False
    
    def addReqStudent(self):
        """
        Adds 1 student to number who want to take the class.
        """
        self.reqTotalStudents += 1
    
    def addTeacher(self, teacher: Teacher):
        """
        Adds a teacher object to the list of qualified teachers and updates list of potential periods
        """
        if teacher.isQualified(self.courseCode):
            self.qualifiedTeachers.append(teacher)
            for period in teacher.openPeriods:
                if period not in self.potentialPeriods:
                    self.potentialPeriods.append(period)
    
    def getCourseCode(self) -> str:
        """
        Get course code.
        """
        return self.courseCode
    
    def getTeachers(self) -> list:
        """
        Get teachers qualified to teach class.
        """
        return self.qualifiedTeachers
    
    def getpotentialPeriods(self) -> list:
        """
        Get potential periods for class to occur.
        """
        return self.potentialPeriods
    
    def getReqStudents(self) -> int:
        """
        Get number of students interested in the class.
        """
        return self.reqTotalStudents
    
    def getCourseType(self) -> CourseType:
        """
        Get the course type.
        """
        return self.courseType

    def newSection(self) -> Section:
        """
        Create a new section of a class.
        """
        return Section(self.courseCode, self.courseType)
    
    def removeTeacher(self, teacher: Teacher):
        """
        Remove a teacher from the list of qualified teachers, reevaluate periods.
        """
        self.qualifiedTeachers.remove(teacher)
        self.potentialPeriods = []
        for teacher in self.qualifiedTeachers:
            for period in teacher.openPeriods:
                if period not in self.potentialPeriods:
                    self.potentialPeriods.append(period)
    
    def removeReqStudent(self):
        """
        Remove 1 interested student.
        """
        self.reqTotalStudents -= 1

class Section:
    def __init__(self, courseCode: str, courseType: CourseType):
        self.courseCode = courseCode
        self.courseType = courseType
        self.instructor = None
        self.period = -1
        self.students = []

    def __str__(self) -> str:
        """
        Return string representation of Section
        """
        ret = "CourseCode: " + self.courseCode
        ret += "\n of type: " + str(self.courseType.name)
        ret += "\n with teacher: " + self.instructor.tag 
        ret += "\n in period: " + str(self.period)
        ret += "\n with students: " + str([stu.tag for stu in self.students])
        return ret

    def __eq__(self, other) -> bool:
        """
        Returns whether a Section is the same as another, excluding students.
        """
        if isinstance(other, Section):
            codeCorrect = (self.courseCode == other.courseCode)
            instructorCorrect = (self.instructor == other.instructor)
            courseTypeCorrect = (self.courseType == other.courseType)
            periodCorrect = (self.period == other.period)
            return (codeCorrect and instructorCorrect and courseTypeCorrect and periodCorrect)
        return False

    def sameBaseCourse(self, other: Section):
        """
        Returns whether the course code is the same as another Section.
        """
        return self.courseCode == other.courseCode

    def changeInstructor(self, teacher: Teacher):
        """
        Changes or adds (depending on whether instructor is None currently) the instructor.
        """
        self.instructor = teacher

    def changePeriod(self, period: int):
        """
        Changes or adds (depending on whether period is -1 currently) the period.
        """
        self.period = period
    
    def addStudent(self, student: Student):
        """
        Adds a student to the list.
        """
        if not self.isTaking(student):
            self.students.append(student)

    def getCourseCode(self) -> str:
        """
        Gets course code
        """
        return self.courseCode
    
    def getCourseType(self) -> CourseType:
        """
        Gets course type
        """
        return self.courseType

    def getInstructor(self) -> Teacher:
        """
        Gets instructor
        """
        return self.instructor
    
    def getPeriod(self) -> int:
        """
        Gets period
        """
        return self.period
    
    def getStudents(self) -> list:
        """
        Gets all students currently scheduled for Section.
        """
        return self.students
    
    def getStudentCount(self) -> int:
        """
        Gets total number of participating students.
        """
        return len(self.students)
    
    def isTaking(self, student: Student) -> bool:
        """
        Returns whether a student is taking the class.
        """
        return (student in self.students)
    
    def removeStudent(self, student: Student):
        """
        Removes a student from the class.
        """
        if self.isTaking(student):
            self.students.remove(student)
    
    def isValid(self):
        """
        Returns whether the Section is at least "valid" (all data types populated)
        """
        instructorValid = (self.instructor != None) and (self.instructor.isQualified(self.courseCode))
        # TODO: Add checks to make sure that two classes aren't at the same time?
        # TODO: If the Teacher instance makes changes to the root Teacher instance, it's easy.
        periodValid = (self.period != -1)
        studentsValid = (len(self.students) > 0)
        return (instructorValid and periodValid and studentsValid)

