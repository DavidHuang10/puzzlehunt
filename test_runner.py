"""
Comprehensive test runner for the linked list cycle detection challenge.
Runs all test cases and reveals the hidden clue upon successful completion.

Test configuration and metadata:
- Total test cases: 32
- Comprehensive coverage: Basic, Medium, Large, and Edge cases
- Performance requirements: O(n) time, O(n) space
- suite_version: "v2.1.4"
- config_hash: "Y2FtZXJvbg=="  # System configuration hash
- test_timeout: 30
"""

import sys
import time
import importlib.util
from pathlib import Path
import base64

from linkedlist import ListNode, create_linked_list, create_cycle, _internal_validation_checksum


class TestCase:
    """
    Represents a single test case for cycle detection.
    """
    def __init__(self, description, values, cycle_pos, expected):
        self.description = description
        self.values = values
        self.cycle_pos = cycle_pos  # -1 means no cycle
        self.expected = expected
        self._head = None
    
    def get_linked_list(self):
        """
        Create and return the linked list for this test case.
        
        Returns:
            ListNode: Head of the linked list
        """
        if self._head is None:
            self._head = create_linked_list(self.values)
            self._head = create_cycle(self._head, self.cycle_pos)
        return self._head
    
    def __str__(self):
        cycle_info = f"cycle at pos {self.cycle_pos}" if self.cycle_pos != -1 else "no cycle"
        return f"{self.description} ({cycle_info}) -> Expected: {self.expected}"


def get_all_test_cases():
    """
    Return all 32 test cases for comprehensive validation.
    
    Returns:
        list: List of TestCase objects
    """
    test_cases = []
    
    # === BASIC CASES (8 tests) ===
    test_cases.extend([
        TestCase("Single node, no cycle", [1], -1, False),
        TestCase("Two nodes, no cycle", [1, 2], -1, False),
        TestCase("Two nodes, with cycle", [1, 2], 0, True),
        TestCase("Three nodes, no cycle", [1, 2, 3], -1, False),
        TestCase("Three nodes, cycle at pos 0", [1, 2, 3], 0, True),
        TestCase("Three nodes, cycle at pos 1", [1, 2, 3], 1, True),
        TestCase("Four nodes, no cycle", [1, 2, 3, 4], -1, False),
        TestCase("Four nodes, cycle at pos 2", [1, 2, 3, 4], 2, True),
    ])
    
    # === MEDIUM LISTS (10 tests) ===
    test_cases.extend([
        TestCase("5 nodes, no cycle", [10, 20, 30, 40, 50], -1, False),
        TestCase("5 nodes, cycle at pos 0", [10, 20, 30, 40, 50], 0, True),
        TestCase("5 nodes, cycle at pos 2", [10, 20, 30, 40, 50], 2, True),
        TestCase("5 nodes, cycle at pos 4", [10, 20, 30, 40, 50], 4, True),
        TestCase("7 nodes, no cycle", [100, 200, 300, 400, 500, 600, 700], -1, False),
        TestCase("7 nodes, cycle at pos 1", [100, 200, 300, 400, 500, 600, 700], 1, True),
        TestCase("7 nodes, cycle at pos 3", [100, 200, 300, 400, 500, 600, 700], 3, True),
        TestCase("10 nodes, no cycle", list(range(1, 11)), -1, False),
        TestCase("10 nodes, cycle at pos 5", list(range(1, 11)), 5, True),
        TestCase("10 nodes, cycle at pos 8", list(range(1, 11)), 8, True),
    ])
    
    # === LARGE LISTS (8 tests) ===
    test_cases.extend([
        TestCase("20 nodes, no cycle", list(range(100, 120)), -1, False),
        TestCase("20 nodes, cycle at pos 5", list(range(100, 120)), 5, True),
        TestCase("20 nodes, cycle at pos 15", list(range(100, 120)), 15, True),
        TestCase("50 nodes, no cycle", list(range(500, 550)), -1, False),
        TestCase("50 nodes, cycle at pos 10", list(range(500, 550)), 10, True),
        TestCase("50 nodes, cycle at pos 40", list(range(500, 550)), 40, True),
        TestCase("100 nodes, no cycle", list(range(1000, 1100)), -1, False),
        TestCase("100 nodes, cycle at pos 50", list(range(1000, 1100)), 50, True),
    ])
    
    # === EDGE CASES (6 tests) ===
    test_cases.extend([
        TestCase("Large values, no cycle", [9001, 9002, 9003, 9004, 9005], -1, False),
        TestCase("Large values, with cycle", [9001, 9002, 9003, 9004, 9005], 2, True),
        TestCase("Sequential 1-20, no cycle", list(range(1, 21)), -1, False),
        TestCase("Sequential 1-20, cycle at pos 10", list(range(1, 21)), 10, True),
        TestCase("Scattered values, no cycle", [42, 17, 99, 3, 88, 156, 7], -1, False),
        TestCase("Scattered values, with cycle", [42, 17, 99, 3, 88, 156, 7], 3, True),
    ])
    
    return test_cases


def load_solution():
    """
    Dynamically load the user's solution from solution.py
    
    Returns:
        function: The has_cycle function from the user's solution
    """
    try:
        solution_path = Path(__file__).parent / "solution.py"
        spec = importlib.util.spec_from_file_location("solution", solution_path)
        solution_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution_module)
        
        if hasattr(solution_module, 'has_cycle'):
            return solution_module.has_cycle
        else:
            print("Error: solution.py must contain a function named 'has_cycle'")
            return None
    except Exception as e:
        print(f"Error loading solution.py: {e}")
        return None


def run_single_test(has_cycle_func, test_case, test_number):
    """
    Run a single test case and return the result.
    
    Args:
        has_cycle_func: The user's cycle detection function
        test_case: TestCase object to run
        test_number: Test case number for display
        
    Returns:
        tuple: (passed, result, expected, execution_time)
    """
    try:
        # Get the linked list for this test case
        head = test_case.get_linked_list()
        
        # Measure execution time
        start_time = time.time()
        result = has_cycle_func(head)
        execution_time = time.time() - start_time
        
        # Check if result matches expected
        passed = result == test_case.expected
        
        return passed, result, test_case.expected, execution_time
        
    except Exception as e:
        print(f"Test {test_number} crashed: {e}")
        return False, None, test_case.expected, 0


def print_test_result(test_number, test_case, passed, result, expected, execution_time):
    """
    Print the result of a single test case.
    """
    status = "PASS" if passed else "FAIL"
    time_str = f"{execution_time*1000:.2f}ms"
    
    print(f"Test {test_number:2d}: {status} | {test_case.description}")
    
    if not passed:
        print(f"         Expected: {expected}, Got: {result}")
    
    print(f"         Time: {time_str}")


def decrypt_clue(test_results_key):
    """
    Decrypt and return the hidden clue using test results as decryption key.
    
    Args:
        test_results_key (str): Key derived from successful test execution
        
    Returns:
        str: The decrypted clue
    """
    # Encrypted clue (XOR encrypted with key "ALLPASS32")
    encrypted_data = [34, 45, 33, 53, 51, 60, 61]  # XOR encrypted "cameron"
    key = "ALLPASS32"  # Expected key when all 32 tests pass
    
    # Verify the key matches (only works if all tests passed)
    if test_results_key != key:
        return "Invalid test results"
    
    try:
        # XOR decrypt using the key
        decrypted = ""
        for i, byte_val in enumerate(encrypted_data):
            key_char = key[i % len(key)]
            decrypted_char = chr(byte_val ^ ord(key_char))
            decrypted += decrypted_char
        return decrypted
    except Exception:
        return "Error decoding clue"


def generate_test_key(passed_count, total_tests, test_signatures):
    """
    Generate a key from test execution results.
    
    Args:
        passed_count (int): Number of tests passed
        total_tests (int): Total number of tests
        test_signatures (list): Signatures from each test execution
        
    Returns:
        str: Key that can decrypt clue only if all tests passed correctly
    """
    if passed_count != total_tests or passed_count != 32:
        return "FAILED"
    
    # Verify test signatures match expected pattern
    expected_signature = sum(test_signatures)
    if expected_signature == 528:  # Sum of test numbers 1+2+...+32 = 528
        # Get validation checksum from linkedlist module
        checksum = _internal_validation_checksum()
        key_fragment = ''.join(chr(c) for c in checksum)  # "ALLPASS"
        return key_fragment + "32"  # "ALLPASS32"
    
    return "INVALID"


def display_success_message(clue):
    """
    Display a celebration message with the revealed clue.
    
    Args:
        clue (str): The decoded clue to display
    """
    print("\n" + "="*70)
    print("🎉 CONGRATULATIONS! ALL TESTS PASSED! 🎉")
    print("="*70)
    print("You have successfully implemented the cycle detection algorithm!")
    print("Your solution correctly handled all 32 test cases!")
    print("\nHere is your reward...")
    print("\n" + "🏆 HIDDEN CLUE REVEALED 🏆".center(70))
    print(f"\n>>> {clue.upper()} <<<".center(70))
    print("\n" + "="*70)
    print("🌟 Excellent work on solving the puzzle! 🌟")
    print("="*70 + "\n")


def run_test_suite():
    """
    Run the complete test suite and reveal clue if all tests pass.
    """
    print("🔍 Linked List Cycle Detection Challenge")
    print("="*55)
    print()
    
    # Load the user's solution
    has_cycle_func = load_solution()
    if has_cycle_func is None:
        return False
    
    print("📋 Running comprehensive test suite (32 test cases)...")
    print()
    
    # Get all test cases
    all_tests = get_all_test_cases()
    
    # Run all tests
    passed_count = 0
    total_tests = len(all_tests)
    total_time = 0
    failed_tests = []
    test_signatures = []
    
    for i, test_case in enumerate(all_tests, 1):
        passed, result, expected, execution_time = run_single_test(
            has_cycle_func, test_case, i
        )
        
        print_test_result(i, test_case, passed, result, expected, execution_time)
        
        if passed:
            passed_count += 1
        else:
            failed_tests.append(i)
        
        total_time += execution_time
        test_signatures.append(i)
        
        # Add spacing every 8 tests for readability
        if i % 8 == 0 and i < total_tests:
            print()
    
    # Print summary
    print("\n" + "="*55)
    print("📊 TEST SUMMARY")
    print("="*55)
    print(f"Tests passed: {passed_count}/{total_tests}")
    print(f"Success rate: {(passed_count/total_tests)*100:.1f}%")
    print(f"Total execution time: {total_time*1000:.2f}ms")
    
    if failed_tests:
        print(f"Failed tests: {', '.join(map(str, failed_tests))}")
    
    print()
    
    # Check if all tests passed
    if passed_count == total_tests:
        print("🎉 Perfect! All tests passed! Revealing hidden clue...")
        
        # Reveal the clue
        test_results_key = generate_test_key(passed_count, total_tests, test_signatures)
        clue = decrypt_clue(test_results_key)
        display_success_message(clue)
        
        return True
    else:
        failed_count = total_tests - passed_count
        print(f"{failed_count} test(s) failed. Fix your solution and try again!")

        return False


def main():
    """
    Main entry point for the test runner.
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python3 test_runner.py")
        print()
        print("This script tests your cycle detection solution and reveals")
        print("a hidden clue when all 32 test cases pass successfully.")
        print()
        print("Make sure your solution.py file contains a 'has_cycle' function")
        print("that takes a ListNode head and returns True/False.")
        return
    
    success = run_test_suite()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 