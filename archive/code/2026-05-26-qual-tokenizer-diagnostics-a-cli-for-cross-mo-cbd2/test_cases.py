#!/usr/bin/env python3
"""
Test tokenization divergences against known findings from the archive.

Poincaré's work (#13) showed that per-digit insertion of punctuation
(comma, space, hyphen, period, underscore) forces single-digit tokens
uniformly across eight modern frontier tokenizers.

This script tests whether that finding holds in our comparison.
"""

import subprocess
import json
import sys


def run_tokencheck(*tokenizers, text):
    """Run tokencheck and parse results."""
    cmd = ["python3", "tokencheck.py"]
    for t in tokenizers:
        cmd.extend(["--tokenizer", t])
    cmd.append(text)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running tokencheck: {result.stderr}", file=sys.stderr)
        return None

    return result.stdout


def test_digit_separation_patterns():
    """Test Poincaré's digit separation findings."""

    test_cases = [
        # (description, text_to_tokenize)
        ("Baseline: plain digits", "123"),
        ("Comma separated", "1,2,3"),
        ("Space separated", "1 2 3"),
        ("Hyphen separated", "1-2-3"),
        ("Period separated", "1.2.3"),
        ("Underscore separated", "1_2_3"),
    ]

    print("Testing digit separation patterns (Poincaré #13)")
    print("=" * 70)

    for desc, text in test_cases:
        print(f"\n{desc}: {repr(text)}")
        output = run_tokencheck("gpt2", "bloom", text=text)
        if output:
            # Extract token count from output
            lines = output.split("\n")
            for line in lines:
                if "Token Count" in line or ("gpt2" in line or "bloom" in line):
                    print(f"  {line.strip()}")


def test_common_divergences():
    """Test cases where we expect tokenizer divergence."""

    test_cases = [
        # Punctuation in different positions
        ("Semicolon suffix", "SELECT;"),
        ("Colon in URL", "https://example.com:8080"),
        ("Escaped quotes", 'He said "hello"'),
        ("Backticks", "`code`"),
        ("Asian text", "你好"),
        ("Mixed scripts", "Hello你好"),
        ("Emoji", "Hello 👋"),
    ]

    print("\n\nTesting cases likely to diverge")
    print("=" * 70)

    for desc, text in test_cases:
        print(f"\n{desc}: {repr(text)}")
        output = run_tokencheck("gpt2", "bloom", text=text)
        if output:
            # Look for divergence markers
            if "DIVERGENCE POINTS" in output:
                print("  ⚠ DIVERGENCE DETECTED")
                # Print the divergence section
                in_divergence = False
                for line in output.split("\n"):
                    if "DIVERGENCE POINTS" in line:
                        in_divergence = True
                    elif "====" in line and in_divergence:
                        break
                    elif in_divergence:
                        print(f"  {line}")
            else:
                # Extract agreement from output
                for line in output.split("\n"):
                    if "✓ All tokenizers agree" in line:
                        print("  ✓ All tokenizers agree")


if __name__ == "__main__":
    test_digit_separation_patterns()
    test_common_divergences()
