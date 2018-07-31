import sys
import csv

#TODO: Ask about expectations for setting in/out filenames
#relative path? or sys.argv?
pollingcsv = "election_data.csv"
analysistxt = "polling_analysis.txt"

with open(pollingcsv, "r", newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    header = next(csvreader)

    #This function and the following function calls set the reference columns for the calculations
    #performed to generate the Financial Analysis
    def get_column(header, word):
        for columnID, columnName in enumerate(header):
            if columnName == word:
                return columnID
    
    search_word = 'Voter ID'
    voterColID = get_column(header, search_word)
    search_word = 'County'
    countyColID = get_column(header, search_word)
    search_word = 'Candidate'
    candidateColID = get_column(header, search_word)

    #The following conditionals set defaults for reference column IDs 
    #in case the header names are changed or do not match the original set names.
    if voterColID == None:
        voterColID = 0
        print(f'Warning! No header names matching "Voter ID" Column index set to "{voterColID}"\n')

    if countyColID == None:
        countyColID = 1
        print(f'Warning! No header names matching "County" Column index set to "{countyColID}"\n')

    if candidateColID == None:
        candidateColID = 2
        print(f'Warning! No header names matching "Candidate" Column index set to "{candidateColID}"\n')

    #Creates dictionary of candidates and vote count
    votesPerCandidate = {}
    voteCount = 0
    while True:
        try:
            line = next(csvreader)
        except StopIteration:
            break
        voteCount += 1
        candidateName = line[candidateColID]
        if candidateName in votesPerCandidate:
            votesPerCandidate[candidateName] += 1
        else:
            votesPerCandidate[candidateName] = 1

#Opens and overwrites/creates .txt for results
fileOut = open(analysistxt,"w")

#Function that simultaneously prints results to console and writes to file
def resultsLog(file, printContents):
    sys.stdout.write(printContents)
    file.write(printContents)

resultsLog(fileOut, "Election Results \n-------------------------\n")
resultsLog(fileOut, f"Total Votes: {voteCount} \n-------------------------\n")

#Prints the outcomes for each candidate including percent expressed in decimal rounded to 5 significant digits
for candidate in votesPerCandidate.keys():
    percentVotes = (votesPerCandidate[candidate] / voteCount) * 100
    resultsLog(fileOut, f"{candidate}: {percentVotes:.3f}% ({votesPerCandidate[candidate]})\n")

#Compares the number of votes for each candidate to find the candidate with the most votes
votes = 0
for candidate in votesPerCandidate:
    if votesPerCandidate[candidate] >= votes:
        votes = votesPerCandidate[candidate]
        winner = candidate
resultsLog(fileOut, f"-------------------------\nWinner: {winner}\n-------------------------\n")

#Closes the .txt where results were written   
fileOut.close() 

#TODO: figure out whether to include following lines based on lessons taught in week 4
#if __name__ == "__main__":
#    main()