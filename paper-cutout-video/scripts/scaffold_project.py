#!/usr/bin/env python3
"""Create an idempotent project skeleton for paper cutout explainer videos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DIRECTORIES = (
    "edit/backgrounds/raw",
    "edit/backgrounds/processed",
    "edit/layers/raw",
    "edit/layers/vectors",
    "edit/images/raw",
    "edit/images/processed",
    "edit/audio/raw",
    "edit/audio/final",
    "edit/composition/src",
    "edit/composition/public",
    "edit/renders",
    "edit/verify",
)


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold an editable paper cutout explainer video project."
    )
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()

    if args.duration <= 0 or args.fps <= 0 or args.width <= 0 or args.height <= 0:
        parser.error("duration, fps, width, and height must be positive")

    root = args.project_dir.expanduser().resolve()
    for relative in DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)

    edit = root / "edit"
    files: dict[Path, str] = {
        edit / "project.md": f"""# {args.title}\n\n## 状态\n\n- 阶段：立项\n- 成片：未生成\n- 工程：`edit/composition/`\n\n## 关键决定\n\n- 画幅：{args.width} × {args.height}\n- 帧率：{args.fps} fps\n- 目标时长：{args.duration:.2f} 秒\n\n## 会话记录\n\n- 初始化项目骨架。\n""",
        edit / "brief.md": f"""# 生产 Brief\n\n- 项目：{args.title}\n- 主题：\n- 一句话结论：\n- 目标观众：\n- 观看价值：\n- 目标平台：\n- 时长：{args.duration:.2f} 秒\n- 画幅：{args.width} × {args.height}\n- 帧率：{args.fps} fps\n- 声音：\n- 事实与来源：\n- 场景语法：map-route / timeline-process / relationship-board / comparison / product-story\n- 交付层级：文档 / 工程 / 样片 / 成片\n""",
        edit / "script.md": """# 口播与画面\n\n| 开始 | 结束 | 口播 | 主要视觉 | 来源状态 | 动画 | 字幕 | 音效 |\n|---:|---:|---|---|---|---|---|---|\n""",
        edit / "shotlist.md": """# 镜头表\n\n| 镜头 | 时间 | 目的 | 背景/证据 | 纸张解释层 | 线条/路径 | 主体 | 镜头运动 | 验收点 |\n|---|---|---|---|---|---|---|---|---|\n""",
        edit / "assets-manifest.md": """# 素材清单\n\n| ID | 类型 | 来源状态 | 原始文件 | 派生文件 | 许可/来源 | 用途 | 待办 |\n|---|---|---|---|---|---|---|---|\n""",
        edit / "composition" / "DESIGN.md": """# Composition Design\n\n## 图层顺序\n\n1. PaperBackground\n2. EvidenceFrame\n3. PaperLayerReveal\n4. LineDraw / FlowMarks\n5. InfoLabel\n6. CutoutSubject\n7. CaptionLayer\n\n## 颜色 Token\n\n- paper:\n- accentA:\n- accentB:\n- line:\n- label:\n- caption:\n""",
    }

    created = []
    skipped = []
    for path, content in files.items():
        (created if write_if_missing(path, content) else skipped).append(str(path))

    motion_spec = edit / "motion-spec.json"
    motion_content = json.dumps(
        {
            "title": args.title,
            "composition": {
                "width": args.width,
                "height": args.height,
                "fps": args.fps,
                "durationSeconds": args.duration,
            },
            "camera": {"startScale": 1.0, "endScale": 1.06},
            "sceneGrammar": None,
            "paperLayers": [],
            "lines": [],
            "subjects": [],
            "captions": "captions.json",
            "audio": {"voiceover": None, "music": None, "sfx": []},
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    (created if write_if_missing(motion_spec, motion_content) else skipped).append(
        str(motion_spec)
    )

    print(f"Project root: {root}")
    print(f"Created files: {len(created)}")
    for path in created:
        print(f"  + {path}")
    if skipped:
        print(f"Preserved existing files: {len(skipped)}")
        for path in skipped:
            print(f"  = {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
