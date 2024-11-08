import random

# Custom function to read CSV and group students by tutorial group
def read_and_group_students(file_path):
    tutorial_groups = {}
    
    # Read the file and group by Tutorial Group
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip header
        
        for line in lines:
            data = line.strip().split(',')
            tutorial_group = data[0]
            student_id = data[1]
            school = data[2]
            name = data[3]
            gender = data[4]
            cgpa = float(data[5])
            
            student = {'ID': student_id, 'School': school, 'Name': name, 'Gender': gender, 'CGPA': cgpa}
            
            if tutorial_group not in tutorial_groups:
                tutorial_groups[tutorial_group] = []
            
            tutorial_groups[tutorial_group].append(student)
    
    return tutorial_groups

# Function to form diverse teams from a list of students
def form_teams(students):
    teams = []
    random.shuffle(students)  # Shuffle students to avoid bias
    
    while len(students) >= 5:
        team = []
        while len(team) < 5:
            student = students.pop(0)
            team.append(student)
        
        # Ensure the team meets the diversity criteria
        if validate_team(team):
            teams.append(team)
        else:
            # If not valid, reshuffle
            students.extend(team)
            random.shuffle(students)
    
    # Handle leftover students (if any)
    if students:
        teams.append(students)
    
    return teams

# Function to validate team diversity (School, Gender, CGPA)
def validate_team(team):
    schools = [student['School'] for student in team]
    genders = [student['Gender'] for student in team]
    cgpas = [student['CGPA'] for student in team]
    
    # Check school diversity (limit to a maximum of 2 from the same school)
    if max(schools.count(school) for school in schools) > 2:
        return False
    
    # Check gender diversity (limit to a maximum of 2 of the same gender)
    if max(genders.count(gender) for gender in genders) > 2:
        return False
    
    # Check CGPA diversity (ensure CGPA spread isn't too large)
    if max(cgpas) - min(cgpas) > 1.0:  # Adjust the threshold as needed
        return False
    
    return True

# Main function to organize students into diverse teams
def organize_teams(file_path):
    tutorial_groups = read_and_group_students(file_path)
    
    all_teams = {}
    
    for tutorial_group, students in tutorial_groups.items():
        teams = form_teams(students)
        all_teams[tutorial_group] = teams
    
    return all_teams

# Output the results
def print_teams(teams):
    for group, team_list in teams.items():
        print(f"\nTutorial Group: {group}")
        for i, team in enumerate(team_list):
            print(f" Team {i + 1}:")
            for student in team:
                print(f"   {student['ID']} - {student['Name']} - {student['School']} - {student['Gender']} - CGPA: {student['CGPA']}")
                
# Path to the file
file_path = '/mnt/data/records (2).csv'

# Organize and print teams
teams = organize_teams(file_path)
print_teams(teams)
c
