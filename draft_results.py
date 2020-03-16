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

    def __init__(self, numteams):
        self.results = []
        self.num_teams = numteams

    def add_trials(self, trials: [TrialResult]):
        self.results.extend(trials)

    def summary_by_strategy(self):
        normalization_factor = defaultdict(int)
        ranks_per_strategy = defaultdict(list)
        rank_diffs_per_strategy = defaultdict(list)
        vals_per_strategy = defaultdict(list)
        strategy_per_rank = defaultdict(lambda: defaultdict(int))

        for trial_result in self.results:
            ranks_per_strategy[trial_result.strategy_name].append(
                trial_result.rank + 1)  # fix the zero-based rank
            gain_in_rank = trial_result.draft_pos - trial_result.rank
            rank_diffs_per_strategy[trial_result.strategy_name].append(gain_in_rank)
            vals_per_strategy[trial_result.strategy_name].append(trial_result.value)
            strategy_per_rank[trial_result.rank][trial_result.strategy_name] += 1
            normalization_factor[trial_result.strategy_name] += 1

        def average_and_rank(data, descending=False, rankmaximum=-1):
            averages = []
            for strategy_name, data_pts in data.items():
                averages.append((strategy_name, sum(data_pts) / len(data_pts)))

            ordered = sorted(averages, key=lambda avg: avg[1], reverse=descending)
            return "\n".join(
                [f"{name}, {f'{avg}/{rankmaximum}' if (rankmaximum != -1) else avg}" for name, avg
                 in ordered])

        def average_and_rank_with_sign(data, descending=False):
            averages = []
            for strategy_name, data_pts in data.items():
                averages.append((strategy_name, sum(data_pts) / len(data_pts)))

            ordered = sorted(averages, key=lambda avg: avg[1], reverse=descending)
            return "\n".join(
                [f"{name}, {f'+{avg}' if (avg > 0) else avg}" for name, avg in ordered])

        print("Final rank in the drafts on average (payoff)",
              average_and_rank(ranks_per_strategy, False, self.num_teams), sep="\n----\n",
              end="\n----\n\n")
        print("Average rank compared to draft rank",
              average_and_rank_with_sign(rank_diffs_per_strategy, True), sep="\n----\n",
              end="\n----\n\n")
        print("Average accumulated player values", average_and_rank(vals_per_strategy, True),
              sep="\n----\n", end="\n----\n\n")

        print("Stacked bar chart CSV")
        strategy_names = ranks_per_strategy.keys()
        print('', *strategy_names, sep=',')
        for rank, strategy_ranks in strategy_per_rank.items():
            print(rank + 1, end=',')
            vals = []
            for strategy in strategy_names:
                if strategy in strategy_ranks:
                    vals.append(f'{strategy_ranks[strategy] / normalization_factor[strategy]}')
                else:
                    vals.append('')

            print(",".join(vals))
