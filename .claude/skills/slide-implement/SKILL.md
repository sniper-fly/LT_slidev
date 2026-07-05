---
description: 既存のスライドアウトライン (章立て概要) から Slidev の slides.md を肉付け実装するスキル。素材把握 → デザイン基準決定 → スライド実装 → ビルド検証 → フィードバック反映の順で進める。Use when OUTLINE.md などの章立て文書を元に Slidev スライドを実装するとき。
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
