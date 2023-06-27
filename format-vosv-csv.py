import csv, sys
from strsimpy.overlap_coefficient import OverlapCoefficient

# Create blank lists for each column from csv file
id = []
organization = []
documents = []
citations = []
totallinkstrength = []

# Set the similarity score
similarity = float(input("Enter the similarity score (0-1): "))
infile = sys.argv[1]
outfile = sys.argv[2]


# Try to read the file
try:
    with open(infile, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        data = list(reader)

        # Create blank list for each column
        for col_name in data[0]:
            col_name = col_name.replace(" ","")
            exec(col_name + " = []")

        # Populate each column with the data from the CSV file
        for row in data[1:]:
            id.append(row[0])
            organization.append(row[1])
            documents.append(row[2])
            citations.append(row[3])
            totallinkstrength.append(row[4])

# If the file cannot be opened, print an error message
except IOError:
    print("Could not open file. Please make sure the file is in the same directory as this script or the file is following the right naming convention.")
    
# filter out the organizations that have high likeness score using sorensen-dice
duplicateID = []
duplicateID2 = []
duplicateOrg = []
duplicateDoc = []
duplicateCit = []
duplicateTLS = []

hitFlag = False

# check if the id is in the duplicateID list
def checkDuplicateList(id_j, id_list):
    for i in range(len(id_list)):
        for j in id_list[i].split(', '):
            if int(j) == int(id_j):
                return i
    return -1

# compare the organization to the duplicateOrg list
def checkDuplicateOrg(org_i, org_list, i):
    for n in range(len(org_list)):
        if s.distance(org_i, org_list[n]) < similarity:
            # if already in the collection of duplicate organizations, skip
            if str(id[i]) in duplicateID[n].split(", "):
                return i
            # if organization is similar, concatenate the id to the duplicateID list
            duplicateID[n] = str(duplicateID[n]) + ', ' + str(id[i])
            duplicateID2[n] = str(duplicateID2[n]) + ', ' + str(id[i])
            duplicateDoc[n] = int(duplicateDoc[n]) + int(documents[i])
            duplicateCit[n] = int(duplicateCit[n]) + int(citations[i])
            duplicateTLS[n] = int(duplicateTLS[n]) + int(totallinkstrength[i])
            print(org_i, "\n", org_list[n], "\n\n", duplicateID[n], "\n\n", "updated a duplicate")
            print()
            return i
    return -1

# Compare each organization to every other organization
s = OverlapCoefficient()

for i in range(len(id)):
    print("Comparing", id[i], "to the rest of the organizations...")
    hitFlag = False
    for j in range(i, len(id)):
        x = checkDuplicateList(id[j], duplicateID)
        if x != -1:
            hitFlag = True
            continue
        # check if the organization is already in the duplicateOrg list
        # this needs to be here because the duplicateOrg list is updated in the checkDuplicateOrg function
        # if the organization is already in the duplicateOrg list, skip
        y = checkDuplicateOrg(organization[i], duplicateOrg, i)
        if y != -1:
            hitFlag = True
            continue
        # if the organization is the same, skip
        if i == j or id[i] == id[j]:
            continue
        # if reached the end of the list, add the organization to the dictionary
        if j == len(id) - 1:
            # add the organization to the dictionary with the id as the key
            # add the sum of the documents, citations, and total link strength to the dictionary with the id as the key
            duplicateID.append(id[i])
            duplicateID2.append(id[i])
            duplicateOrg.append(organization[i])
            duplicateDoc.append(documents[i])
            duplicateCit.append(citations[i])
            duplicateTLS.append(totallinkstrength[i])
            print(organization[i], "\n\n", id[i], "\n\n", "added without duplicate")
            print()
        else:
            # if the organization is not the same, check for similarity
            if s.distance(organization[i], organization[j]) < similarity:
                hitFlag = True
                if documents[i] == documents[j] and citations[i] == citations[j] and totallinkstrength[i] == totallinkstrength[j]:
                    # if similar but similar in all columns, skip
                    # add the organization to the dictionary with the id as the key
                    # only copy the columns of the organization at index i
                    duplicateID.append(str(id[i]) + ', ' + str(id[j]))
                    duplicateID2.append(id[j])
                    duplicateOrg.append(organization[i])
                    duplicateDoc.append(documents[i])
                    duplicateCit.append(citations[i])
                    duplicateTLS.append(totallinkstrength[i])
                else:
                    # if the organization is similar, add to dictionary
                    # add the organization to the dictionary with the id as the key
                    # add the sum of the documents, citations, and total link strength to the dictionary with the id as the key
                    if len(organization[i]) <= len(organization[j]):
                        # append the values to each list
                        duplicateID.append(str(id[i]) + ', ' + str(id[j]))
                        duplicateID2.append(id[j])
                        duplicateOrg.append(organization[i])
                        duplicateDoc.append(int(documents[i]) + int(documents[j]))
                        duplicateCit.append(int(citations[i]) + int(citations[j]))
                        duplicateTLS.append(int(totallinkstrength[i]) + int(totallinkstrength[j]))
                    else:
                        duplicateID.append(str(id[i]) + ', ' + str(id[j]))
                        duplicateID2.append(id[i])
                        duplicateOrg.append(organization[j])
                        duplicateDoc.append(int(documents[i]) + int(documents[j]))
                        duplicateCit.append(int(citations[i]) + int(citations[j]))
                        duplicateTLS.append(int(totallinkstrength[i]) + int(totallinkstrength[j]))

                print(organization[i], "\n", organization[j], "\n\n", id[i], id[j], "\n\n", s.distance(organization[i], organization[j]))
                print()
            else:
                # if not similar, skip
                continue

# Write the data to a new CSV file
try:
    with open(outfile, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Organization", "Documents", "Citations", "Total Link Strength"])
        for i in range(len(duplicateID)):
            print(duplicateID[i], duplicateOrg[i], duplicateDoc[i], duplicateCit[i], duplicateTLS[i])
            writer.writerow([duplicateID[i], duplicateOrg[i], duplicateDoc[i], duplicateCit[i], duplicateTLS[i]])
        print("File successfully written.")

# If the file cannot be opened, print an error message
except IOError:
    print("Could not open file. Please make sure the file is in the same directory as this script.")


