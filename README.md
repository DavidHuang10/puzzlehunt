# Linked List Cycle Detection

Detect cycles in a linked list using unique node values. Pass all tests to unlock a hidden clue!

## Problem

Given a linked list where **each node has a unique value**, return `True` if there's a cycle, `False` otherwise.


### 1. Understand the Problem
```bash
python3 examples.py
```
Shows visual examples and step-by-step algorithm demonstration.

### 2. Implement Your Solution
Edit `solution.py` and implement the `has_cycle()` function:

```python
def has_cycle(head):
    # TODO: Use a set to track seen values
    # Hint: if current.val in seen: return True
    return False
```

### 3. Test Locally
```bash
python3 solution.py
```
Runs 3 basic tests to check your implementation.

### 4. Run Full Test Suite
```bash
python3 test_runner.py
```
Runs **32 comprehensive test cases**. Pass all to unlock the hidden clue!


## 🎁 Reward

Complete all 32 test cases successfully to reveal a hidden clue!

## 📁 Files

- `solution.py` - **Edit this file** with your implementation
- `test_runner.py` - Run this for full testing (32 tests)
- `examples.py` - Run this to see problem examples
- `linkedlist.py` - Utilities (don't edit)

## 🔧 Requirements

- Python 3.7+
- Each node value is unique 
- Head always exists (no empty lists)
- Use a set to track visited values

## 🐛 Troubleshooting

**Function not found**: Make sure your function is named exactly `has_cycle`

**Wrong results**: Remember to check `if current.val in seen:` before adding to set

**Need help**: Run `python3 examples.py` for step-by-step demonstration

---

🎮 **Ready?** Run `python3 examples.py` to get started!
