[简体中文](./README.zh.md) | **English**

# KongQuYingZhi
**White-box Text System · Sentence-level Reasoning · No Matrix Computation**

## Core Thesis
The essence of linguistic intelligence is **the recognition and reuse of structures (syntax, causality, logic)**, not statistical fitting of word frequencies.

## Design Goals
- Single-sentence generation < 50ms (on CPU)
- Corpus compression ratio > 100
- Hardware: consumer-grade PC (AMD 3900X + Arc B580)
- No context window limit (database-level persistence)
- Hardware-friendly: ~0.1–0.3× hardware cost, <0.001× training cost compared with Transformer

## Comparison with Transformer

| Dimension | Transformer | KongQuYingZhi |
|---|---|---|
| Reasoning unit | token | **sentence** |
| Knowledge storage | weight matrices (black-box) | tag libraries + enum libraries (white-box) + structured high-compression original-text DB |
| Context | window truncation | **database retrieval** |
| Training | GPU clusters, weeks | single machine, one-pass traversal |
| Logic source | statistical emergence | **hard-coded causal/logic templates** |

## Core Components
- Two-tier statistics (structure layer + word-frequency layer)
- Cognition / Forgetting / Spacetime / Propagation engines
- Tag indexing + hierarchical retrieval (B+Tree / HNSW)
- General enum libraries (causal templates, logic templates, grammar templates)

## Current Status
V2 engineering in progress, 30k-word blueprint. Validation datasets scale from 1GB to 2TB. Acceptance benchmark: MiniCPM5-1B.

## Notes
I am not fluent in English. Please use an LLM to translate the documentation before reading.
Updates will focus on the Chinese version of docs. You may use AI translation.
Do not ask the translator to over-interpret or over-reason. Tell the AI to stick strictly to the literal meaning of the text.
