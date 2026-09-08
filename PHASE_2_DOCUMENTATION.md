# LLP V1 — Phase 2 Superior Manager Documentation

## 1. Purpose

Phase 2 extends the LLP V1 orchestration layer by refactoring the existing Supervisor concept into a **Superior Manager** responsible for request analysis, route selection, strategy selection, and coordination of downstream processing.

The target storyboard architecture is:

```text
User Input
   ↓
Input Validation
   ↓
Context / Memory
   ↓
Superior Manager
   ↓
Grammar + Vocabulary + Cultural Bridge
   ↓
Confidence Coach + Audit Agent
   ↓
Superior Manager
   ↓
Final Response
```

The storyboard defines the Superior Manager acceptance criteria as:
1. Route input to all five agents, with Grammar/Vocabulary/Cultural Bridge as the first stage.
2. Add second-stage routing to Confidence Coach and Audit Agent after the first-stage merge.
3. Merge structured outputs without field collisions.
4. Run full regression testing across the five-agent pipeline.

## 2. Current LLP V1 Implementation

The current backend uses FastAPI and the existing LLP service architecture. Phase 2 work currently introduces:

- `backend/app/services/superior_manager.py`
- `manager_decision` in `backend/app/models/agent_context.py`
- Superior Manager decision metadata in `AgentController`

The current Superior Manager performs:

- Intent analysis
- Route selection
- Strategy selection
- Decision metadata generation

### Supported routes

| Route | Intent examples | Strategy |
|---|---|---|
| TOOL | Vocabulary, Word of Day, Synonyms, Antonyms, Translation, Pronunciation, Cultural | Use tool |
| LLM | Grammar, Conversation, Daily Phrases, Cultural Bridge | Use LLM + memory |
| PLANNING | Learning Plan, Roadmap, Current Day, Progress | Use planning + memory |
| GENERAL | Other/unknown requests | General LLM + memory |

## 3. Decision Contract

The Superior Manager returns a structured decision:

```json
{
  "intent": "VOCABULARY",
  "confidence": 1.0,
  "route": "TOOL",
  "strategy": {
    "route": "TOOL",
    "use_tools": true,
    "use_memory": false,
    "use_planning": false
  }
}
```

This decision is stored in `AgentContext.manager_decision` and exposed through response metadata where the common AgentController response path is used.

## 4. Phase 1 Integration Status

Cultural Bridge Agent work was implemented using the locally available Ollama model rather than Mistral Saba, because Mistral Saba was not available in the local environment.

Current local model used for the Cultural Bridge implementation:

```text
ministral-3:8b
```

The agent was tested for:
- Telugu-English influenced phrasing
- Literal translations
- Professional English that should remain unchanged

Example:

```text
Input:
Yesterday itself I completed the work.

Improved:
I completed the work yesterday.
```

The implementation preserves the intended meaning and returns the required Cultural Bridge fields:

```json
{
  "issue": "...",
  "original": "...",
  "improved": "...",
  "reason": "..."
}
```

## 5. Validation Completed

Phase 1 functional tests completed successfully for:

- Grammar
- Vocabulary
- Translation
- Cultural Bridge
- Tool routing
- Frontend/backend connectivity

Translation was additionally validated after the translation-tool fallback handling was corrected.

Reflection/quality validation was improved for translation and vocabulary responses.

## 6. Phase 2 Work Completed So Far

### Completed

- Created `SuperiorManager`.
- Added intent-to-route mapping.
- Added tool, LLM, planning and general strategies.
- Integrated the manager into `AgentController`.
- Added `manager_decision` to `AgentContext`.
- Added manager decision metadata to the common response path.
- Verified routing for Vocabulary, Translation and Grammar.
- Verified the manager independently identifies Learning Plan as a planning route.

### Remaining

The current Phase 2 implementation is a routing foundation and is **not yet the final five-agent Superior Manager pipeline** described in the storyboard.

Remaining work:

1. Avoid duplicate intent analysis between `AgentController` and `SuperiorManager`.
2. Extend the manager from route selection to first-stage agent dispatch.
3. Add structured merge handling for Grammar, Vocabulary and Cultural Bridge outputs.
4. Add second-stage Confidence Coach and Audit routing when those agents are available.
5. Add final response assembly with collision-safe structured outputs.
6. Complete full-pipeline regression testing.

## 7. Testing Strategy

The storyboard specifies the following validation sequence for new agents:

```text
Unit Test
   ↓
Prompt Test
   ↓
Edge Case Test
   ↓
Model Output Validation
   ↓
CrewAI Integration Test
   ↓
End-to-End Test
```

For the Superior Manager, additional tests should cover:

- Correct intent classification
- Correct route selection
- Correct strategy flags
- Structured manager decision output
- Tool route execution
- LLM route execution
- Planning route execution
- Unknown/general requests
- First-stage merge behavior
- Second-stage routing
- Final response assembly
- No field collisions between agent outputs

## 8. Known Technical Constraints

### Local model availability

The storyboard specifies Mistral Saba for Cultural Bridge, but it was not available locally. The implementation therefore uses the available Ollama Ministral model for development and validation.

### External translation service

The translation tool encountered an external Google translation rate-limit condition (HTTP 429). Fallback handling was added so translation can continue through the available fallback path.

### Local inference latency

Ollama model inference can be slow on the development machine. This affects response latency but does not currently prevent functional testing.

## 9. GitHub

Repository:

`https://github.com/sunanda2601/LLP_Project`

## 10. Next Development Target

The immediate goal is to complete the Superior Manager orchestration refactor and then run the full regression test required for the Phase 2 acceptance criteria.

Target completion window: **September 11, 2026**.
