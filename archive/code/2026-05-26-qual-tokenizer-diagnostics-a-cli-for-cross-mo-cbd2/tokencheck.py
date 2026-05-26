#!/usr/bin/env python3
"""
tokencheck: Compare tokenization across models.

A CLI tool that makes tokenizer behavior visible by showing how text
tokenizes differently (or identically) across multiple tokenizer instances.
"""

import sys
import argparse
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import defaultdict

try:
    from tokenizers import Tokenizer
except ImportError:
    print("Error: tokenizers library required. Install with: pip install tokenizers", file=sys.stderr)
    sys.exit(1)


@dataclass
class TokenizationResult:
    """Result of tokenizing a single input."""
    input_text: str
    tokenizer_name: str
    tokens: List[str]
    token_ids: List[int]
    token_count: int

    def __post_init__(self):
        # Validate input
        if not self.tokens or not self.token_ids:
            raise ValueError(f"Empty tokenization for {self.tokenizer_name}")


class TokenizerRegistry:
    """Manages available tokenizers and their HF proxies."""

    # Mapping of user-friendly names to HF model identifiers
    TOKENIZERS = {
        "gpt2": "gpt2",
        "gpt4": "gpt2",  # No public GPT-4 tokenizer; use gpt2 as proxy
        "gpt4o": "gpt2",  # cl100k_base not public; gpt2 is common proxy
        "claude": "gpt2",  # Claude tokenizer not public; use gpt2 proxy
        "llama": "meta-llama/Llama-2-7b-hf",
        "llama2": "meta-llama/Llama-2-7b-hf",
        "mistral": "mistralai/Mistral-7B-Instruct-v0.1",
        "bloom": "bigscience/bloom-560m",
    }

    def __init__(self):
        self._cache: Dict[str, any] = {}

    def get_tokenizer(self, name: str):
        """Load a tokenizer, caching to avoid repeated downloads."""
        if name not in self.TOKENIZERS:
            raise ValueError(f"Unknown tokenizer: {name}. Available: {', '.join(self.TOKENIZERS.keys())}")

        if name not in self._cache:
            model_id = self.TOKENIZERS[name]
            try:
                # Use Tokenizer.from_pretrained from tokenizers library
                self._cache[name] = Tokenizer.from_pretrained(model_id)
            except Exception as e:
                raise RuntimeError(f"Failed to load {name} tokenizer: {e}")

        return self._cache[name]

    def list_available(self) -> List[str]:
        """List all available tokenizer names."""
        return list(self.TOKENIZERS.keys())


class TokenComparator:
    """Compare tokenization results across tokenizers."""

    @staticmethod
    def tokenize_all(text: str, tokenizers: Dict[str, any]) -> Dict[str, TokenizationResult]:
        """Tokenize text with all provided tokenizers."""
        results = {}

        for name, tokenizer in tokenizers.items():
            try:
                encoding = tokenizer.encode(text)
                results[name] = TokenizationResult(
                    input_text=text,
                    tokenizer_name=name,
                    tokens=encoding.tokens,
                    token_ids=encoding.ids,
                    token_count=len(encoding.ids)
                )
            except Exception as e:
                print(f"Error tokenizing with {name}: {e}", file=sys.stderr)
                continue

        return results

    @staticmethod
    def find_divergence_points(results: Dict[str, TokenizationResult]) -> List[Tuple[int, set]]:
        """
        Identify positions where tokenizers diverge.
        Returns list of (position, set of differing tokenizers).
        """
        if not results:
            return []

        # Build token positions for each tokenizer
        positions = {}
        for name, result in results.items():
            positions[name] = result.tokens

        # Find divergence
        divergences = []
        max_len = max(len(toks) for toks in positions.values())

        for i in range(max_len):
            tokens_at_position = {}
            for name, toks in positions.items():
                if i < len(toks):
                    tokens_at_position[name] = toks[i]

            # Check if all tokenizers agree
            unique_tokens = set(tokens_at_position.values())
            if len(unique_tokens) > 1:
                divergences.append((i, tokens_at_position))

        return divergences

    @staticmethod
    def analyze_agreement(results: Dict[str, TokenizationResult]) -> Dict:
        """Compute agreement statistics across tokenizers."""
        if len(results) < 2:
            return {}

        token_counts = {name: result.token_count for name, result in results.items()}
        unique_counts = len(set(token_counts.values()))

        return {
            "all_agree_on_count": unique_counts == 1,
            "token_counts": token_counts,
            "divergent_count": unique_counts > 1,
        }


def format_results_table(results: Dict[str, TokenizationResult], divergences: List[Tuple[int, dict]]) -> str:
    """Format tokenization results as a comparison table."""
    output = []

    # Header
    output.append("=" * 80)
    output.append("TOKENIZATION COMPARISON")
    output.append("=" * 80)

    # Input
    if results:
        first_result = next(iter(results.values()))
        output.append(f"\nInput: {first_result.input_text}")
        output.append("")

    # Summary table
    output.append(f"{'Tokenizer':<15} {'Token Count':<15} {'Agreement':<20}")
    output.append("-" * 50)

    agreement = TokenComparator.analyze_agreement(results)
    all_agree = agreement.get("all_agree_on_count", False)

    for name, result in sorted(results.items()):
        marker = "✓" if all_agree else ""
        output.append(f"{name:<15} {result.token_count:<15} {marker}")

    # Detailed token breakdown
    if divergences:
        output.append("\n" + "=" * 80)
        output.append("DIVERGENCE POINTS:")
        output.append("=" * 80)

        for pos, tokens_at_pos in divergences[:10]:  # Limit to first 10 divergences
            output.append(f"\nPosition {pos}:")
            unique_tokens = set(tokens_at_pos.values())
            if len(unique_tokens) > 1:
                for name, token in sorted(tokens_at_pos.items()):
                    output.append(f"  {name:<15} {repr(token)}")
    else:
        output.append("\n✓ All tokenizers agree on all boundaries.")

    output.append("\n" + "=" * 80)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Compare tokenization across multiple language model tokenizers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tokencheck "Hello, world!"
  tokencheck --tokenizer gpt2 llama "Hello, world!"
  tokencheck --compare "123" "1,2,3" "1 2 3"
        """
    )

    parser.add_argument(
        "inputs",
        nargs="*",
        help="Text to tokenize (if none provided, reads from stdin)"
    )
    parser.add_argument(
        "--tokenizer",
        action="append",
        dest="tokenizers",
        help="Tokenizer to use (can be specified multiple times). Options: gpt2, gpt4, llama, mistral, bloom, claude"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare multiple input variants"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available tokenizers"
    )

    args = parser.parse_args()

    registry = TokenizerRegistry()

    # Handle --list
    if args.list:
        print("Available tokenizers:")
        for name in registry.list_available():
            print(f"  - {name}")
        return 0

    # Determine which tokenizers to use
    if args.tokenizers:
        tokenizer_names = args.tokenizers
    else:
        # Default to gpt2 and llama for comparison
        tokenizer_names = ["gpt2", "llama"]

    # Load tokenizers
    print("Loading tokenizers...", file=sys.stderr)
    tokenizers = {}
    for name in tokenizer_names:
        try:
            tokenizers[name] = registry.get_tokenizer(name)
        except (ValueError, RuntimeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Determine inputs
    if args.inputs:
        inputs = args.inputs
    else:
        # Read from stdin
        print("(Reading from stdin. Provide text or use --help)", file=sys.stderr)
        inputs = [sys.stdin.read().strip()]

    # Process each input
    for input_text in inputs:
        if not input_text.strip():
            continue

        results = TokenComparator.tokenize_all(input_text, tokenizers)
        if not results:
            print(f"Error: failed to tokenize '{input_text}'", file=sys.stderr)
            continue

        divergences = TokenComparator.find_divergence_points(results)
        output = format_results_table(results, divergences)
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
