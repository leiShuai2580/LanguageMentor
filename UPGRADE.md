# LanguageMentor 依赖升级总结

**日期:** 2026-02-10
**Python 版本:** 3.12.12
**Langchain 版本:** 1.0.7
**Gradio 版本:** 6.5.1
**状态:** ✅ 完成并正常运行

---

## 概述

本次升级包含两个主要阶段：

1. **Langchain 升级** (0.2.16 → 1.0.7) - 配合 Python 3.12.12
2. **Gradio 升级** (4.43.0 → 6.5.1) - 解决兼容性问题

两次升级均已完成，所有功能测试通过，应用程序运行正常。

---

## 一、依赖版本变更

### 第一阶段：Langchain 升级

| 包名 | 升级前 | 升级后 | 变更类型 |
|------|--------|--------|----------|
| Python | 3.10 | 3.12.12 | 大版本升级 |
| langchain | 0.2.16 | 1.0.7 | 大版本升级 |
| langchain-core | 0.2.41 | 1.2.9 | 大版本升级 |
| langchain-community | 0.2.17 | 0.4.1 | 小版本升级 |
| langchain-openai | 0.1.25 | 1.0.0 | 大版本升级 |
| langchain-ollama | 0.1.3 | 1.0.0 | 大版本升级 |
| loguru | 0.7.2 | 0.7.2 | 保持不变 |
| gradio | 4.43.0 | 6.5.1 | 修复 huggingface_hub 兼容性 |
| gradio-client | 1.3.0 | 2.0.3 | 随 gradio 自动升级 |
| huggingface_hub | 1.4.1 | 1.4.1 | 保持兼容 |

---

## 二、版本兼容性分析

### Langchain 核心约束

Langchain 1.0.7 要求 `langchain-core<2.0.0,>=1.0.4`，这导致需要升级所有集成包：

1. **langchain-community**
   - 0.3.x 要求 langchain-core<0.4.0 ❌ 不兼容
   - 0.4.1 要求 langchain-core<2.0.0,>=1.0.1 ✅ 兼容

2. **langchain-openai**
   - 0.2.14 要求 langchain-core<0.4.0 ❌ 不兼容
   - 1.0.0 要求 langchain-core<2.0.0,>=1.0.0 ✅ 兼容

3. **langchain-ollama**
   - 0.2.3 要求 langchain-core<0.4.0 ❌ 不兼容
   - 1.0.0 要求 langchain-core<2.0.0,>=1.0.0 ✅ 兼容

### Gradio 兼容性问题

**问题：** Langchain 升级后，gradio 4.43.0 与 huggingface_hub 1.4.1 不兼容
```
ImportError: cannot import name 'HfFolder' from 'huggingface_hub'
```

**原因：** gradio 4.43.0 依赖已被移除的 `HfFolder` 类（在 huggingface_hub 0.20.0+ 版本中删除）

**解决方案：** 升级到 gradio 6.5.1，该版本与现代 huggingface_hub 版本兼容

---

## 三、代码变更

### Langchain 相关变更（3处）

#### 1. 导入路径更新
**文件：** `src/agents/agent_base.py` (第4行)

**修改前：**
```python
from langchain_ollama.chat_models import ChatOllama
```

**修改后：**
```python
from langchain_ollama import ChatOllama  # 更新导入路径以支持 langchain 1.0
```

**原因：** langchain-ollama 1.0.0 简化了导入结构

---

#### 2. ChatOllama 参数更新
**文件：** `src/agents/agent_base.py` (第60行)

**修改前：**
```python
self.chatbot = system_prompt | ChatOllama(
    model="llama3.1:8b-instruct-q8_0",
    max_tokens=8192,
    temperature=0.8,
)
```

**修改后：**
```python
self.chatbot = system_prompt | ChatOllama(
    model="llama3.1:8b-instruct-q8_0",
    num_predict=8192,  # 正确设置 token 限制
    temperature=0.8,
)
```

**原因：** `max_tokens` 参数未被正确应用；`num_predict` 是 Ollama 模型的正确参数

---

#### 3. 消息调用模式更新
**文件：** `src/agents/agent_base.py` (第82行)

**修改前：**
```python
response = self.chatbot_with_history.invoke(
    [HumanMessage(content=user_input)],
    {"configurable": {"session_id": session_id}},
)
```

**修改后：**
```python
response = self.chatbot_with_history.invoke(
    {"messages": [HumanMessage(content=user_input)]},  # 字典格式
    {"configurable": {"session_id": session_id}},
)
```

**原因：** langchain-core 1.2.9 的 ChatPromptTemplate 要求使用字典格式，带有显式的 `messages` 键

---

### Gradio 相关变更（3个文件）

#### 移除已废弃的 ChatInterface 参数

Gradio 6.5.1 移除了以下 ChatInterface 参数：
- `retry_btn` (重试按钮)
- `undo_btn` (撤销按钮)
- `clear_btn` (清除按钮)

**修改的文件：**

1. **`src/tabs/conversation_tab.py`** (第33-35行)
2. **`src/tabs/scenario_tab.py`** (第71-73行)
3. **`src/tabs/vocab_tab.py`** (第74-76行)

**修改示例：**

**修改前：**
```python
gr.ChatInterface(
    fn=handle_func,
    chatbot=chatbot_component,
    retry_btn=None,  # ← 删除此行
    undo_btn=None,   # ← 删除此行
    clear_btn="清除历史记录",  # ← 删除此行
    submit_btn="发送",
)
```

**修改后：**
```python
gr.ChatInterface(
    fn=handle_func,
    chatbot=chatbot_component,
    submit_btn="发送",
)
```

**原因：** Gradio 6.5.1 API 不再支持这些参数

---

## 四、文件变更清单

### 新增文件

1. **测试文件**
   - `tests/__init__.py`
   - `tests/test_integration.py`

2. **文档文件**
   - `UPGRADE.md` - 本文件（中文升级总结）

3. **辅助文件**
   - `activate_env.sh` - 虚拟环境激活脚本


### 修改文件

1. **依赖文件**
   - `requirements.txt` - 更新所有依赖版本

2. **源代码文件**
   - `src/agents/agent_base.py` - Langchain API 更新（3处）
   - `src/tabs/conversation_tab.py` - 移除废弃 Gradio 参数
   - `src/tabs/scenario_tab.py` - 移除废弃 Gradio 参数
   - `src/tabs/vocab_tab.py` - 移除废弃 Gradio 参数

3. **文档文件**
   - `README.md` - 添加激活脚本使用说明

---

## 五、测试结果

### 集成测试
✅ **全部通过**
- 导入测试：通过
- 会话历史测试：通过
- 对话代理测试：通过

### 组件测试
✅ **代理功能验证**
- AgentBase 工作正常
- ConversationAgent 实例化正常
- ScenarioAgent 实例化正常
- VocabAgent 实例化正常
- 会话历史管理正常

### 应用程序启动
✅ **成功启动**
- Langchain 组件：正常工作
- 代理创建：正常工作
- Gradio UI：正常启动
- 运行地址：http://0.0.0.0:7860

### UI 功能测试
✅ **全部功能正常**
- **对话标签页**：聊天机器人和消息发送正常
- **场景标签页**：场景选择和聊天正常
- **单词标签页**：词汇学习和按钮功能正常

### 警告/弃用检查
✅ **无警告** - 干净升级，无弃用警告

---

## 六、升级收益

### 兼容性
- ✅ 所有依赖现在能够协同工作
- ✅ 与现代生态系统兼容

### 性能
- ✅ Python 3.12 性能改进
- ✅ Langchain 1.0.7 优化的 API
- ✅ Gradio 6.5.1 改进的渲染速度

### 稳定性
- ✅ 两个大版本更新带来的错误修复
- ✅ 更好的错误处理和消息

### 可维护性
- ✅ 使用支持的版本，便于未来更新
- ✅ 更清晰的 API 和更好的文档

### 功能特性
- ✅ 访问两个框架的最新功能
- ✅ 改进的 ChatInterface 功能
- ✅ 更好的类型提示和开发体验

---

## 七、总结

### 升级状态
✅ **升级成功完成**

### 关键成就
- ✅ 依赖升级无冲突
- ✅ 识别并修复所有破坏性更改
- ✅ 创建集成测试并通过
- ✅ 提供完整文档
- ✅ UI 完全正常运行

### 技术栈现状

LanguageMentor 现在运行在：
- **Python 3.12.12** - 最新稳定版
- **Langchain 1.0.7** - 改进的 API 和性能
- **Gradio 6.5.1** - 现代 UI 框架
- **所有依赖兼容** - 稳定的生态系统