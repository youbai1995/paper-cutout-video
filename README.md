# paper-cutout-video

一个用于 Codex 的通用 Skill：把历史科普、地图路线、时间线、人物关系、流程对比或产品故事，制作成可验证、可编辑的纸张剪纸拼贴风格视频。

## 能做什么

- 从生产 brief、口播稿和镜头表开始组织内容；
- 区分真实素材、官方素材、解释动画和占位素材；
- 搭建分层 Remotion 工程；
- 处理字幕、声音、样片、正式渲染和质量验收；
- 迁移参考视频的视觉语言，同时替换主题与素材。

## 安装

克隆仓库后，将 Skill 目录复制到 Codex Skills 目录：

```bash
git clone https://github.com/youbai1995/paper-cutout-video.git
cd paper-cutout-video
cp -R paper-cutout-video ~/.codex/skills/
```

重新启动 Codex 后即可调用：

```text
$paper-cutout-video

参考这段视频的剪纸拼贴视觉语言，
做一段 30 秒“郑和下西洋路线”动画。
先只输出脚本和镜头表。
```

## 目录

```text
paper-cutout-video/
├── SKILL.md
├── agents/openai.yaml
├── scripts/scaffold_project.py
└── references/
```

## 许可

MIT License。第三方参考视频、字体、图片、音乐和其他素材不包含在本仓库许可范围内，使用者需自行确认相应授权。
