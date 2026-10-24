import unittest
from collector.model import normalize, ordinary, promotion, theme_score
from collector.run import check_rows


class ModelTests(unittest.TestCase):
    def test_universe(self):
        for prefix in ('600','601','603','605','000','001','002','003'):
            self.assertTrue(ordinary(prefix+'123', '测试'))
        for code in ('688001','300001','301001','830001','920001','200001','60001'):
            self.assertFalse(ordinary(code, '测试'))
        for name in ('ST测试','*ST测试','测试退','退市整理'):
            self.assertFalse(ordinary('600001', name))

    def test_one_word_and_t(self):
        raw = [{'代码':'600001','名称':'测试','连板数':1}]
        self.assertIsNone(normalize(raw)[0]['all_day_one_word'])
        quote = {'600001': {'今开':10, '最高':10, '最低':10, '最新价':10}}
        self.assertFalse(normalize(raw, quote)[0]['eligible_observation'])
        quote['600001']['最低'] = 9.9
        row = normalize(raw, quote)[0]
        self.assertTrue(row['eligible_observation'])
        self.assertFalse(row['execution_verified'])

    def test_subjective_scores(self):
        self.assertIsNone(theme_score()['total'])
        self.assertEqual(theme_score(5,5,5,1)['total'], 15)
        self.assertEqual(theme_score(0,0,0,-1)['total'], 0)
        with self.assertRaises(ValueError):
            theme_score(6)

    def test_missing_not_zero(self):
        self.assertIsNone(promotion(None, [], [])['observation_rate'])
        self.assertIsNone(promotion([], [], [])['observation_rate'])
        class Fake:
            calls = {'x': {}}
        self.assertIsNone(check_rows(Fake(), 'x', [{'代码':'1'}], ['代码','名称']))
        self.assertEqual(Fake.calls['x']['status'], 'schema_error')

    def test_promotion_and_denominator(self):
        yesterday = [dict(code='600001', height=1, eligible_observation=True),
                     dict(code='600002', height=1, eligible_observation=True),
                     dict(code='600003', height=1, eligible_observation=False)]
        today = [dict(code='600001', height=2, eligible_observation=True),
                 dict(code='600003', height=2, eligible_observation=False)]
        r = promotion(yesterday, today, [dict(code='600002')])
        self.assertEqual(r['denominator'], 2)
        self.assertEqual(r['observation_rate'], .5)
        self.assertEqual(r['broken_count'], 1)
        self.assertIsNone(r['verified_tradable_rate'])


if __name__ == '__main__':
    unittest.main()
