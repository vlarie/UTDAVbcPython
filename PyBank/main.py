import os
import sys
import pandas as pd 

# dataDirectory finds the filepath of the python script being run
dataDirectory = os.path.dirname(sys.argv[0])
budgetcsv = "budget_data.csv"
analysistxt = "financial_analysis.txt"
csvFilepath = os.path.join(dataDirectory, budgetcsv)
txtOutpath = os.path.join(dataDirectory, analysistxt)


try:
    budgetDF = pd.read_csv(csvFilepath)
    budgetDF.head()

    dateCol = budgetDF["Date"]
    totalMonths = dateCol.count()
    totalPL = budgetDF["Profit/Losses"].sum()

    # Creates a list for the changes in Profit/Losses
    # First value is established as None because there is no previous data to compare to
    # and the list needs to be the same length as other fields in order to append to dataframe
    changePL = [None, ]
    for i in range(1, totalMonths):
        column = budgetDF["Profit/Losses"]
        new = column[i]
        old = column[i - 1]
        changePL.append(new - old)
    
    # Adds a new column to the dataframe with the changePL list
    budgetDF["Changes in Profit/Losses"] = changePL
    # Establishes variable for Changes column
    changePLdfCol = budgetDF["Changes in Profit/Losses"]
    avgChange = (changePLdfCol.sum()) / (totalMonths - 1)

    # This loop gathers the greatest increase and decrease in changes
    # as well as the indexes for these values which will be used to look up the coordinating dates
    maxPLindex = 1
    maxPL = changePL[maxPLindex]
    minPLindex = 1
    minPL = changePL[minPLindex]
    for i in range(1, len(changePL)):
        if changePL[i] > maxPL:
            maxPL = changePL[i]
            maxPLindex = i
        elif changePL[i] < minPL:
            minPL = changePL[i]
            minPLindex = i

    # Uses indexes from the above loop in the Date         
    maxPLdate = dateCol[maxPLindex]
    minPLdate = dateCol[minPLindex]

    # This function reformats the date string to be a four digit year
    def reDate(date, index, insert):
        index = date.find(index)
        reDate = date[:index] + insert + date[index:]
        return reDate

    maxPLdate = reDate(maxPLdate, "1", "20")
    minPLdate = reDate(minPLdate, "1", "20")

#Provides a descriptive error with instruction for correcting if an error occurs when opening the infile
except FileNotFoundError:
    print(f'Please move {pollingcsv} to the same directory as the script.')
    exit(1)

#Opens and overwrites/creates .txt for results
fileOut = open(txtOutpath,"w")

#Function that simultaneously prints results to console and writes to file
def resultsLog(file, printContents):
    sys.stdout.write(printContents)
    file.write(printContents)

resultsLog(fileOut, "Financial Analysis \n----------------------------\n")
resultsLog(fileOut, f"Total Months: {totalMonths} \n-------------------------\n")
resultsLog(fileOut, f"Total: ${totalPL:,}\n")
resultsLog(fileOut, f"Average Change: ${avgChange:,.2f}\n")
resultsLog(fileOut, f"Greatest Increase in Profits: {maxPLdate} ${maxPL:,}\n")
resultsLog(fileOut, f"Greatest Decrease in Profits: {minPLdate} ${minPL:,}\n")