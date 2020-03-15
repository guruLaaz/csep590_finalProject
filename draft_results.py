from collections import defaultdict, namedtuple


# class DraftResults(object):
#     def __init__(self):
#         self.rankings = []

#     # add a ranking for a strategy
#     def AddDraftRanking(self, strategyName, ranking):
#         pair = (strategyName, ranking)
#         self.rankings.append(pair)

#     # merge a DraftResults object into another
#     def AddDraftRankings(self, draftResults):
#         for result in draftResults.rankings:
#             self.AddDraftRanking(result[0], result[1])

#     def GetAverageDraftRanking(self, strategyName):
#         totalRankingsForStrategy = 0
#         numberOfStrategyInstances = 0

#         for ranking in self.rankings:
#             if (ranking[0] == strategyName):
#                 totalRankingsForStrategy += ranking[1]
#                 numberOfStrategyInstances += 1

#         return totalRankingsForStrategy / numberOfStrategyInstances


TrialResult = namedtuple('TrialResult', 'year strategy_name value rank draft_pos')


class DraftResults(object):

    def __init__(self):
        self.results = []

    def add_trials(self, trials: TrialResult):
        self.results.extend(trials)

    def summary_by_strategy(self):
        ranks_per_strategy = defaultdict(list)
        rank_diffs_per_strategy = defaultdict(list)
        vals_per_strategy = defaultdict(list)

        for trial_result in self.results:
            ranks_per_strategy[trial_result.strategy_name].append(trial_result.rank)
            rank_diffs_per_strategy[trial_result.strategy_name].append(trial_result.rank - trial_result.draft_pos)
            vals_per_strategy[trial_result.strategy_name].append(trial_result.value)

        def average_and_rank(data, descending=False):
            averages = []
            for strategy_name, data_pts in data.items():
                averages.append((strategy_name, sum(data_pts) / len(data_pts)))

            ordered = sorted(averages, key=lambda avg: avg[1], reverse=descending)
            return "\n".join([f"{name}, {avg}" for name, avg in ordered])

        print("Rank", average_and_rank(ranks_per_strategy), sep="\n----\n", end="\n\n")
        print("Change in rank", average_and_rank(rank_diffs_per_strategy), sep="\n----\n", end="\n\n")
        print("Values", average_and_rank(vals_per_strategy, True), sep="\n----\n", end="\n\n")
