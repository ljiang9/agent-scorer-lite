import unittest

from agent_scorer import RubricScorer, DEFAULT_RUBRIC, _len_score, _keyword_score


class TestHelpers(unittest.TestCase):
    def test_len_score(self):
        self.assertAlmostEqual(_len_score("a" * 100, 50), 1.0)
        self.assertAlmostEqual(_len_score("短", 50), 1 / 50)

    def test_keyword_score(self):
        self.assertAlmostEqual(_keyword_score("机器 学习", ["机器", "学习", "缺失"]), 2 / 3)
        self.assertEqual(_keyword_score("任意", []), 1.0)


class TestScorer(unittest.TestCase):
    def setUp(self):
        self.sc = RubricScorer()

    def test_total_in_range(self):
        r = self.sc.score("这是一段还可以的输出，有一定长度。包含一些内容。")
        self.assertGreaterEqual(r["total"], 0)
        self.assertLessEqual(r["total"], 1.0)
        self.assertEqual(len(r["details"]), 3)

    def test_longer_scores_higher(self):
        short = "短"
        long = "这是一段足够长的完整输出。第一，它讲了 A。第二，它讲了 B。第三，它总结了 C。"
        self.assertGreater(self.sc.score(long)["total"], self.sc.score(short)["total"])

    def test_custom_rubric(self):
        sc = RubricScorer([{"name": "相关性", "weight": 1.0, "keywords": ["退款"]}])
        r = sc.score("我要退款")
        self.assertEqual(r["details"][0]["score"], 1.0)
        r2 = sc.score("今天天气")
        self.assertEqual(r2["details"][0]["score"], 0.0)


if __name__ == "__main__":
    unittest.main()
