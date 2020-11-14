#!/usr/bin/python


def score(vectorModel, docList, queryTermsList):
    docScores = []
    for doc in docList:
        currentDoc = [doc, 0]
        for term in queryTermsList:
            if (doc, term) in vectorModel:
                currentDoc[1] += vectorModel[doc, term]
        insertDocScoreSorted(docScores, currentDoc)
    return docScores


def insertDocScoreSorted(docScoresList, newScore):
    for i in range(0, docScoresList.__len__()):
        if docScoresList[i][1] < newScore[1]:
            docScoresList.insert(i, newScore)
            return
    docScoresList.append(newScore)


def generateRuns(queryName, staffName, docScoresList):
    f = open("runs/run_" + staffName + ".txt", "w")
    rank = 1
    path = "/article[1]"
    coef = 1 / docScoresList[0][1]
    runs = ""
    for docScore in docScoresList:
        # currentRun = queryName + "Q0" + docScore[0] * coef + docScore[1] + staffName + path
        currentRun = f'{queryName} Q0 {docScore[0]} {rank} {str(docScore[1])} {staffName} {path}'
        runs += currentRun + "\n"
        rank += 1
    f.write(runs)
    f.close()


# vectorModel = {
#        ("doc1", "terme1"): 120,
#        ("doc1", "terme2"): 100,
#        ("doc2", "terme2"): 100,
#        ("doc3", "terme1"): 10,
#        ("doc3", "terme3"): 10
#    }
#
#    docList = ["doc1", "doc2", "doc3"]
#    queryTermsList = ["terme1", "terme2", "terme3"]
#
#    generateRuns("2010001", "BenoitGauthierGuillaumeTheo", score(vectorModel, docList, queryTermsList))
