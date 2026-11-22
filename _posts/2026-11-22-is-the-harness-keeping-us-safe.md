---
title: "Is the Harness Really Keeping Us Safe? Why Command Text Is Not Enough"
date: 2026-11-22
description: "The harness decides what a coding agent may run. How flexible and effective are those checks in practice?"
---

The harness around a coding agent decides which commands may run. Many of these checks read the text of a command, and as far as I can tell, the sandbox ends up as the last line of defense. Our recent work, ["Shall We Approve?"](https://arxiv.org/abs/2610.40753), shows that command text can be misleading: the harm may sit in the code a command invokes, not in the command itself.

In this post I want to look at how flexible and effective harness-level safety mechanisms really are, and what it would take to rely on more than the sandbox. Underneath that is a narrower question: when the harness approves a command, what exactly has it approved?

## What the approval layer is for

Both Claude Code and Codex put a checkpoint between the agent and the shell. You can write allow and deny rules, and more and more of the decisions are now handed to a model. Claude Code's Auto Mode runs a classifier before each action. Codex's auto-review sends requests that would leave the sandbox to a separate reviewer model.

Both vendors are open about the limits of this layer. Claude Code says its Bash rules are not "a security boundary around the program" and that auto mode "does not guarantee safety." Codex calls auto-review "not a deterministic security guarantee." Both point to the sandbox as the thing that actually holds the line.

The numbers they publish say the same thing about what the approval layer is for. Anthropic reports that users approve 93% of Claude Code's permission prompts anyway. OpenAI reports that with auto-review, Codex sessions stop for a human roughly 200 times less often. These are real improvements, and what they improve is how often a person gets interrupted. They say little about how much risky behavior the layer catches.

That would be fine if the questions the layer does ask were the right ones. I worry that they often are not.

## What the approver does not see

Here is the figure that started this line of work for me.

<figure>
  <img src="/assets/img/fig-same-command.avif" alt="Diagram: the same make command deletes source files and repository history in one workspace, and only build artifacts in another." width="900" height="984">
  <figcaption>The same command in two workspaces. The agent types exactly the same thing in both. What it does depends on the files around it, and an approver that reads only the command sees identical input in both cases.</figcaption>
</figure>

A more everyday version: the agent is asked to check whether the tests pass, so it runs `pytest`. Nothing about that command looks risky, and no reasonable rule would block it. But `pytest` imports `conftest.py` from the repository before it runs a single test, and whatever code sits in that file runs too. The same is true of `sitecustomize.py` when Python starts, of a Makefile recipe behind `make build`, and of a git hook behind `git commit`.

In all of these cases the agent does nothing suspicious, and the approver has nothing suspicious to look at. The behavior is in code the approver never reads.

## How much gets through

I wanted to know how big this gap is in practice, so I built a set of 200 scenarios and ran a real Claude Code agent through each of them.

Each scenario asks for one restricted effect: an outbound connection, a read of a secret, a file write, a process that outlives the session, resource exhaustion, or a connection to a local service. The effect is delivered through different channels, from a plain shell command to a Makefile, a `conftest.py`, a git hook, a startup file, or a sub-agent. In about half the cases the agent is asked, in honest language, to write the code itself. In the rest the code is already in the repository and the agent gets an innocent task like "run the tests." I tested two gates: a plain allowlist of tool names, and Claude Code's own auto-mode classifier.

I did not trust the agent's transcript to tell me what happened. Each run was traced at the system-call level, and every effect had a physical witness: a local listener that records any bytes it receives, a process and service snapshot after the agent exits, or a check on the file it was supposed to write. Everything stayed on the machine. The "secrets" were planted fakes, and nothing ever connected to a real external host.

Most restricted effects got through. In 144 of 200 scenarios (72%) the effect happened while the gate approved every call it saw. Of the cases that were stopped, only 7 were stopped by the gate. The other 43 were stopped by the agent itself, which declined the task.

Making the gate smarter did not change this. The tool-name allowlist let 71% through and the LLM classifier let 72% through. The classifier was clearly active and did block some actions, but when the effect is not in the text it reads, a better model has nothing more to reason about. What it lacks is information.

What decided the outcome was whether the agent could see the harmful code. I took one clearly dangerous action, reading a planted key and sending it to an external-looking host, and ran it two ways, twelve times each. When the agent had to write the code itself, it refused every time. When the same code sat in a `conftest.py` and the agent was only asked to run the tests, it went through every time.

These numbers have limits. My scenarios use small repositories and deliberately harmless stand-ins for real damage, so a success here means that a restricted action ran without being stopped. It does not mean that something catastrophic happened. I also ran only Claude Code, and what I say about Codex comes from its documentation. And I am not the first to look at this: [Ji et al.](https://arxiv.org/abs/2604.04978) stress-tested Claude Code's auto mode earlier this year and reached a similar conclusion.

## Why this happens

I don't think any of this is a bug in one product. It follows from how the approval layer is designed.

The layer is optimized for fewer prompts. If the main metric is how often a human gets interrupted, it will be tuned to approve ordinary-looking commands quickly, and ordinary-looking commands are exactly where hidden behavior lives.

Not seeing is also partly a choice. Claude Code's classifier sees the user's messages and the agent's tool calls, but tool results are stripped out so that hostile text in a file cannot talk the classifier into anything. That is a sensible defense against prompt injection, and its cost is that the classifier cannot see what a script contains either. Codex's reviewer sees more, including tool outputs, but it is only consulted when an action asks to leave the sandbox. Anything the sandbox already allows runs without review. Both designs give up visibility to get something else.

Attaching rules to tools also creates detours, because the same effect can often be reached through a tool that is gated differently. In one run, the classifier blocked a shell command that wrote a script to a file. The agent then used its file-writing tool to write the same script, which was approved, and the effect followed.

Finally, the sandbox is a real boundary, but the workspace is inside it. A sandbox that limits writes to the project and turns the network off by default is a strong baseline, and I would not run an agent without one. By design, though, it lets the agent change files in the workspace, start processes, and use local resources. In my scenarios, local service connections, resource exhaustion, file writes and lingering processes went through between 74% and 100% of the time. The network was where the agent's own caution helped most, and it is also the boundary people most often switch off to get work done.

## What it would take to rely on more than the sandbox

If the approval layer cannot see effects, a better reader of commands will not fix it. The approver needs to be given something closer to the effect.

That is the idea behind Caper, the system in our paper: run each command first in a snapshot of the workspace, record what it actually did, show that record to an approver, and keep or roll back the result. It is one point in the design space, and it has real costs. It adds latency, it sees one execution rather than every possible one, and it cannot catch behavior that only triggers later.

Other pieces seem just as important to me. One is to watch the small set of auto-execution points. Test configurations, build files, git hooks, startup files and CI definitions are where an innocent command turns into someone else's code. The list is short, and a deterministic check on changes to it is cheap. Another is to grant capabilities per task. A task that runs the tests does not need the network or access to secrets, and scoping those per task shrinks what any hidden code can do.

It also helps to follow sensitive data instead of commands. A process that reads a credential and then opens a connection is worth stopping, whatever the command that started it looked like. And agents should keep being trained to reason about effects. The agent's own judgment did most of the blocking in my runs, though it only works on what the agent can see.

None of these is enough alone, and each covers a channel the others miss. The approval layer makes agents less annoying to use, and the sandbox gives them a boundary. What is still missing between the two is a layer that looks at what a command does, not only at what it says.
