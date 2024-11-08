import csv
import pprint
import random
def main():
    data = []
    try:
        with open('records.csv', "r") as myFile:
            # read the headers
            headers = myFile.readline().strip().split(",")

            #iterate over each remaining line in the file
            for row in myFile:
                # split the row by commas to get individual columns
                columns = row.strip().split(",")
                
                # create a dictionary for the current row, mapping headers to values
                csv_row = {headers[i]: columns[i] for i in range(len(headers))}

                #apend the dictionary to the data list
                data.append(csv_row)
    except:
        print("invalid data")
    # pprint.pprint(data)
    grouped_dict_data ={} # temporary dictionary to store data by group number
    
    for student in data:
        group_number = student["Tutorial Group"]
        
        if group_number not in grouped_dict_data:
            grouped_dict_data[group_number] = [] # create a new list if group number has not been initialised
            
        grouped_dict_data[group_number].append(student) # append student into his/her respective group

    experiments = {} # dictionary to hold our 10 runs 
    i = 0
    while i < 10:
        tut_grps_list = list(grouped_dict_data.values()) # list (cohort) of list (grp) of dictionaries (students)
        for tut_grp in tut_grps_list:
            random.shuffle(tut_grp)
        assigned_cohort = distribute_By_Diversity(tut_grps_list) # list (cohort) of list (grp) of list (subgrp) of dictionaries (students)
        average_diversity_of_experiment = get_Average_Diversity(assigned_cohort)
        experiments[i]={"assigned_cohort": assigned_cohort, "average_diversity": average_diversity_of_experiment}

    optimum_assignment=experiments[0] #initialise optimum_assignment with the first experiment

    for experiment in experiments.values(): #iterate over experiments to find the one with the highest average diversity
        if optimum_assignment["average_diversity"] < experiment["average_diversity"]:
            optimum_assignment=experiment 
        
    for experiment in experiments:
        if optimum_assignment["average_diversity"] < experiment["average_diversity"]:
            optimum_assignment["average_diversity"] = experiment["average_diversity"]
            optimum_assignment["assigned_cohort"] = experiment["assigned_cohort"]

    filename = "FDAB_Team2.csv"

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
    
        # Write header
        writer.writerow(['CGPA', 'Gender', 'Name', 'School', 'Student ID', 'Tutorial Group', 'Team Assigned'])
    
        # Flatten and write rows
        for tut_grp_list in optimum_assignment["assigned_cohort"]:
            for assigned_cohort in tut_grp_list:
                for entry in assigned_cohort:
                    # Assuming each entry is a dictionary
                    writer.writerow(entry['Tutorial Group'], entry['Student ID'], entry['School'], entry['Name'], entry['Gender'], entry['CGPA'], entry['Team Assigned','N/A'])   
def distribute_By_Diversity(groups):
    assigned_tut_grps_list = function_to_assign_students(groups) # returns a list of tut grps with assigned subgrps, but not sorted by best diversity
    return assigned_tut_grps_list # list (cohort) of list (grp) of list (subgrp) of dictionaries (students)
def get_Average_Diversity(cohort):
    tutgrp_dscore_list = []
    print(len(cohort))
    for tut_grp in cohort:
        print(len(tut_grp))
        subgrp_dscore_list =[]
        for sub_grp in tut_grp:
            subgrp_dscore = get_Diversity_Score(sub_grp)
            subgrp_dscore_list.append(subgrp_dscore)
        average_tutgrp_dscore = sum(subgrp_dscore_list)/ len(subgrp_dscore_list)
        tutgrp_dscore_list.append(average_tutgrp_dscore)
    average_cohort_dscore = sum(tutgrp_dscore_list)/ len(tutgrp_dscore_list)
    return average_cohort_dscore
def get_Diversity_Score(group:list):
    numStudents = len(group)
    numMales = len([student for student in group if student["Gender"]=="Male"])
    schoolCount = {
        "CCDS": len([student for student in group if student["School"]=="CCDS"]),
        "EEE": len([student for student in group if student["School"]=="EEE"]),
        "CoB (NBS)": len([student for student in group if student["School"]=="CoB (NBS)"]),
        "SoH": len([student for student in group if student["School"]=="SoH"]),
        "WKW SCI": len([student for student in group if student["School"]=="WKW SCI"]),
        "CoE": len([student for student in group if student["School"]=="CoE"]),
        "MAE": len([student for student in group if student["School"]=="MAE"]),
        "SPMS": len([student for student in group if student["School"]=="SPMS"]),
        "SBS": len([student for student in group if student["School"]=="SBS"]),
        "SSS": len([student for student in group if student["School"]=="SSS"]),
        "ASE": len([student for student in group if student["School"]=="ASE"]),
        "NIE": len([student for student in group if student["School"]=="NIE"]),
        "ADM": len([student for student in group if student["School"]=="ADM"]),
        "CCEB": len([student for student in group if student["School"]=="CCEB"]),
        "MSE": len([student for student in group if student["School"]=="MSE"]),
        "LKCMedicine": len([student for student in group if student["School"]=="LKCMedicine"]),
        "CEE": len([student for student in group if student["School"]=="CEE"]),
        "HASS": len([student for student in group if student["School"]=="HASS"]),
    }
    
    # CGPA Diversity
    minCgpa = 3.7
    averageCgpaSubGroup = sum(float(student["CGPA"]) for student in group)/numStudents
    averageCgpa = 4.335
    cgpaDiversity = 1 - abs((1/(averageCgpa - minCgpa)) * (averageCgpaSubGroup - averageCgpa)) # Inverse lerp function to calculate how far cgpa is from average

    # Gender Diversity
    genderDiversity = 1 - 2 * abs((numMales / numStudents) - 0.5) # Simple inverse lerp function to calculate gender diversity (0 to 1)

    # School Diversity
    # Proportions of students from each school
    proportions = [count / numStudents for count in schoolCount.values()]

    # Simpson's Diversity Index -> Diversity = 1 - sum of all p^2, where p is proportions
    schoolDiversity = 1 - sum(p ** 2 for p in proportions)

    # Return overall diversity (simple average) -> returns a percentage
    # print(((genderDiversity + cgpaDiversity + schoolDiversity)/3) * 100)
    return ((genderDiversity + cgpaDiversity + schoolDiversity)/3) * 100
def function_to_assign_students(groups):
    #initialise an empty list to store all assigned teams for each of all tutorial groups 
    assigned_tut_grps_list = [] 
    
    for group in groups:
        initial_teams = [[] for _ in range(10)] #initiate 10 empty lists, one for each team in each tutorial group

        for student in group:
            best_team = None #store the best team with highest diversity score after adding the student
            best_team_score = float('-inf') #Higher score indicate better diversity. This stores the highest diversity score so far
            
            #shuffle teams to avoid consistent order
            random.shuffle(initial_teams)
           
            for team in initial_teams:
                if len(team) < 5:  # Only consider teams that are not full
                    #Temporarily add the student to the team
                    team.append(student)
                
                    # Use the defined diversity score function, Calculate team diversity score if student is in the team
                    score = get_Diversity_Score(team) + random.uniform(0,0.01) #add slight randomness
                    team.pop() #Remove student after calculating diversity score 

                    # Choose the team with the Highest diversity score
                    if score > best_team_score:
                        best_team_score = score
                        best_team = team
            if best_team is not None:
                best_team.append(student)
            else:
                print("Warning: No available team for student", student)
            
            # Add the student to the chosen best team
            best_team.append(student)

        assigned_tut_grps_list.append(initial_teams)
    # pprint.pprint(assigned_tut_grps_list)
    return assigned_tut_grps_list
if __name__ == "__main__":
    main()

