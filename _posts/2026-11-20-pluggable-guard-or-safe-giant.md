---
title: "A Pluggable Guard or a Safe Giant? What Safety Alignment Should Aim For"
date: 2026-11-20
description: "Should safety live in a small model we can plug in anywhere, in a large model that is safe by itself, or in both?"
---

*This is a preview. The full post is coming soon.*

When we train models for safety, what exactly are we aiming for? One option is a small model that can be plugged in next to any agent: fast, cheap, and easy to update, but it only sees part of the picture. The other is a large model that carries safety through the whole task: it has the full context, but it is slow, costly, and hard to update on its own.

In this post I want to compare what each one needs from training and what each one gives back, and ask whether the right answer is one, the other, or both.
