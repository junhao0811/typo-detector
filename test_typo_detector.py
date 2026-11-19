import unittest
from typo_detector import TypoDetector


class TestTypoDetector(unittest.TestCase):

    def test_n_1(self):
        ai = TypoDetector([])
        self.assertEqual(ai.check_word("any"), [])

    def test_n_2(self):
        ai = TypoDetector(["", "a", "b"])
        self.assertEqual(ai.check_word(""), [])

    def test_n_3(self):
        words = ["car", "cat", "bar"]
        ai = TypoDetector(words)
        result = ai.check_word("car")
        self.assertCountEqual(result, ["bar", "cat"])

    def test_n_4(self):
        words = ["test", "best", "tent"]
        ai = TypoDetector(words)
        result = ai.check_word("test")
        self.assertCountEqual(result, ["best", "tent"])

    def test_n_5(self):
        words = ["abcd", "abcf", "wxyz"]
        ai = TypoDetector(words)
        result = ai.check_word("abcd")
        self.assertEqual(result, ["abcf"])

    def test_n_6(self):
        words = ["a", "ab", "abc"]
        ai = TypoDetector(words)
        self.assertEqual(ai.check_word("ab"), [])

    def test_n_7(self):
        words = ["dog", "dig", "dag", "dot"]
        ai = TypoDetector(words)
        first = ai.check_word("dog")
        self.assertCountEqual(first, ["dig", "dag", "dot"])
        second = ai.check_word("dig")
        self.assertCountEqual(second, ["dog", "dag"])

    def test_bees(self):
        words = [
            "according",
            "to",
            "all",
            "known",
            "laws",
            "of",
            "aviation",
            "there",
            "is",
            "no",
            "way",
            "a",
            "bee",
            "should",
            "be",
            "able",
            "to",
            "fly",
        ]

        ai = TypoDetector(list(set(words)))
        input = [
            "acfording",
            "tx",
            "agl",
            "khown",
            "lass",
            "ou",
            "aviatzon",
            "thyre",
            "zs",
            "qo",
            "wak",
            "l",
            "vee",
            "spould",
            "bq",
            "alle",
            "ao",
            "gly",
        ]

        for i in range(len(input)):
            self.assertIn(words[i], ai.check_word(input[i]))

    def test_j_1(self):
        words = ["aaa", "abc", "xyz", "aba", "aaaa"]
        ai = TypoDetector(words)

        sus_list = ["aaa", "axa", "ab", "xxx", "aaab"]
        expected = [["aba"], ["aaa", "aba"], [], [], ["aaaa"]]

        for sus, exp in zip(sus_list, expected):
            with self.subTest(sus_word=sus):
                result = ai.check_word(sus)
                self.assertCountEqual(result, exp)
                self.assertEqual(result, exp)

    def test_a_1(self):
        ai = TypoDetector(["abc", "def", "ghi"])
        self.assertEqual(ai.check_word("xyz"), [])

    def test_a_2(self):
        words = ["bake", "cake", "lake", "make"]
        ai = TypoDetector(words)
        result = ai.check_word("fake")
        self.assertCountEqual(result, ["bake", "cake", "lake", "make"])

    def test_a_3(self):
        ai = TypoDetector(["hat", "bat", "cat"])
        result = ai.check_word("rat")
        self.assertCountEqual(result, ["hat", "bat", "cat"])

    def test_a_4(self):
        ai = TypoDetector(["dog", "dot", "don"])
        result = ai.check_word("dop")
        self.assertCountEqual(result, ["dog", "dot", "don"])

    def test_a_5(self):
        ai = TypoDetector(["hello", "hxllo", "hallo", "hillo"])
        result = ai.check_word("hello")
        self.assertCountEqual(result, ["hxllo", "hallo", "hillo"])

    def test_a_6(self):
        ai = TypoDetector(["aaaa", "aaab", "aaba", "abaa", "baaa"])
        result = ai.check_word("aaaa")
        self.assertCountEqual(result, ["aaab", "aaba", "abaa", "baaa"])

    def test_a_7(self):
        ai = TypoDetector(["word"])
        self.assertEqual(ai.check_word("word"), [])


if __name__ == "__main__":
    unittest.main()
