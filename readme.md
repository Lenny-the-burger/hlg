# Hierarchical Language Generator

### 1. Syntax Stage

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

Yes this project is a visual studio solution sue me. Its only 3 files and probably a bunch of python scripts for training.
