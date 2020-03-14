class DraftResults(object):
    def __init__(self):
        self.rankings = []

    # add a ranking for a strategy
    def AddDraftRanking(self, strategyName, ranking):
        pair = (strategyName, ranking)
        self.rankings.append(pair)

    # merge a DraftResults object into another
    def AddDraftRankings(self, draftResults):
        for result in draftResults.rankings:
            self.AddDraftRanking(result[0], result[1])

    def GetAverageDraftRanking(self, strategyName):
        totalRankingsForStrategy = 0
        numberOfStrategyInstances = 0

        for ranking in self.rankings:
            if (ranking[0] == strategyName):
                totalRankingsForStrategy += ranking[1]
                numberOfStrategyInstances += 1

        return totalRankingsForStrategy / numberOfStrategyInstances