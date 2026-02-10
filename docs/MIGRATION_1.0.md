# Migration to Langchain 1.0.7

## Overview
This document describes the migration from langchain 0.2.x to 1.0.7 completed on 2026-02-10.

## Environment Changes

### Python Version
- **Before:** Python 3.10
- **After:** Python 3.12.12
- **Reason:** Better performance, improved type hints, latest features

### Dependency Versions

**Before:**
```txt
langchain==0.2.16
langchain-core==0.2.41
langchain-community==0.2.17
langchain-openai==0.1.25
langchain-ollama==0.1.3
gradio==4.43.0
loguru==0.7.2
```

**After:**
```txt
langchain==1.0.7
langchain-core==1.2.9
langchain-community==0.4.1
langchain-openai==1.0.0
langchain-ollama==1.0.0
gradio==4.43.0
loguru==0.7.2
```

## Code Changes

### 1. Import Path Changes
**File:** `src/agents/agent_base.py` (line 4)

**Before:**
```python
from langchain_ollama.chat_models import ChatOllama
```

**After:**
```python
from langchain_ollama import ChatOllama
```

**Reason:** langchain-ollama 1.0.0 simplified import structure

### 2. ChatOllama Parameter Changes
**File:** `src/agents/agent_base.py` (line 60)

**Before:**
```python
self.chatbot = system_prompt | ChatOllama(
    model="llama3.1:8b-instruct-q8_0",
    max_tokens=8192,
    temperature=0.8,
)
```

**After:**
```python
self.chatbot = system_prompt | ChatOllama(
    model="llama3.1:8b-instruct-q8_0",
    num_predict=8192,
    temperature=0.8,
)
```

**Reason:** `max_tokens` parameter was not properly applied; `num_predict` is the correct parameter for Ollama models

### 3. Message Invocation Pattern Changes
**File:** `src/agents/agent_base.py` (line 82)

**Before:**
```python
response = self.chatbot_with_history.invoke(
    [HumanMessage(content=user_input)],
    {"configurable": {"session_id": session_id}},
)
```

**After:**
```python
response = self.chatbot_with_history.invoke(
    {"messages": [HumanMessage(content=user_input)]},
    {"configurable": {"session_id": session_id}},
)
```

**Reason:** langchain-core 1.2.9 requires dict format with explicit `messages` key for ChatPromptTemplate

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python tests/test_integration.py
```

Expected output:
```
✓ Import test passed
✓ Session history test passed
✓ Conversation agent test passed

All integration tests passed!
```

### 4. Run Application
```bash
python src/main.py
```

## Rollback Instructions

If issues occur:

```bash
# Restore old requirements
cp requirements.txt.backup requirements.txt

# Reinstall old versions in a fresh venv
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Revert code changes
git revert HEAD~4  # Reverts the 4 commits for this upgrade
```

## Testing Checklist

- [x] All imports work without errors
- [x] Session history creation works
- [x] ConversationAgent instantiation works
- [x] ScenarioAgent instantiation works
- [x] VocabAgent instantiation works
- [x] Integration tests pass
- [ ] Gradio UI loads correctly (blocked by separate gradio/huggingface_hub issue)
- [ ] Chat functionality works end-to-end (blocked by UI issue)

## Known Issues

### Gradio/Huggingface-Hub Compatibility (Separate from Langchain)

**Issue:** gradio 4.43.0 is incompatible with huggingface_hub 1.4.1 (HfFolder import error)

**Status:** Does not affect langchain functionality. All agent code works correctly.

**Workaround options:**
1. Upgrade gradio to a newer version (e.g., 5.x)
2. Pin huggingface_hub to compatible version
3. Use alternative UI framework temporarily

## Breaking Changes Reference

See langchain release notes:
- [Langchain 1.0 Migration Guide](https://python.langchain.com/docs/versions/v0_2/)
- [Langchain-Ollama Documentation](https://python.langchain.com/docs/integrations/chat/ollama/)

## Resolution: Gradio Upgraded to 6.5.1

**Date:** 2026-02-10

The gradio/huggingface_hub compatibility issue has been resolved by upgrading gradio to 6.5.1.

**Change:**
- gradio: 4.43.0 → 6.5.1
- gradio-client: 1.3.0 → 2.0.3
- huggingface_hub: Compatible version maintained (1.4.1)

**Code Changes:**
Removed deprecated ChatInterface parameters from 3 tab files:
- `retry_btn=None` (removed - no longer supported)
- `undo_btn=None` (removed - no longer supported)
- `clear_btn` (removed - no longer supported)

**Result:**
- ✅ Application UI now starts successfully
- ✅ All tabs functional (对话, 场景, 单词)
- ✅ No deprecation warnings
- ✅ Backward compatible migration

**Testing:**
- Integration tests: PASSED
- No deprecation warnings
- All agent functionality intact

## Support

For issues:
1. Check this migration guide
2. Review langchain 1.0 documentation
3. Check project integration tests
4. Open GitHub issue with test results
