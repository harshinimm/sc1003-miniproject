import csv
import random
def read_csv(file_path):
    students=[]
    with open(file_path,mode='r') as file:
        reader=csv.DictReader(file)
        for row in reader:
            students.append({'name':row['name'],'cgpa': float(row['cgpa']),  'gender': row['gender'],'major': row['major']})
    return students
def group_students(students,num_groups, max_major_count=2, max_gpa_diff=1.0,group_size=5):
    groups = [[] for _ in range(num_groups)]
    gender_count=[{'male':0,'female':0} for _ in range(num_groups)]
    major_count = [{'major': {}} for _ in range(num_groups)]
    gpa_count = [{'gpa': []} for _ in range(num_groups)]
    random.shuffle(students)
    for student in students:
        assigned = False
        for i in range(num_groups):
            gender = student['Gender'].lower()
            major = student['Major']
            gpa = student['GPA']
            if len(teams[i]) >= group_size:
                continue
            if gender_count[i][gender] >= 3:
                continue
            if major in major_count[i][major] and major_count[i][major] >= max_major_count:
                continue
            if max(gpa_count[i]['gpa']) - min(gpa_count[i]['gpa']) > max_gpa_diff:
                continue
            gender_count[i][gender] += 1
            major_count[i][major] = major_count[i].get(major, 0) + 1
            gpa_count[i]['gpa'].append(gpa)
            teams[i].append(student)
            assigned = True
            break
        if not assigned:
            group.append([student])
       return groups

students = read_csv('record.csv') 
num_groups = 100
groups = group_students(students, num_groups)
for group in groups:
    print(f"Group {i + 1}:")
    for student in group:
        print(f"  {student['name']} ({student['gender']}, GPA: {student['cgpa']}, Major: {student['major']})")
    print()
    
    

