import unittest

from elections import Elections


class ElectionShould(unittest.TestCase):

    def test_run_without_districts(self):
        districts = {
            'District 1': {'Bob', 'Anna', 'Jess', 'July'},
            'District 2': {'Jerry', 'Simon'},
            'District 3': {'Johnny', 'Matt', 'Carole'}
        }

        elections = Elections(districts, False)
        elections.add_candidate('Michel')
        elections.add_candidate('Jerry')
        elections.add_candidate('Johnny')

        elections.vote_for('Bob', 'Jerry', 'District 1')
        elections.vote_for('Jerry', 'Jerry', 'District 2')
        elections.vote_for('Anna', 'Johnny', 'District 1')
        elections.vote_for('Johnny', 'Johnny', 'District 3')
        elections.vote_for('Matt', 'Donald', 'District 3')
        elections.vote_for('Jess', 'Joe', 'District 1')
        elections.vote_for('Simon', '', 'District 2')
        elections.vote_for('Carole', '', 'District 3')

        results = elections.results()

        expected_results = {
            'Jerry': '50,00%',
            'Johnny': '50,00%',
            'Michel': '0,00%',
            'Blank': '25,00%',
            'Null': '25,00%',
            'Abstention': '11,11%'
        }

        self.assertEqual(expected_results, results)

    def test_run_with_districts(self):
        districts = {
            'District 1': {'Bob', 'Anna', 'Jess', 'July'},
            'District 2': {'Jerry', 'Simon'},
            'District 3': {'Johnny', 'Matt', 'Carole'}
        }
        elections = Elections(districts, True)
        elections.add_candidate('Michel')
        elections.add_candidate('Jerry')
        elections.add_candidate('Johnny')

        elections.vote_for('Bob', 'Jerry', 'District 1')
        elections.vote_for('Jerry', 'Jerry', 'District 2')
        elections.vote_for('Anna', 'Johnny', 'District 1')
        elections.vote_for('Johnny', 'Johnny', 'District 3')
        elections.vote_for('Matt', 'Donald', 'District 3')
        elections.vote_for('Jess', 'Joe', 'District 1')
        elections.vote_for('July', 'Jerry', 'District 1')
        elections.vote_for('Simon', '', 'District 2')
        elections.vote_for('Carole', '', 'District 3')

        results = elections.results()

        expected_results = {
            'Jerry': '66,67%',
            'Johnny': '33,33%',
            'Michel': '0,00%',
            'Blank': '22,22%',
            'Null': '22,22%',
            'Abstention': '0,00%'
        }
        self.assertEqual(expected_results, results)


if __name__ == '__main__':
    unittest.main()
