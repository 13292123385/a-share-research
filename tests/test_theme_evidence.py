import unittest
from collector.theme_evidence import parse_evidence

class DatedEvidenceTests(unittest.TestCase):
    html='<section id="market-concepts"><h2 id="concept-title"><strong>2026-11-11</strong></h2><table><tbody><tr><th><a class="concept-detail-link" href="https://www.dabanke.com/gn.html?name=PCB&date=20261111">PCB</a></th><td><span class="concept-stock" title="600001.SH"><a class="stock-detail-link" href="https://www.dabanke.com/gupiao-600001.html?review_date=2026-11-11">示例</a></span></td></tr></tbody></table></section>'
    def parse(self,html=None,date='2026-11-11'):
        return parse_evidence(html or self.html,date,'2026-11-12T00:00:00+08:00','https://www.dabanke.com/index-20261111.html')
    def test_mapping_is_explicit_partial_dated_evidence(self):
        r=self.parse()[0]
        self.assertEqual(r['code'],'600001')
        self.assertEqual(r['theme_name'],'PCB')
        self.assertEqual(r['coverage'],'partial_selected_active_stocks')
        self.assertFalse(r['source_price_used'])
        self.assertNotIn('historical_valid_from',r)
    def test_wrong_date_is_rejected(self):
        with self.assertRaises(ValueError):self.parse(date='2026-11-10')
    def test_wrong_stock_link_is_rejected(self):
        with self.assertRaises(ValueError):self.parse(self.html.replace('gupiao-600001','gupiao-600002'))
    def test_wrong_theme_link_date_is_rejected(self):
        with self.assertRaises(ValueError):self.parse(self.html.replace('date=20261111','date=20261110'))
    def test_empty_page_is_missing(self):
        with self.assertRaises(ValueError):self.parse('<html></html>')
