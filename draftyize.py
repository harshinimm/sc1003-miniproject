ls = []
with open('records.csv', 'r') as f:
    for index,line in enumerate(f):
        if index == 0:
            continue
        ls.append(line.strip('\n').split(','))
##reading the csv file and storing it in a list of lists

for i in range(len(ls)):
    ls[i].append(False)   ##adding a new element to each sublist, which will be used to keep track of whether the student has been assigned to a group or not

for tut in range(12):
    tutls = ls[tut*50:(tut+1)*50]
    tutls.sort(key=lambda x: x[5], reverse=True)     ##sorting the list of lists based on the 6th element (which is the gpa)
    groups = []
    gpagroups =[]
    schoolls = [[],[],[],[],[],[],[],[],[],[]] ##creating a list of 10 empty sublists, each representing the schools of students in each group
    genderls = [] ##creating a list representing the gender of students in each group
    for i in range(10):
        genderls.append({'Male':0,'Female':0}) ##initializing the genderls list with 0s for each group

    for i in range(10):
        gpagroups.append(tutls[i*5:(i+1)*5])      ##creating a list of 10 sublists, each containing 5 students, ranked by gpa

    for i in range(10):
        groups.append([gpagroups[i][0],gpagroups[9-i][4]])       ##creating a list of 10 pairs, each containing the top and bottom students in each group
        gpagroups[i][0][6] = True
        gpagroups[9-i][4][6] = True ##assigning the top and bottom students to their respective groups
        schoolls[i] = [gpagroups[i][0][2],gpagroups[9-i][4][2]] ##adding the schools of the top and bottom students to their respective groups in the schoolls list
        genderls[i][gpagroups[i][0][4]] += 1
        genderls[i][gpagroups[9-i][4][4]] += 1 ##updating the genderls list with the gender of the top and bottom students in each group
    j = 0
    i = 0
    rnum = 0 ## mark the number of the student needs to be replaced
    for i in range(10):
        Flag = False ## mark whether there is a student assigned to the tutorial group i or not
        for j in range(10):
            if not(schoolls[i].count(gpagroups[j][1][2]) > 2 or genderls[i][gpagroups[j][1][4]] == 3 or gpagroups[j][1][6] == True):
                groups[i].append(gpagroups[j][1])
                gpagroups[j][1][6] = True
                schoolls[i].append(gpagroups[j][1][2])
                genderls[i][gpagroups[j][1][4]] += 1
                Flag = True
                break
            if gpagroups[j][1][6] == False: ##if there is no student assigned to the tutorial group i, find a student from the other gpagroups to replace it
                rnum = j ##mark the number of the student needs to be replaced
                
        if not Flag:
            for k in range(10):
                if not(schoolls[i].count(gpagroups[k][2][2]) > 2 or genderls[i][gpagroups[k][2][4]] == 3 or gpagroups[k][2][6] == True):
                    gpagroups[rnum][1], gpagroups[k][2] = gpagroups[k][2], gpagroups[rnum][1]
                    groups[i].append(gpagroups[rnum][1])
                    gpagroups[rnum][1][6] = True
                    schoolls[i].append(gpagroups[rnum][1][2])
                    genderls[i][gpagroups[rnum][1][4]] += 1
                    break
                
    rnum = 0
    for i in range(10):
        Flag = False
        for j in range(10):
            if not(schoolls[i].count(gpagroups[9-j][3][2]) > 2 or genderls[i][gpagroups[9-j][3][4]] == 3 or gpagroups[9-j][3][6] == True):
                groups[i].append(gpagroups[9-j][3])
                gpagroups[9-j][3][6] = True
                schoolls[i].append(gpagroups[9-j][3][2])
                genderls[i][gpagroups[9-j][3][4]] += 1
                Flag = True
                break
            if gpagroups[9-j][3][6] == False:
                rnum = j ##mark the number of the student needs to be replaced
        if not Flag:
            for k in range(10):
                if not(schoolls[i].count(gpagroups[9-k][2][2]) > 2 or genderls[i][gpagroups[9-k][2][4]] == 3 or gpagroups[9-k][2][6] == True):
                    gpagroups[9-rnum][3], gpagroups[9-k][2] = gpagroups[9-k][2], gpagroups[9-rnum][3]
                    groups[i].append(gpagroups[9-rnum][3])
                    gpagroups[9-rnum][3][6] = True
                    schoolls[i].append(gpagroups[9-rnum][3][2])
                    genderls[i][gpagroups[9-rnum][3][4]] += 1
                    break
   
    for i in range(10):
        Flag = False
        for j in range(10):
            if not(schoolls[i].count(gpagroups[j][2][2]) > 2 or genderls[i][gpagroups[j][2][4]] == 3 or gpagroups[j][2][6] == True):
                groups[i].append(gpagroups[j][2])
                gpagroups[j][2][6] = True
                schoolls[i].append(gpagroups[j][2][2])
                genderls[i][gpagroups[j][2][4]] += 1
                Flag = True
                break
        if not Flag:
            for k in range(10):
                if not(schoolls[i].count(gpagroups[k][2][2]) > 3 or gpagroups[k][2][6] == True):
                    groups[i].append(gpagroups[k][2])
                    gpagroups[k][2][6] = True
                    schoolls[i].append(gpagroups[k][2][2])
                    genderls[i][gpagroups[k][2][4]] += 1
                    break
        
    print("TUTGroup",tut+1,":")
    for i in range(10):
        print("Group",i+1,":")
        sum = 0
        for student in groups[i]:
            print(student,sep='/n') ##printing the students in each group
            sum += float(student[5]) ##calculating the total gpa of the group
        print("Average GPA of Group",i+1,"is",round(sum/5,2)) ##printing the average gpa of the group


        # if len(groups[i]) < 5:
        #     print("Group",i+1,"is incomplete") ##printing a message if a group is incomplete
        # for j in range(5):
        #     if gpagroups[i][j][6] == False:
        #         print("Student",j+1,"is not assigned to a group") ##printing a message if a student is not assigned to a group
        #         print(gpagroups[i][j])
