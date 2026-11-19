# ✏️ Typo Detector (Trie)

Given a dictionary and a word that looks like a typo, this returns every dictionary word **exactly one substitution away**. It uses tries instead of comparing the word against every entry. Written from scratch in Python with no external libraries.

```python
from typo_detector import TypoDetector

detector = TypoDetector(["abcd", "abcc", "bbcd", "dacb"])
detector.check_word("abcb")   # -> ['abcc', 'abcd']
```

---

## How it works

1. **One trie per word length.** A one-substitution match must have the same length as the input, so each word is inserted into the trie for its length. A lookup only ever searches one small trie.
2. **Breadth-first search with an edit budget.** Each queue entry is a `(trie node, mismatches so far, position in word)` triple.
   - Following the child that matches the next letter costs nothing.
   - Following any other child uses up the single allowed mismatch.
   - A path is dropped as soon as it would need a second mismatch.
3. **Results in order.** Words that reach the end with exactly one mismatch are collected. Because children are visited in alphabetical order, they come out sorted.

| Operation | Time |
|---|---|
| Build | O(C), where C = total characters in the dictionary |
| Lookup | O(J·N + X), where J = word length, N = dictionary words of that length, X = output size |

---

## ✅ Tests

```bash
python -m unittest test_typo_detector
```

**All 16 pass**, including an empty dictionary.

## 🛠️ Tech
Python 3 · tries · breadth-first search · edit distance
