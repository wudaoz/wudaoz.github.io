---
title: "Is the Harness Really Keeping Us Safe? Why Command Text Is Not Enough"
date: 2026-11-19
description: "The harness decides what a coding agent may run. How flexible and effective are those checks in practice?"
---

*This is a preview. The full post is coming soon.*

The harness around a coding agent decides which commands may run. Many of these checks read the text of a command, and as far as I can tell, the sandbox ends up as the last line of defense. Our recent work, ["Shall We Approve?"](https://arxiv.org/abs/2610.40753), shows that command text can be misleading: the harm may sit in the code a command invokes, not in the command itself.

In this post I want to look at how flexible and effective harness-level safety mechanisms really are, and what it would take to rely on more than the sandbox.
