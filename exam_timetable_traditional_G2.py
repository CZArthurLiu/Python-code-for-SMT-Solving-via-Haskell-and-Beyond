import time
from collections import deque


class Student:
    def __init__(self, name, course):
        self.name = name
        self.course = course


class Room:
    def __init__(self, id, availability):
        self.id = id
        self.availability = availability


class Exam:
    def __init__(self, course,number):
        self.course = course
        self.number = number
        self.room = None
        self.day = None
        self.slot = None
    def printexam(self):
        exam_info = f"Course: {self.course}\nNumber: {self.number}\nRoom: {self.room}\nDay: {self.day}\nSlot: {self.slot}\n"
        print(exam_info)

# hard constraint check
def hard_constraint_check(state, student, room, courses):
    room_set = {}
    for r in room:
        room_set[r.id] = set()
    for course in courses:
        cur_exam = state[course]
        if cur_exam.room is not None:
            if cur_exam.number > room[cur_exam.room - 1].availability:
                return False
            time_slot = cur_exam.day * 10 + cur_exam.slot
            if time_slot in room_set[cur_exam.room]:
                return False
            room_set[cur_exam.room].add(time_slot)
    for cur_student in student:
        cur_set = set()
        course = cur_student.course
        for cur_course in course:
            if state[cur_course].day is not None:
                time = state[cur_course].day * 10 + state[cur_course].slot
                if time in cur_set:
                    return False
                cur_set.add(time)
    return True


if __name__ == '__main__':
    #init room
    room = []
    with open("room.txt", "r") as file:
        for line in file:
            # Split each line into two nodes
            pair = line.strip().split()
            room.append(Room(int(pair[0]),int(pair[1])))
    #init stu
    stu = []
    with open("student.txt", "r") as file:
        for line in file:
            # Split each line into two nodes
            pair = line.strip().split()
            temp_stu = Student(pair[0],pair[1:])
            stu.append(temp_stu)
    #init exam
    exam = {}
    course =[]
    with open("exam.txt", "r") as file:
        for line in file:
            # Split each line into two nodes
            pair = line.strip().split()
            temp_stu = Exam(pair[0],int(pair[1]))
            exam[pair[0]] = temp_stu
            course.append(pair[0])
    queue = deque()
    start_time = time.time()
    # init state
    for r in room:
        for i in range(len(exam)):
            temp_exam = {}
            for j in range(len(exam)):
                cur_exam = exam.get(course[j])
                temp = Exam(cur_exam.course,cur_exam.number)
                if i == j:
                    temp.day = 1
                    temp.slot = 1
                    temp.room = r.id
                temp_exam[course[j]] = temp
            queue.append(temp_exam)
    flag = False
    cnt = 0
    # find solution
    while len(queue) > 0:
        cur_exam = queue.popleft()
        cnt += 1
        if not hard_constraint_check(cur_exam,stu,room,course):
            continue
        cur = 0
        for c in course:
            if cur_exam[c].room is not None:
                cur += 1
        if cur == 4:
            for c in course:
                cur_exam[c].printexam()
            flag = True
            break
        for r in room:
            for i in range(len(cur_exam)):
                temp_exam = {}
                flag_2 = True
                for j in range(len(cur_exam)):
                    exam = cur_exam.get(course[j])
                    temp = Exam(exam.course, exam.number)
                    temp.room = exam.room
                    temp.day = exam.day
                    temp.slot = exam.slot
                    if i == j:
                        temp.room = r.id
                        if exam.day is None:
                            temp.day = 1
                            temp.slot = 1
                        else:
                            if exam.slot < 3:
                                temp.day = exam.day
                                temp.slot = exam.slot + 1
                            else:
                                if exam.day < 3:
                                    temp.day = exam.day + 1
                                    temp.slot = 1
                                else:
                                    flag_2 = False
                                    break
                    temp_exam[course[j]] = temp
                if flag_2:
                    queue.append(temp_exam)
    end_time = time.time()
    if not flag:
        print("find no solution")
    else:
        print(f"traditional G2 method find solution via {cnt} search process")
    print(f"the running time for traditional G2 method: {end_time - start_time} ")

