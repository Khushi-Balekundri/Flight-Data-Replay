import os
import subprocess
import sys
from pathlib import Path

TEST_FILES = (
    "test_loader.py",
    "test_replay.py",
    "test_export_replay_fdr.py",
)

ROOT = Path(__file__).resolve().parent
TEST_ROOT = ROOT / "tests"


def run_test(file):
    print(f"\n=== Running {file.name} ===")

    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).parent)

    result = subprocess.run(
        [sys.executable, str(file)],
        capture_output=True,
        text=True,
        env=env
    )

    
    print(result.stdout, end="")
    
    if result.returncode != 0:
        print("[NO] FAILED")
        if result.stderr:
            print(result.stderr, end="")
        return False
    
    print("[OK] PASSED")
    return True

def main():
    if not TEST_ROOT.exists():
        sys.exit("ERROR: test folder not found.")
    
    print("Running unified test suite...\n")
    
    failed_tests = []
    for test_file in TEST_FILES:
        path = TEST_ROOT / test_file
        if not path.exists():
            print(f"WARNING: {test_file} not found, skipping")
            continue
        
        if not run_test(path):
            failed_tests.append(test_file)
    
    print("\n===========================")
    if not failed_tests:
        print("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print(f"{len(failed_tests)} TEST(S) FAILED")
        for test in failed_tests:
            print(f"  - {test}")
        sys.exit(1)

if __name__ == "__main__":
    main()