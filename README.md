[简体中文](./README.zh.md) | **English**

# KongQuYingZhi

**White-box Text System · Sentence-level Reasoning · No Matrix Computation**

## Core Thesis
The essence of linguistic intelligence is **the recognition and reuse of structures (syntax, causality, logic)** , not statistical fitting of word frequencies.

## Design Goals
- Single-sentence generation < 50ms (on CPU)
- Corpus compression ratio > 100
- Hardware: consumer-grade PC (AMD 3900X + Arc B580)
- No context window limit (database-level persistence)
- Hardware-friendly: ~0.3–0.1× hardware cost, <0.001× training cost vs. Transformer

## Comparison with Transformer

| Dimension | Transformer | KongQuYingZhi |
|---|---|---|
| Reasoning unit | token | **sentence** |
| Knowledge storage | weight matrices (black-box) | tag libraries + enum libraries (white-box) + structured + high-compression high-performance original-text DB |
| Context | window truncation | **database retrieval** |
| Training | GPU clusters, weeks | single machine, one-pass traversal |
| Logic source | statistical emergence | **hard-coded causal/logic templates** |

## Core Components
- Two-tier statistics (structure layer + word-frequency layer)
- Cognition / Forgetting / Spacetime / Propagation engines
- Tag indexing + hierarchical retrieval (B+Tree / HNSW)
- General enum libraries (causal templates, logic templates, grammar templates)

## Current Status
V2 engineering in progress, 30k-word blueprint. Validation datasets: 1GB → 2TB. Acceptance benchmark: MiniCPM5-1B.

## To Read
I am not fluent in English. Please use an LLM to translate doc before reading.
The update readme,will fouce on cn-doc version.You can easily read it by AI.I will not use stange words.
Pay attentin , tell AI to focus on the words-self-meaning , but not anything else,not deep think.
