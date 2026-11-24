[简体中文](./README.zh.md) | **English**
# KongQuYingZhi
**White-box Multimodal System · Sentence-level Reasoning · No Matrix Computation in Text Pipeline · Transformer-free Paradigm**

## Core Thesis
Linguistic intelligence lies in recognition and reuse of structures (syntax, causality, spacetime logic), not statistical fitting of word frequencies.
Based on *Four-Image Linguistics*. The framework theoretically supports all human languages. It unifies text, image, audio and video under one cognitive foundation.

## Design Goals
- Single sentence generation on CPU < 50 ms
- Corpus compression ratio > 100
- Hardware: consumer PC (AMD 3900X + Arc B580)
- No context window limit, database persistence
- Hardware cost: 0.1–0.3 × Transformer; training cost < 0.001 × Transformer

## Paradigm Comparison
| Dimension | Transformer | KongQuYingZhi |
|---|---|---|
| Reasoning unit | Token | **Sentence** |
| Knowledge storage | Weight matrices (black-box) | Tag library, enum library (white-box) + high-compression structured text database |
| Context | Window truncation | **Database retrieval** |
| Training | GPU clusters, weeks | Single machine, one-pass traversal |
| Logic source | Statistical emergence | **Native causal, logic and grammar templates** |
| Multimodal | Separate encoders | **Unified Four-Image mapping** |

## Core Modules
- Two-tier statistics: structure layer / word-frequency layer
- Cognition, Forgetting, Spacetime, Propagation engines
- Tag indexing + hierarchical retrieval (B+Tree / HNSW)
- Enum libraries: causal, logic, *Four-Image Linguistics* grammar templates
- Multimodal mapper: convert image, audio, video into Four-Image structures

## Current Status
Aug 13, 2026: Theory started
Nov 25, 2026: This version timestamped
*Four-Image Linguistics* is the foundation of text AI, built in three months and decoupled from existing grammar systems.
Text-image-audio-video integration finished, engineering phase started.
30k-word blueprint. Validation dataset: 1GB → 2TB. Benchmark: MiniCPM5-1B.

## Notes
My English is not proficient. Use LLM translation.
Prioritize Chinese docs. Tell translator to stick to literal meaning.

## License Notice
Copy & redistribution permitted with clear author, project and timestamp attribution. Removing authorship or falsifying origin is forbidden. Closed-source commercial use and derivative patent applications require written permission.

## Notes
I am not fluent in English. Please use an LLM to translate the documentation before reading.
Updates will focus on the Chinese version of docs. You may use AI translation.
Do not ask the translator to over-interpret or over-reason. Tell the AI to stick strictly to the literal meaning of the text.
