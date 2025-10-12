#pragma once

#include <stddef.h>
#include <stdio.h>

// Include this header to use HLG.
#ifdef __cplusplus
extern "C" {
#endif

// Error codes
#define HLG_ERROR_NULL_POINTER    -1
#define HLG_ERROR_FILE_OPEN       -2
#define HLG_ERROR_ALLOCATION      -3
#define HLG_ERROR_NOT_INITIALIZED -4

#pragma region Structures

// Struct that hold embedding data. Uses streaming.
typedef struct {
    char* filename;    // Path to the embeddings file
    size_t dim;       // Dimension of the embeddings

    void* cache;     // Pointer to cache structure
    size_t cache_size; // Size of the cache in bytes
} HLG_Embedding;

// ======================= Configuration for each stage =======================

// ============================== Syntax Stage ================================

// Per layer markov chain
typedef struct {
    // for now this is always a trigram. In the future it should be n length
    int num_grams;
} HLG_Y_MarkovChain;

// A syntactic layer
typedef struct {
    HLG_Y_MarkovChain chain;
	char* upstream_vocab;   // string name of vocab file that feeds into the chain
    char* downstream_vocab; // string name of vocab file that the chain produces
} HLG_Y_Layer;

typedef struct {
	int num_layers;          // Number of syntactic layers
	int* layer_sizes;
    HLG_Y_Layer* layers; // Array of markov chains for each layer
} HLG_SyntaxCfg;

// =============================== Semantic Stage =============================

// Similar to a markov chain but uses embeddings to select next word
typedef struct {
    int num_grams;
} HLG_E_CandidateMapping;

// Semantic stage does not have layers, just multiple domain-specific chains in series
typedef struct {
    int num_chains;          // Number of domain-specific chains
    HLG_E_CandidateMapping* chains; // Array of candidate mappings
	HLG_Embedding* embedding;      // Common general purpose embedding
} HLG_SemanticCfg;

// =============================== Cohesion Stage =============================

// Markov chain like candidate mapping
typedef struct {
    int num_grams;
} HLG_C_CandidateMap;

// A cohesion layer
typedef struct {
    HLG_C_CandidateMap map; // Candidate mapping for this layer
	int syntax_parent_layer; // Which syntactic layer this cohesion layer belongs to
} HLG_C_Layer;

typedef struct {
    int num_layers;          // Number of cohesion layers
    HLG_C_Layer* layers;     // Array of cohesion layers
} HLG_CohesionCfg;

// ============================ Main Structures ===============================

// Options for creating an HLG instance
typedef struct {
    const char* syntactic_model_path;  // Path to syntactic markov chains
    const char* semantic_model_path;   // Path to semantic chains + embeddings
    const char* cohesion_model_path;   // Path to cohesion chains
    const char* embeddings_path;       // Path to embeddings file

    size_t syntactic_layers;           // Number of syntactic layers (default: 2)
    size_t cohesion_layers;            // Number of cohesion layers (default: 1)
    size_t embedding_cache_size;       // Size of embedding cache in MB
} HLG_Options;

// Main HLG instance - manages the three-stage pipeline
typedef struct {
    int initialized;             // Flag to check if properly initialized

	HLG_SyntaxCfg syntax;        // Syntactic stage configuration
	HLG_SemanticCfg semantic;    // Semantic stage configuration
	HLG_CohesionCfg cohesion;    // Cohesion stage configuration
} HLG;

// Context for a generation session
// Not strictly a conversation, but any series of generations where context is preserved
typedef struct {
    char** history;              // Previous outputs for context
    size_t history_count;        // Number of items in history
    size_t history_capacity;     // Allocated capacity

    float* context_vector;       // Aggregated context embedding
    size_t context_dim;          // Dimension of context vector

	HLG* hlg;                    // Pointer back to the main HLG instance
} HLG_Conversation;

#pragma endregion
#pragma region API Functions

// Initialize an HLG instance with the given options
// Returns 0 on success, negative error code on failure
int hlg_init(HLG* hlg, const HLG_Options* options);

// Clean up resources used by an HLG instance
void hlg_cleanup(HLG* hlg);

// Initialize a conversation/generation context
// Returns 0 on success, negative error code on failure
int hlg_conversation_init(HLG_Conversation* convo, size_t context_dim);

// Clean up a conversation context
void hlg_conversation_cleanup(HLG_Conversation* convo);

// Add a prompt to the conversation context
void hlg_conversation_add_prompt(HLG_Conversation* convo, const char* prompt);

// Generate text using the HLG pipeline
// Output is written to the provided buffer
// Returns number of bytes written, or negative error code
int hlg_generate(HLG* hlg, HLG_Conversation* convo, char* output, size_t output_size);

#pragma endregion

#ifdef __cplusplus
}
#endif