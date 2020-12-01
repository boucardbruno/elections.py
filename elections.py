class Elections(object):
    votes_with_districts: {}

    def __init__(self, districts: {}, with_district: bool):
        self.candidates = []
        self.districts_with_their_candidates = {}
        self.official_candidates = []
        self.votes_with_districts = {
            'District 1': [],
            'District 2': [],
            'District 3': []
        }
        self.votes_without_districts = []
        self.districts = districts
        self.with_district = with_district

    def add_candidate(self, candidate: str):
        self.official_candidates.append(candidate)
        self.candidates.append(candidate)
        self.votes_without_districts.append(0)
        self.votes_with_districts["District 1"].append(0)
        self.votes_with_districts["District 2"].append(0)
        self.votes_with_districts["District 3"].append(0)

    def vote_for(self, elector: str, candidate: str, elector_district: str):

        if not self.with_district:
            if candidate in self.candidates:
                index = self.candidates.index(candidate)
                self.votes_without_districts[index] = self.votes_without_districts[index] + 1
            else:
                self.candidates.append(candidate)
                self.votes_without_districts.append(1)
        else:
            if elector_district in self.votes_with_districts:
                district_votes = self.votes_with_districts[elector_district]
                if candidate in self.candidates:
                    index = self.candidates.index(candidate)
                    district_votes[index] = district_votes[index] + 1
                else:
                    self.candidates.append(candidate)
                    for (k, v) in self.votes_with_districts.items():
                        v.append(0)
                    district_votes[len(self.candidates) - 1] \
                        = district_votes[len(self.candidates) - 1] + 1

    @property
    def results(self):
        results = {}
        nb_votes = 0
        null_votes = 0
        blank_votes = 0
        nb_valid_votes = 0
        if not self.with_district:
            nb_votes = sum([vote for vote in self.votes_without_districts])
            for index in range(0, len(self.official_candidates)):
                index = self.candidates.index(self.official_candidates[index])
                nb_valid_votes += self.votes_without_districts[index]

            for index in range(0, len(self.votes_without_districts)):
                candidate_result = self.votes_without_districts[index] * 100 / nb_valid_votes
                candidate = self.candidates[index]
                if self.official_candidates.__contains__(candidate):
                    results[candidate] = "{:.2f}%".format(candidate_result).replace(".", ",")
                else:
                    if self.candidates[index] == '':
                        blank_votes += self.votes_without_districts[index]
                    else:
                        null_votes += self.votes_without_districts[index]

        else:
            for key, value in self.votes_with_districts.items():
                district_votes = value
                nb_votes += sum([vote for vote in district_votes])

            for index in range(0, len(self.official_candidates)):
                index = self.candidates.index(self.official_candidates[index])
                for key, value in self.votes_with_districts.items():
                    district_votes = value
                    nb_valid_votes += district_votes[index]

            official_candidates_result = {}

            for index in range(0, len(self.official_candidates)):
                official_candidates_result[self.candidates[index]] = 0

            for key, value in self.votes_with_districts.items():
                district_result = []
                districtVotes = value
                for index in range(0, len(districtVotes)):
                    candidate_result = 0.0
                    if nb_valid_votes != 0:
                        candidate_result = districtVotes[index] * 100 / nb_valid_votes
                    candidate = self.candidates[index]
                    if candidate in self.official_candidates:
                        district_result.append(candidate_result)
                    else:
                        if candidate == "":
                            blank_votes += districtVotes[index]
                        else:
                            null_votes += districtVotes[index]
                district_winner_index = 0
                for index in range(1, len(district_result)):
                    if district_result[district_winner_index] < district_result[index]:
                        district_winner_index = index
                official_candidates_result[self.candidates[district_winner_index]] = official_candidates_result[
                                                                                         self.candidates[
                                                                                             district_winner_index]] + 1

            for index in range(0, len(official_candidates_result)):
                ratioCandidate = official_candidates_result[self.candidates[index]] / len(
                    official_candidates_result) * 100
                results[self.candidates[index]] = "{:.2f}%".format(ratioCandidate).replace(".", ",")

        blank_result = blank_votes * 100 / nb_votes
        results["Blank"] = "{:.2f}%".format(blank_result).replace(".", ",")

        null_result = null_votes * 100 / nb_votes
        results["Null"] = "{:.2f}%".format(null_result).replace(".", ",")

        nb_electors = sum(([len(v) for k, v in self.districts.items()]))
        abstention_result = 100 - nb_votes * 100 / nb_electors
        results["Abstention"] = "{:.2f}%".format(abstention_result).replace(".", ",")
        abstention_result = 100 - nb_votes * 100 / nb_electors
        results["Abstention"] = "{:.2f}%".format(abstention_result).replace(".", ",")

        return results
