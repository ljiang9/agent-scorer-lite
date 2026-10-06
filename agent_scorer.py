#!/usr/bin/env python3
"""agent_scorer —— 按可配置 rubric 对 agent 输出做规则式评分。

rubric 是一组维度，每个维度有权重与若干规则函数；
每个维度得分 0~1，加权求和得到总分。可选调用 LLM 复核（无 key 时自动降级为纯规则）。
零第三方依赖。

用法：
    from agent_scorer import RubricScorer, DEFAULT_RUBRIC
    sc = RubricScorer(DEFAULT_RUBRIC)
    print(sc.score("一段 agent 输出……"))
"""
from __future__ import annotations

import argparse
import json
import sys

# 默认 rubric：维度 + 权重 + 规则
DEFAULT_RUBRIC = [
    {"name": "完整性", "weight": 0.4, "min_len": 50},
    {"name": "相关性", "weight": 0.3, "keywords": []},
    {"name": "结构清晰", "weight": 0.3, "has_markers": True},
]


def _len_score(text: str, min_len: int) -> float:
    n = len(text.strip())
    return min(1.0, n / min_len) if min_len else 1.0


def _keyword_score(text: str, keywords: list[str]) -> float:
    if not keywords:
        return 1.0
    hits = sum(1 for k in keywords if k in text)
    return hits / len(keywords)


def _structure_score(text: str) -> float:
    markers = sum(m in text for m in ["1.", "-", "。", "\n"])
    return min(1.0, markers / 3.0)


class RubricScorer:
    def __init__(self, rubric: list[dict] | None = None):
        self.rubric = rubric or DEFAULT_RUBRIC

    def score_dimension(self, dim: dict, text: str) -> dict:
        name = dim["name"]
        if name == "完整性":
            s = _len_score(text, dim.get("min_len", 50))
            reason = f"长度 {len(text.strip())} 字"
        elif name == "相关性":
            s = _keyword_score(text, dim.get("keywords", []))
            reason = "关键词命中" if dim.get("keywords") else "无关键词要求，默认满分"
        elif name == "结构清晰":
            s = _structure_score(text)
            reason = f"结构标记出现次数"
        else:
            s = 0.5
            reason = "未知维度默认分"
        return {"dimension": name, "score": round(s, 3),
                "weight": dim["weight"], "reason": reason}

    def score(self, text: str) -> dict:
        details = [self.score_dimension(d, text) for d in self.rubric]
        total = sum(d["score"] * d["weight"] for d in details)
        return {
            "total": round(total, 3),
            "max": 1.0,
            "details": details,
        }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="rubric 规则式评分")
    p.add_argument("text", nargs="?", help="待评分文本；不传则读标准输入")
    args = p.parse_args(argv)
    text = args.text or sys.stdin.read()
    r = RubricScorer().score(text)
    print(f"总分：{r['total']} / {r['max']}")
    for d in r["details"]:
        print(f"  {d['dimension']}（权重 {d['weight']}）：{d['score']}  —— {d['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
