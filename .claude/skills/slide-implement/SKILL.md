---
description: 既存のスライドアウトライン (章立て概要) から Slidev の slides.md を肉付け実装するスキル。素材把握 → デザイン基準決定 → スライド実装 → ビルド検証 → フィードバック反映の順で進める。矢印フロー / Before-After 比較 / 循環図などの図解パターンを HTML/CSS で実装するスニペット集を含む。Use when OUTLINE.md などの章立て文書を元に Slidev スライドを実装するとき。
---

# slide-implement — Slidev スライド肉付け実装スキル

## 目的

アウトラインから slides.md を実装するときの定型作業 (フォント基準合わせ / 画像レイアウト / v-clicks 構文) を一通り押さえ、ユーザーに同じ指摘を繰り返させないようにする。

## 全体フロー

Phase 1: 素材把握 → Phase 2: デザイン基準決定 → Phase 3: スライド実装 → Phase 4: ビルド検証 → Phase 5: フィードバック反映

実装が一通り終わったら、レイアウト崩れ・見切れチェックは `slide-review` / `slide-review-run` スキルに委譲する。

## Phase 1: 素材把握

- OUTLINE.md などのアウトライン文書を Read
- 必要なアセット (画像 / コード / URL) の存在を確認
- **画像は `sips -g pixelWidth -g pixelHeight <file>` で実サイズを実測**。推測しない
- 不足アセットがあれば「未取得 (ユーザー提供必須)」と明示。「代用可」「モックで OK」で曖昧化しない

## Phase 2: デザイン基準決定

最初に基準を 1 つ決めて、全スライドで統一する。
- 本文フォント: `text-xl` を基準、補足は `text-base`/`text-sm`
- 行間: `leading-relaxed` + `space-y-6` (箇条書きの基準)
- カラースキーム: `colorSchema: dark` など
- 基準スライドを 1 枚先に作り、後続スライドはそこから派生させる

## Phase 3: スライド実装

### 画像中心スライド (大きな画像を画面いっぱい)

viewport 単位 (`vh`/`vw`) は使わない。ブラウザのアスペクト比が 16:9 でないとスライドエリアからはみ出る。
親要素 (%) ベースで:

```html
---
layout: full
---

<div style="position: absolute; inset: 2% 4%; display: flex; align-items: center; justify-content: center;">
  <img src="./assets/foo.png" style="width: 100%; height: 100%; object-fit: contain;" />
</div>
```

### 図解パターンのスニペット集

`slide-outline` で「因果/対比/並列/時系列/循環」と判定された箇条書きは、以下のテンプレートで実装する。Mermaid ではなく、既存スライドのカードスタイル (`bg-*-900/30` + `border` + `rounded-lg`) に揃えた HTML/CSS 直書きで統一する。色は `blue`/`green`/`purple`/`cyan` など既存スライドで使っている Tailwind カラーから選ぶ。

#### 矢印フロー (因果・変換の流れ)

```html
<div class="flex items-center justify-center gap-6">
  <div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-8 py-6 text-2xl text-center">A</div>
  <div class="text-4xl opacity-60">→</div>
  <div class="bg-green-900/30 border border-green-500/40 rounded-lg px-8 py-6 text-2xl text-center">B</div>
</div>
```

- 3 ステップ以上に伸ばす場合は `<div>` + `→` を繰り返す。矢印は `text-4xl opacity-60` で統一し、ノードの文字サイズより控えめにする
- 各ノードの横幅がテキスト量で不揃いになる場合は `flex-1` を付けて揃える

#### ステップフロー (時系列・手順)

矢印フローに番号を追加したもの。各ノードの左上に番号バッジを置く。

```html
<div class="flex items-center justify-center gap-6">
  <div class="relative bg-blue-900/30 border border-blue-500/40 rounded-lg px-8 py-6 text-2xl text-center">
    <span class="absolute -top-3 -left-3 bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg">1</span>
    素材収集
  </div>
  <div class="text-4xl opacity-60">→</div>
  <div class="relative bg-green-900/30 border border-green-500/40 rounded-lg px-8 py-6 text-2xl text-center">
    <span class="absolute -top-3 -left-3 bg-green-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg">2</span>
    実装
  </div>
</div>
```

#### Before / After 比較 (対比)

```html
<div class="flex-1 grid grid-cols-2 gap-8 items-center">
  <div class="text-center">
    <div class="text-xl opacity-60 mb-2">Before</div>
    <div class="bg-red-900/20 border border-red-500/30 rounded-lg px-6 py-8 text-2xl">...</div>
  </div>
  <div class="text-center">
    <div class="text-xl opacity-60 mb-2">After</div>
    <div class="bg-green-900/20 border border-green-500/30 rounded-lg px-6 py-8 text-2xl">...</div>
  </div>
</div>
```

- 中央に `⇄` や `→` を挟みたい場合は `grid-cols-[1fr_auto_1fr]` に変更し、中央列に矢印を置く

#### 並列カード (弱い並列で、かつ図解価値がある場合)

`slide-outline` の判断基準で「3 要素以下の弱い並列」は箇条書きのままにするが、要素数が多い/各要素の独立性を強調したい場合はこの横並びカードを使う。既存の「ループエンジニアリングの定義 3 種」スライド (縦 3 段カード) と同じ考え方で、横並びにする版:

```html
<div class="grid grid-cols-3 gap-6">
  <div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-6 py-6 text-center">...</div>
  <div class="bg-green-900/30 border border-green-500/40 rounded-lg px-6 py-6 text-center">...</div>
  <div class="bg-purple-900/30 border border-purple-500/40 rounded-lg px-6 py-6 text-center">...</div>
</div>
```

#### 循環図 (振り出しに戻る・反復)

3〜4 ノードを円環状に配置し、矢印で繋ぐ。CSS の `position: absolute` で配置するため、座標は必ず `%` 指定にする (px だとキャンバス比率 980x552 からずれて画面外に出る)。

```html
<div class="relative w-full" style="height: 60%;">
  <div class="absolute bg-blue-900/30 border border-blue-500/40 rounded-lg px-6 py-4 text-xl" style="top: 0%; left: 40%;">A</div>
  <div class="absolute bg-green-900/30 border border-green-500/40 rounded-lg px-6 py-4 text-xl" style="top: 40%; left: 75%;">B</div>
  <div class="absolute bg-purple-900/30 border border-purple-500/40 rounded-lg px-6 py-4 text-xl" style="top: 40%; left: 5%;">C</div>
  <!-- ノード間の矢印は draw.io で別途作図するか、疑似矢印として ::after の border-triangle を使う -->
</div>
```

- ノード数が 3 を超える、または矢印の向きが複雑になる場合は HTML/CSS ではなく draw.io で作図する (workflow.png と同じ方式)。無理に CSS で描くと矢印とテキストが重なりやすい

### 強調表記

`<div>` 内では Markdown の `**...**` がそのまま表示されることがある。`<strong>` タグを直接使う。

### v-clicks 構文

- 最初から表示するもの: `<v-clicks>` の外
- 順次表示するもの: `<v-clicks>` 内の `- ...` 箇条書き
- 特定クリックで表示: `<div v-click="N">` (N は 1 から)

### 単語途中で折り返させない

長い英単語/カナ語句は `<span class="whitespace-nowrap">...</span>` で囲んで保護する。

## Phase 4: ビルド検証

```
cd <slide-dir> && npx slidev build --base /<topic>/
```

ビルドエラーは即その場で直す。次の Phase に進めない。

## Phase 5: フィードバック反映

- 本文の文言はユーザーが確定したもの。**勝手に短縮・改変しない**。長さの問題は `whitespace-nowrap` で語句保護する
- 画像サイズ調整は「収まる範囲で最大」を最初に狙う。次に縮める
- 複数指摘を一度に受けたら、修正方針を整理してユーザーに提示してから実装

## やってはいけないこと

- フォント・行間を他スライドと揃えずに進める
- 画像サイズを推測する (実測する)
- viewport (`vh`/`vw`) で画像サイズを指定する
- 強調を `<div>` 内で `**...**` で書いて、レンダリングされないまま提出する
- アセット未取得を「代用可」「モックで OK」で曖昧化する
- 本文を勝手に短縮する (折り返し問題は `whitespace-nowrap` で解決)
- 循環図・複雑な矢印構造を無理に CSS `position: absolute` (px 指定) で描き、矢印とテキストを重ねる
   → ノード数が多い/矢印が複雑なら draw.io で作図する
