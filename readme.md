# Hierarchical Language Generator

Hierarchical Language Generator is a lightweight alternative to transformer-based language models. HLG generates text using hierarchical submodel selection, probabilistic lookup tables, and a shared embedding space (like GloVe or fastText).

**Design Goals:**
- **CPU-friendly**: No GPU or massive VRAM required
- **Fast inference**: Significantly faster generation than transformer models
- **Low memory footprint**: Uses pre-trained static embeddings instead of billions of parameters
- **Interpretable**: The submodel tree and selection process can be inspected and debugged
- **Controllable**: Explicit injection points for context and constraints at every stage

HLG trades some flexibility for efficiency - it won't match GPT-4's general capability, but it can generate high-quality text in well-defined domains with a fraction of the computational cost.

## Core Architecture

HLG uses a **shared embedding space** (like GloVe or fastText) that all components reference. Every submodel, token, word root, and context representation exists in this same semantic space. This enables intelligent selection and generation at every level without requiring large neural networks.

**Context Vectors**: Throughout generation, the system maintains context from multiple sources:
- User prompt (extracted directly or via logical rules)
- Global/section/paragraph-level context
- Moving average of recently generated tokens
- Metadata passed down from higher-level submodels

All stages use these context vectors to make embedding-space decisions rather than purely statistical ones.

## Submodel Types

HLG supports two types of submodels that are selected and invoked identically:

### Generative Submodels
Traditional statistical generation using probabilistic lookup tables and embedding-space evaluation. These generate text based on learned patterns.

### Procedural Submodels
**Executable code** that produces structured tokens. These can:
- Read files (CSV, logs, JSON)
- Query databases
- Call APIs
- Execute code snippets
- Parse data structures
- Perform calculations

Procedural submodels advertise themselves via context vectors just like generative ones (e.g., CSV reader: `mean(["csv", "file", "data", "spreadsheet"])`). The selection mechanism doesn't care whether a submodel generates statistically or procedurally - both emit tokens with metadata that flow through the pipeline.

**Example use cases:**
- `{csv_reader path="sales.csv"}` → reads file → emits `{csv_headers}{csv_rows}`
- `{parse_logs path="/var/log" since="24h"}` → parses logs → emits `{error_count n=3}{errors}`
- `{weather_api city="Boston"}` → fetches weather → emits structured weather tokens

This enables **hybrid generation**: rigid procedural structure with flexible AI-generated summaries and explanations.

## Three-Stage Pipeline

### 1. Structural Stage (formerly "Syntactic")

This stage builds a **tree of submodels** from the input, starting with high-level orchestrators and recursively selecting more specific submodels until reaching atomic token generators.

**Process:**
1. Top-level submodel selection: Compare user prompt against orchestrator submodels (e.g., "code creator" vs "creative writer") using context vectors in embedding space. Selection is statistical, not "closest wins"
2. Selected submodel generates section tokens with metadata (e.g., `{greeting}{main_response}{conclusion}`)
3. For each token, select compatible submodels using context vectors + metadata
4. Recurse until reaching atomic-level submodels that emit single meaning units (word roots)

**Top-level orchestrators can be procedural**, enabling deterministic workflows. For example, a daily report orchestrator might always emit: `{parse_logs}{check_disk_usage}{query_metrics}{generate_summary}` - the first three are procedural, the last is generative.

**Example:** "Write me a haiku" → selects "creative writer" → generates sections → selects "haiku writer" for main response → generates haiku structure tokens

**Output:** Complete tree of submodels with atomic tokens at the leaves, plus metadata for downstream stages

### 2. Semantic Stage

This stage converts atomic structural tokens into **word roots** (pure semantic meaning, no grammar).

**Process:**
1. Each atomic-level submodel has a domain-specific probabilistic lookup table (like a markov chain but simpler)
2. Lookup table proposes candidate word roots
3. Candidates are evaluated against context vectors (global, metadata from Structural stage, local moving average) in the embedding space
4. Best semantic match is selected
5. Semantic stage can inject additional context vectors for generalized control (e.g., vocabulary constraints for emails)

**Output:** Word roots representing pure meaning, 1:1 with atomic tokens from Structural stage

### 3. Cohesion Stage

This stage transforms word roots into **final fluent text** with full grammatical freedom.

**Process:**
1. Works similarly to Semantic stage but with greater flexibility
2. Can modify tokens, insert additional words, adjust phrasing
3. "Joins the branches" - merges outputs from different submodels into coherent text
4. Uses metadata from previous stages to guide stylistic choices

**Example:** `{dog}{sit}{mat}` → "The dog sits on the mat." or "A dog is sitting on a mat."

**Output:** Final generated text

## Stage Execution

Stages run **sequentially and completely**:
1. Structural stage fully expands the entire response tree
2. Semantic stage processes all atomic tokens in one pass
3. Cohesion stage generates final text from all word roots

This is not token-by-token generation - each stage completes its full transformation before the next begins.

Each stage is trained independently, and mat be tweaked independently. Each stage is also trained differently. More on training below.

## Use Cases

### Interactive Chat
Run a capable chatbot entirely On your machine. No gpu required.

### Automated Reports
Generate daily/weekly reports by combining procedural data gathering with AI-generated summaries.
- System health monitoring
- Security alert digests
- Sales/analytics reports
- Code review summaries

**Example:** Cron job triggers HLG → procedural SMs parse logs/query databases → generative SM writes natural summary → report emailed to admin. Runs in seconds, costs nothing, requires no GPU.

### Embedded Systems
HLG is designed for constrained environments:
- Runs entirely on CPU with minimal RAM
- No internet required (static embeddings)
- Deterministic behavior (procedural SMs guarantee outputs stay in bounds)
- Perfect for spacecraft, IoT devices, or any system where reliability > flexibility

### Enterprise Data Narration
Turn structured data into natural language without sending sensitive information to external APIs:
- Parse internal databases
- Generate compliance documents
- Create customer-facing reports
- Explain complex data pipelines

## Usage
This library is written in C. The two main files you have to care about are `hlg.h` and `hlg.c`. `main.cpp` is mostly just an example of how to use the library and to help with development. You dont need it.

Submodel API coming soon - write custom generative or procedural submodels in Python or JavaScript.

Yes this project is a visual studio solution sue me. Its only 3 files and probably a bunch of python scripts for training.

Yes this readme was slopped together using claude but im probably no better at explaining this than it is.