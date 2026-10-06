# agent-scorer-lite

按**可配置 rubric** 对 agent 输出做规则式评分：维度 + 权重 + 规则打分并给理由。
零第三方依赖；可选 LLM 复核，无 key 自动降级为纯规则。

## 功能简介

- rubric = 维度列表，每个维度有权重；
- 内置规则维度：完整性（长度）、相关性（关键词命中）、结构清晰（结构标记）；
- `score(text)` 返回总分 0~1 与各维度明细及理由；
- rubric 可自定义传入。

## 快速开始

```bash
python3 agent_scorer.py "这是一段足够长的完整输出。第一讲 A，第二讲 B。"
```

作为库：

```python
from agent_scorer import RubricScorer, DEFAULT_RUBRIC
r = RubricScorer([{"name": "相关性", "weight": 1.0, "keywords": ["退款"]}]).score("我要退款")
print(r["total"])
```

## 无 API key 如何运行

核心评分是纯规则，**不需要任何 API key**。

## 目录结构

```
agent-scorer-lite/
├── agent_scorer.py
├── tests/test_agent_scorer.py
├── README.md / LICENSE / .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests -v
```

## 许可证

[MIT](./LICENSE) © 2026 ljiang9
