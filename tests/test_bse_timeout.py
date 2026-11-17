import tempfile
import unittest
from collector.market_snapshot import load_rosters
from collector.reconcile import ROSTERS

class BSETimeoutTest(unittest.TestCase):
    def test_slow_bse_gets_separate_budget_without_changing_other_calls(self):
        test = self
        class Client:
            timeout = 20
            def call(self, key, function, **kwargs):
                entry = next(x for x in ROSTERS if x[1] == function and x[2] == kwargs)
                name, _, _, code_key, date_key = entry
                test.assertEqual(self.timeout, 90 if name == 'bj' else 20)
                code = {'sh_main':'600000','sh_star':'688001','sz':'000001','bj':'920001'}[name]
                return [{code_key:code,date_key:'2020-01-01'}]
        client = Client()
        with tempfile.TemporaryDirectory() as folder:
            symbols, unavailable = load_rosters(client, folder, '2026-11-17')
        self.assertEqual(len(symbols),4)
        self.assertEqual(unavailable,[])
        self.assertEqual(client.timeout,20)
