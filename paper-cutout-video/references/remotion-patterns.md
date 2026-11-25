# Remotion 实现模式

## 目录

1. 基础原则
2. 纸片揭示
3. 线条与路径绘制
4. 流动标记
5. 剪纸主体入场
6. 真实证据框
7. 镜头推近
8. 参数化
9. 3D 纸雕舞台（`@remotion/three`）

## 1. 基础原则

- 使用 `useCurrentFrame()`、`useVideoConfig()`、`interpolate()` 和 `Sequence`。
- 所有插值范围设置 `extrapolateLeft/Right: 'clamp'`，除非明确需要循环或延伸。
- 不使用 CSS transition 或 CSS animation。
- 需要 Studio 编辑时把插值直接写在元素内联样式中，并优先使用 `scale`、`translate` 和 `rotate`。
- 静态背景使用 `CanvasImage` + `staticFile()`；动态纸片、线条、标签和主体保持独立。
- 准确地图、图表或界面使用可信素材；解释层不能覆盖或篡改真实证据。

## 2. 纸片揭示

普通卡片用裁切进度揭示；不规则区域用 SVG mask。揭示方向必须服务于口播。

```tsx
const progress = interpolate(frame, [start, end], [0, 1], {
  easing: Easing.bezier(0.16, 1, 0.3, 1),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

<div
  style={{
    clipPath: `inset(0 ${(1 - progress) * 100}% 0 0)`,
    filter: 'drop-shadow(0 12px 10px rgba(45,31,23,0.2))',
  }}
>
  <CanvasImage src={staticFile(src)} />
</div>
```

地图色带或任意不规则区域使用宽路径作为 `<mask>`，不要只对完整区域做 opacity 淡入。

## 3. 线条与路径绘制

安装与当前 Remotion 版本一致的路径包：

```bash
npx remotion add @remotion/paths
```

```tsx
import {evolvePath} from '@remotion/paths';
import {Easing, interpolate, useCurrentFrame} from 'remotion';

export const LineDraw = ({d, start, end}: Props) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [start, end], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const evolution = evolvePath(progress, d);

  return <path d={d} fill="none" stroke="#51448d" strokeWidth={18}
    strokeLinecap="round" strokeDasharray={evolution.strokeDasharray}
    strokeDashoffset={evolution.strokeDashoffset} />;
};
```

`LineDraw` 可用于关系线、时间线、路线和手绘下划线。需要准确的路径先从可信几何或人工描摹获得 `d`。

## 4. 流动标记

主线完成后再启动虚线或箭头。绘制进度和流动偏移是两个属性。

```tsx
const dashOffset = interpolate(frame, [flowStart, flowEnd], [0, -240], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'extend',
});

<path d={d} fill="none" stroke="#fffaf0" strokeWidth={7}
  strokeLinecap="round" strokeDasharray="18 18" strokeDashoffset={dashOffset} />
```

如果末尾需要循环，让偏移长度与 dash 周期成整数倍，并把接缝放在画面外。

## 5. 剪纸主体入场

主体 PNG/WebP 建议预先烘焙白边。用 `<Sequence>` 把全局开始帧转换为局部时间，便于复用。

```tsx
export const CutoutSubject = ({src, start}: {src: string; start: number}) => (
  <Sequence from={start} layout="none"><CutoutBody src={src} /></Sequence>
);

const CutoutBody = ({src}: {src: string}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scale = interpolate(frame, [0, 0.5 * fps], [0.72, 1], {
    easing: Easing.spring({damping: 150}),
    output: 'perceptual-scale',
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return <CanvasImage src={staticFile(src)} style={{
    width: 320, height: 260, objectFit: 'contain', scale,
    translate: `0 ${interpolate(frame, [0, 0.5 * fps], [38, 0], {
      extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    })}px`,
    rotate: `${Math.sin(frame / 18) * 0.8}deg`,
    filter: 'drop-shadow(0 14px 10px rgba(45,31,23,0.28))',
  }} />;
};
```

## 6. 真实证据框

产品页面、截图、图表或原始影像先作为主视觉进入，再叠加纸张标签与高亮。不得用自制界面冒充真实运行结果。

```tsx
<div style={{position: 'absolute', left, top, width, padding: 14,
  background: '#f4ead4', boxShadow: '0 16px 28px rgba(45,31,23,.22)',
  rotate: '-1deg'}}>
  <CanvasImage src={staticFile(src)} style={{width: '100%', height: 'auto'}} />
  <div style={{fontSize: 24, color: '#4a382c'}}>{sourceLabel}</div>
</div>
```

## 7. 镜头推近

环境和解释层可以包在一个容器中缓慢推近。字幕不要放入该容器，否则字幕也会缩放。

```tsx
<div style={{position: 'absolute', inset: 0,
  scale: interpolate(frame, [0, 5 * fps], [1, 1.06], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    output: 'perceptual-scale',
  }), transformOrigin: '48% 55%'}}>
  {/* background, evidence and explainer layers */}
</div>
```

## 8. 参数化

使用 Zod schema 暴露：

- 标题、结论、标签和场景语法；
- 颜色 token；
- 背景、证据、纸片、线条与主体素材路径；
- 每个动作的开始帧和结束帧；
- 主体位置、尺寸和 z-index；
- 字幕和音频文件。

不要把所有元素塞进一个巨型配置对象。保持组件职责清晰，默认 props 作为可运行示例。

## 9. 3D 纸雕舞台（`@remotion/three`）

保留 2D/2.5D 模式的同时，当 `renderMode` 为 `3d-diorama` 或 `hybrid` 时，在 Remotion 中引入 `@remotion/three` 与 `three`。

### 9.1 帧驱动铁律

- **严禁在 `useFrame` 中使用 `delta` 累加状态**，也不得使用 `Math.random()` 或 `Date.now()`。
- 所有折叠角、滑块位置、能量柱高度、地球自转角和云朵漂移，必须完全由 `useCurrentFrame()` 计算得出，保证渲染结果 100% 确定性。

```tsx
import {ThreeCanvas} from '@remotion/three';
import {interpolate, Easing, useCurrentFrame, useVideoConfig} from 'remotion';

export const PaperDioramaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();

  // 1) 画卷分段摊平进度（支撑依赖：第 N 段 > 85% 后才允许上方组件立起）
  const seg0 = interpolate(frame, [0, 32], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const pop0 = interpolate(frame, [26, 48], [0, 1], {
    easing: Easing.out(Easing.back(1.7)),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <ThreeCanvas width={width} height={height} shadows camera={{fov: 34, position: [2, 7.5, 10]}}>
      <color attach="background" args={['#1a1612']} />
      <hemisphereLight args={['#fff4e0', '#2b221a', 0.45]} />
      <directionalLight
        position={[7, 10, 6]}
        intensity={1.35}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />
      {/* 3D 纸雕与折叠层 */}
      <group rotation-y={interpolate(seg0, [0, 1], [-Math.PI * 0.45, 0])}>
        <mesh position={[1, -0.02, 0]} receiveShadow castShadow>
          <boxGeometry args={[2.0, 0.04, 5.2]} />
          <meshStandardMaterial color="#f2ead9" roughness={0.88} />
        </mesh>
        {pop0 > 0.01 && (
          <group scale={pop0} rotation-x={(1 - Math.min(pop0, 1)) * 1.1}>
            {/* 拆分底座、立柱、屋檐等精细子件，均启用 flatShading */}
          </group>
        )}
      </group>
    </ThreeCanvas>
  );
};
```

### 9.2 立体贺卡插片（`PopUpCutout3D`）与微缩运镜

适合城市地标与历史建筑：透明 PNG 剪纸带底部折脚，从折叠地图上沿铰链立起，并配合 `CatmullRomCurve3` 做贴近纸面的微距跟拍与结尾拉升。

```tsx
export const PopUpCutout3D: React.FC<{
  texture: THREE.Texture;
  position: [number, number, number];
  size: [number, number];
  startFrame: number;
}> = ({texture, position, size, startFrame}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [startFrame, startFrame + 22], [0, 1], {
    easing: Easing.out(Easing.back(1.5)),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const [w, h] = size;

  return (
    <group position={position} visible={p > 0.01}>
      {/* 底部纸质折脚（L 形贴合地图表面） */}
      <mesh position={[0, 0.01, 0.14]} rotation-x={-Math.PI / 2} receiveShadow>
        <planeGeometry args={[w * 0.6, 0.28]} />
        <meshStandardMaterial color="#efe6d5" roughness={0.9} />
      </mesh>
      {/* 绕底部铰链立起的照片级剪纸插片 */}
      <group rotation-x={(1 - Math.min(p, 1)) * (Math.PI / 2)} scale={[1, Math.max(0.01, p), 1]}>
        <mesh position={[0, h / 2, 0]} castShadow>
          <planeGeometry args={[w, h]} />
          <meshStandardMaterial map={texture} transparent alphaTest={0.5} side={THREE.DoubleSide} roughness={0.8} />
        </mesh>
      </group>
    </group>
  );
};
```

### 9.3 混合模式（`hybrid`）分层结构

在 `hybrid` 模式下，将 `<ThreeCanvas>` 作为底层立体舞台，精准证据框、数据图表与底部字幕保留在 2D DOM 层，确保截图与字幕零透视畸变：

```tsx
<AbsoluteFill>
  <PaperDioramaScene />
  <EvidenceFrame src="real-benchmark.png" left={80} top={90} width={520} />
  <CaptionLayer captions={captions} />
</AbsoluteFill>
```

