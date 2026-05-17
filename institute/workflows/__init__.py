"""Workflow modules: one per state transition.

Each workflow is a function that takes db state and produces an artifact,
then updates state transactionally. Long-running workflows use resumable
Claude Code session ids so they can be paused and continued safely.
"""
