# Gradio 6.5.1 Upgrade Design

**Date:** 2026-02-10
**Status:** Approved
**Goal:** Upgrade Gradio from 4.43.0 to 6.5.1 to resolve huggingface_hub compatibility issue

## Problem Statement

After the langchain 1.0.7 upgrade, gradio 4.43.0 became incompatible with huggingface_hub 1.4.1:
- **Error:** `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`
- **Root Cause:** gradio 4.43.0 expects `HfFolder` class which was removed in huggingface_hub 0.20.0+
- **Impact:** Application UI cannot start (agent functionality unaffected)

## Solution: Upgrade to Gradio 6.5.1

Gradio 6.5.1 is compatible with modern huggingface_hub versions and includes improvements to core APIs.

## Upgrade Strategy

**Approach:** Fast iteration with immediate feedback

**Rationale:**
1. Code uses basic, stable Gradio APIs (Chatbot, ChatInterface, Blocks, Tab)
2. Core components have strong backward compatibility
3. Breaking changes will surface immediately at startup
4. Faster to fix actual issues than predict theoretical ones

**Risk Level:** Low
- Simple Gradio usage (no advanced features)
- Core APIs are stable across versions
- Virtual environment isolation
- Git rollback available

## Current Gradio Usage

**Features Used:**
- `gr.Blocks` - App container
- `gr.Tab` - Tab navigation (3 tabs: 对话, 场景, 单词)
- `gr.Markdown` - Text content
- `gr.Chatbot` - Chat display with `placeholder`, `height`, `value`
- `gr.ChatInterface` - Chat interaction with `fn`, `chatbot`, buttons, `additional_inputs`
- `gr.Radio` - Scenario selection
- `gr.ClearButton` - Reset button
- Component events: `.change()`, `.click()`

**Files:**
- `src/main.py` - App initialization with `gr.Blocks` and `.launch()`
- `src/tabs/conversation_tab.py` - Conversation interface
- `src/tabs/scenario_tab.py` - Scenario-based learning
- `src/tabs/vocab_tab.py` - Vocabulary practice

## Expected Outcomes

**Most Likely (90%):** ✅ App starts with no code changes
- Gradio 6.x maintains backward compatibility for basic features
- ChatInterface API improved but backward compatible
- Chatbot rendering enhanced but compatible

**Possible (8%):** ⚠️ Minor parameter adjustments needed
- Deprecated parameter warnings
- Button parameter names updated
- Layout tweaks for better rendering

**Unlikely (2%):** ❌ Significant refactoring required
- Major API changes (unlikely for core components)
- Would require deeper investigation

## Upgrade Steps

1. **Update requirements.txt**
   - Change: `gradio==4.43.0` → `gradio==6.5.1`
   - Let gradio manage huggingface_hub version

2. **Install in virtual environment**
   ```bash
   venv/bin/pip install gradio==6.5.1
   ```

3. **Smoke test application startup**
   ```bash
   venv/bin/python src/main.py
   ```
   - Verify app starts without errors
   - Check console for deprecation warnings

4. **Test each tab functionality**
   - **对话 (Conversation):** Send test message, verify response
   - **场景 (Scenario):** Select scenario, verify chat works
   - **单词 (Vocab):** Test word learning flow, verify "下一关" button

5. **Address any issues**
   - Fix errors as they appear
   - Update deprecated parameters if warned
   - Adjust code based on actual behavior

6. **Update documentation**
   - Add gradio upgrade to UPGRADE_REPORT.md
   - Note any code changes made

7. **Commit changes**
   ```bash
   git add requirements.txt [any code changes]
   git commit -m "chore: upgrade gradio to 6.5.1 to fix huggingface_hub compatibility"
   ```

## Risk Mitigation

**Backup & Rollback:**
- `requirements.txt.backup` exists from langchain upgrade
- Git history allows clean revert
- Virtual environment prevents system-wide impact

**Testing Strategy:**
- Start with basic startup test
- Progressive testing of each feature
- Manual UI interaction testing
- Check agent functionality still works

**Safety Net:**
- Integration tests verify agent code unaffected
- Langchain functionality independent of Gradio version
- Can rollback if critical issues found

## Success Criteria

- [x] Design approved
- [ ] gradio 6.5.1 installed
- [ ] Application starts without errors
- [ ] All three tabs render correctly
- [ ] Chat functionality works in all tabs
- [ ] No critical errors or warnings
- [ ] Changes committed to git

## Known Benefits of Gradio 6.x

1. **Improved ChatInterface** - More flexible API, better error handling
2. **Better Chatbot Rendering** - Enhanced message display
3. **Performance** - Faster rendering and updates
4. **Bug Fixes** - Numerous stability improvements from 4.x
5. **Modern Dependencies** - Compatible with current ecosystem

## References

- [Gradio 6.x Changelog](https://github.com/gradio-app/gradio/releases)
- [Gradio ChatInterface Docs](https://www.gradio.app/docs/chatinterface)
- Current issue: gradio/huggingface_hub compatibility
