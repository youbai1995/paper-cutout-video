# paper-cutout-video

**paper-cutout-video** 是一个基于 **Agent Skills** 规范的开源视频生产技能（适用于 **Claude Code**、**Codex** 及兼容 Agent Skills 的 AI 编程助手），用于将历史科普、地理路线、物理机制、人物关系、流程对比或产品故事，制作成**事实可验证、图层可编辑、帧驱动渲染**的纸张剪纸拼贴与 3D 立体纸雕解说视频。

它不是随机抽卡的“一键文生视频”，而是一套完整的 **“生产文档（Brief/口播/分镜）→ 素材真实性分级 → Remotion + Three.js 分层工程 → FFmpeg 质量验收”** 工程化工作流。

---

## 核心能力与渲染架构

本技能支持 **2D/2.5D 剪纸拼贴** 与 **3D 纸雕立体舞台（`@remotion/three`）** 双轨并行，并默认推荐 **`hybrid` 混合模式**：

| 渲染轨道 (`renderMode`) | 适用场景 | 核心视觉机制 | 真实性保障 |
|---|---|---|---|
| **`2d-cutout`** | 快节奏图文解说、产品录屏拆解 | `clipPath` / SVG `<mask>` 揭示、`evolvePath` 画线、`spring` 弹入 | 真实截图与数据图表 0° 零变形 |
| **`2.5d-fold`** | 步骤对比、封门揭晓 | CSS 3D 折痕翻页、受光暗度遮罩、动态接触阴影 | 摊平后保持正交平面 |
| **`3d-diorama`** | 地理地球仪、物理力学实验、多层地质剖面、长卷地图 | Three.js `flatShading` 折纸几何体、程序化纸纤维纹理、`2048px` 软阴影 | 物理过程、坐标与比例受控 |
| **`hybrid`（推荐）** | 城市立体地图、深度科普、历史路线 | 3D 纸雕/立体贺卡主舞台 + 2D Remotion 精准证据框与底部字幕 | 兼顾电影级空间纵深与事实严谨性 |

### 核心特性

- **双表现模式**：支持 **立体贺卡插片（`pop-up-cutout`：前中后多层照片级透明剪纸 + 折脚与薄纸侧边）** 与 **3D 折纸几何体（`lowpoly-papercraft`）**。
- **五种纸艺展开形态（`foldStyle`）**：横向画卷（`scroll-unfold`）、手风琴折页（`accordion-fold`）、中轴对开立体书（`book-spread`）、证据折封揭晓（`evidence-fold`）、倾斜地球仪舞台（`globe-orbit`）。
- **跨风格参考视频拆解**：支持拆解非纸雕风格的外部科普视频（如 Vox 地图解说、3Blue1Brown/物理实验、Kurzgesagt 剖面动画），仅迁移其叙事节拍与镜头机制，重构为可编辑的纸艺工程。
- **真实性边界管控**：严格区分 `REAL LOCAL`、`OFFICIAL`、`LICENSED`、`GENERATED`、`EXPLAINER` 与 `PLACEHOLDER`，绝不伪造数据、地理轮廓或产品界面。

---

## 安装方式（支持多种 AI Agent）

### 方式一：通过 Skills CLI 一键安装（推荐）

支持 **Claude Code**、**Codex** 等兼容 Agent Skills 的客户端：

```bash
# 安装到 Claude Code
npx --yes skills add youbai1995/paper-cutout-video --skill paper-cutout-video --agent claude-code --copy --yes

# 安装到 Codex
npx --yes skills add youbai1995/paper-cutout-video --skill paper-cutout-video --agent codex --copy --yes
```

如需全局跨项目使用，可附加 `--global` 参数。

### 方式二：手动克隆安装

```bash
git clone https://github.com/youbai1995/paper-cutout-video.git
cd paper-cutout-video

# 复制到 Codex Skills 目录
cp -R paper-cutout-video ~/.codex/skills/

# 或复制到 Claude Code Skills 目录
cp -R paper-cutout-video ~/.claude/skills/
```

---

## 快速使用

重启或打开你的 AI 编程助手后，按需求指定交付层级（仅方案 / 工程样片 / 成片导出）：

```text
$paper-cutout-video

参考这段历史地图视频的节奏，制作一段 45 秒的“郑和下西洋路线”横屏科普视频（1920×1080）。
使用 hybrid 模式与横向画卷展开（scroll-unfold），先输出 brief、口播稿与镜头表。
```

也可以直接用于物理、地理或产品实测解说：

```text
$paper-cutout-video

做一个 30 秒的“牛顿三棱镜色散实验”3D 纸雕科普样片，要求光路符合二次折射规律，并附带波长对照数据卡。
```

---

## 仓库结构

```text
paper-cutout-video/
├── SKILL.md                              # 核心工作流与硬规则定义
├── agents/openai.yaml                    # Codex Skill 元数据
├── scripts/scaffold_project.py           # 幂等项目骨架与 motion-spec.json 生成脚本
└── references/
    ├── production-blueprint.md           # 完整生产阶段与角色分工规范
    ├── style-spec.md                     # 双轨视觉规范、纸艺展开形态与 3D 细节约束
    ├── remotion-patterns.md              # Remotion 2D/2.5D 与 @remotion/three 3D 代码模式
    ├── quality-gates.md                  # 成片阻断项、视觉/响度/3D 关键帧与 FFmpeg 验收标准
    └── reference-deconstruction.md       # 非纸雕外部参考视频拆解与跨风格迁移指南
```

---

## 常见问题（FAQ）

**Q：它与 Sora / Runway 等 AI 文生视频工具有什么区别？**  
A：文生视频无法精确控制地图海岸线、物理公式、产品界面截图或文字字幕，且难以局部修改。`paper-cutout-video` 使用 Remotion 与 Three.js 进行确定性帧驱动渲染，所有图层、时间轴、路径、旁白与字幕均可独立编辑与复现。

**Q：如何保证视频中的地图、数据或产品界面不出错？**  
A：Skill 内置真实性硬规则：禁止用生成式图片直接承担需要精确结构的地图、图表或产品界面；必须使用可信矢量/截图素材，并通过 `hybrid` 模式将精准证据置于 0° 正交层，不随 3D 镜头产生透视畸变。

**Q：默认输出规格是什么？**  
A：默认输出为 **1920×1080（16:9 横屏）、30fps、H.264/AAC MP4**，并支持通过 `brief.md` 按需调整为 60fps 或其他画幅。

---

## 许可

MIT License。第三方参考视频、字体、图片、音乐和其他素材不包含在本仓库许可范围内，使用者需自行确认相应授权。
