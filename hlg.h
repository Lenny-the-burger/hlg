#pragma once

// Include this header to use HLG.
#ifdef _cplusplus
extern "C" {
#endif

// The important thing. Dont copy this around too much as it need to keep trck
// of big fat embeddings files.
typedef struct HLG;

typedef struct HLG_Options;

// This isnt strictly a back and forth conversation, but just any series of
// generations by the model where you might want to preserve context.
typedef struct HLG_Conversation;

#ifdef _cplusplus
}
#endif