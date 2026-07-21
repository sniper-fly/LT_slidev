---
name: slide-review
description: |
  Slidev スライドの自動レビューループスキル。1920x1080 想定でスクリーンショットを取得し、
  レイアウト崩れ・文字はみ出し・可読性・情報密度・説明順序・文章のまま図解すべき箇所などを
  エージェント自身が画像レビューして、findings.json (機械可読) + report.html (人間用) を生成。
  AI への応答は subagent の最終出力テキストで返す。critical が 0 件になるか反復 3 回まで継続。

  以下のようなケースでこのスキルを使うこと:
  - Slidev スライドのレビュー、レイアウトチェック、文字はみ出し検出を依頼された場合
  - 「スライドレビュー」「slide-review」「自動レビュー」「スライドの見た目チェック」に言及がある場合
  - 「スクショ撮ってチェックして」とスライドに対して依頼された場合

  general-purpose agent (subagent) から呼ばれることを想定している。
  ユーザーが直接 1 コマンドで起動したいときは `slide-review-run` メタスキル (`/slide-review-run`) を使う。
---

# slide-review — Slidev 自動レビューループ

## このスキルの責務

1. 対象スライドの 1 スライド 1 PNG スクショを取得する (`scripts/capture.sh`)
2. エージェント自身が Read tool で各 PNG を読み、定義済みの観点で評価する
3. `findings.json` (機械可読・履歴) と `report.html` (人間用) を生成する
4. **呼び出し元への応答**は、subagent の最終出力テキストに findings の構造化要約を載せて返す (Markdown ファイルは作らない)
5. 修正後に再ループ。critical が 0 件 / 反復 3 回 / ユーザー停止のいずれかで終了

## 成果物

| 成果物 | 用途 | 形式 |
|---|---|---|
| `<.review/<ts>>/screenshots/NN.png` | スクショ (capture.sh 出力) | PNG |
| `<.review/<ts>>/findings.json` | 機械可読の指摘一覧 / HTML 生成入力 / 履歴 | JSON |
| `<.review/<ts>>/report.html` | 人間用。スクショと改善点を同一画面で確認 | HTML (self-contained) |
| subagent の最終応答テキスト | 呼び出し元エージェントへの報告 | テキスト (構造化) |

## 前提

- 対象スライドは Slidev 形式 (`<slide-dir>/slides.md`) で配置されている
- `<slide-dir>` から `pnpm exec slidev` が解決できる状態 (Slidev プロジェクトとして `pnpm install` 済み)
  - 未インストールなら、Slidev プロジェクトルートで `pnpm install` をユーザーに依頼する
- Playwright のブラウザバイナリ (`chromium-headless-shell`) が導入済み (`slidev export` が内部で利用)
  - `Executable doesn't exist at .../chrome-headless-shell` エラーが出たら、Slidev プロジェクトルートで `pnpm exec playwright install chromium-headless-shell` をユーザーに依頼する

---

## 実行フロー

### Step 1: スクリーンショット取得

```bash
./.claude/skills/slide-review/scripts/capture.sh <slide-dir>
```

オプション:
- `--scale N` 出力解像度倍率 (デフォルト 2 で約 1920px 幅)
- `--range R` `1,4-5` のようにスライド範囲を絞る
- `--with-clicks` クリックステップごとに PNG を分ける (デフォルトはスライド単位のみ)

成功すると最終行に `screenshot_dir=<path>` が出力される。以降このパスを **SHOTS_DIR** と呼ぶ。

### Step 2: 各 PNG を Read してレビュー

`SHOTS_DIR` 配下の PNG を **すべて** Read tool で読み込み、以下の観点で 1 枚ずつ評価する。

**観点 (category)**
- `layout`: 文字はみ出し、要素重なり、画面外配置、
   **意味の切れ目でない位置での改行** (「〜という別の/仕事が生まれる」のような不自然な折れ方)、
   **主役要素 (画像・アイコン等) の配置バランス** (中央寄せ/上寄せなど意図した位置にあるか)
- `readability`: フォントサイズ最小値、行間、本文密度
- `contrast`: 背景色と文字色のコントラスト不足
- `density`: 情報量過多、1 スライド 1 メッセージ違反。
   図と文章を併載しているスライドでは「図がパッと見で理解しやすいか / 文章だけの方が早いか」を比較し、
   図のセンスが悪く読み取りに時間がかかる場合は「文章のみへ差し替え」を提案 (またはその逆)。
   二重提示そのものが悪いのではなく、伝達効率の悪い表現を残すことが悪い
- `narrative`: 説明順序、用語の登場順
- `consistency`: タイトル/見出し/余白/色のスライド間統一
- `wording`: 見出し・箇条書きの**文字量としての冗長性** (長さ・重複による伝達効率の問題)。
   「見出しと本文が同じ内容を繰り返していないか」「修飾語を削っても意味が変わらないか」
   (例: 「一瞬で作れるが、AI の手直しという別の仕事が生まれる」→「AI の手直しという別の仕事が生まれる」) を評価。
   これとは別に、実際にレンダリングされた文字列を見て初めて気づくトーンの気持ち悪さ
   (自己陶酔的な言い回し、過剰な演出、文脈にそぐわない比喩など) も検出対象とする (`requiresHumanDecision: true` で報告、下記「トーンの扱い」参照)
- `pacing`: 箇条書きが複数項目あるスライドで、一括表示のままでよいか `v-clicks` による段階表示にすべきかを評価。
   項目間に問題→解決、主張→補足のような展開があり、聴衆に一つずつ提示すべき場合は段階表示化を提案
- `visualization`: 箇条書き・本文が**文章のまま図解すべき内容を放置していないか**を評価する。
   項目・文中の助詞・接続詞 (「〜すると」「〜に対して」「〜と」「まず/次に」「振り出しに戻る」等) から
   因果・対比・並列・時系列・循環の関係性が読み取れるのに、単純な箇条書き/文章のまま実装されている場合に検出する。
   `slide-outline` の判断基準 (3 要素以下の弱い並列は対象外) を踏襲し、関係性の薄い単純な列挙まで図解化を求めない。
   検出したら `suggestedFix` に具体的な図解パターン名 (矢印フロー/Before-After/並列カード/ステップフロー/循環図。
   `slide-implement` のスニペット集参照) を明記する
- `diagram-consistency`: ワークフロー図・アーキテクチャ図など「構造」を表す埋め込み画像について、
   矢印の向きとグループ (ループ/コンテナ) の包含関係に図の中だけで自己矛盾がないかを確認する。
   図が主張する内容が技術的に正しいかどうかの検証は対象外 (下記「注意事項」参照)。
   図が表す構造を一言で説明できない場合は `note` (`requiresHumanDecision: true`) で報告する

**深刻度 (severity)**
- `critical`: 文字はみ出し、要素重なり、読めないコントラスト、
   **主役画像/主役コード/主役図の見切れ**、
   **主役要素 (主役画像・コード・図) が画面の十分な占有率を持っていない (小さすぎる)**、
   **箇条書きの行間/余白が詰まりすぎてスライド縦領域を使えていない** など **必ず修正**
- `warning`: 情報量過多、余白の偏り、
   **スライド間で意図の説明がつかないフォントサイズ差異 (例: 他が `text-6xl` の見出しが 1 枚だけ `text-5xl`)**、
   説明順序の違和感、
   **文章のまま図解すべき内容 (`visualization`)** など **修正推奨**
- `note`: 好みや改善提案。必須修正ではない

**完成基準** (合格ラインの目安)
- 1920x1080 表示で文字・図・コードがすべて画面内に収まっている
- 本文・注釈・コードの最小フォントが可読範囲 (本文 ≥ 24px / 見出し ≥ 40px が目安。
   主役のコマンド・数式・短い結論はさらに大きく)
- 主役画像/主役コード/主役図は画面の有効領域に対して十分な占有率
   (目安: 高さの 50% 以上 or 幅の 60% 以上)
- 箇条書きはスライドの縦領域を使って適切な行間/余白を確保 (詰めて上半分で終わらせない)
- 背景色と文字色のコントラストが十分
- 図・カード・コードブロック・見出しが重なっていない
- 情報量が過多でなく、発表者が説明しやすい密度
- 同じ情報を図と文章で重ねている場合、どちらの方がパッと見で伝わるかを比較し、
   劣る方を採用していない (図のセンスが悪いなら文章へ差し替え、文章が冗長なら図へ)
- スライド間でタイトル/見出し/余白/フォント/色に一貫性
- 1 スライド 1 メッセージで主張が視覚的に伝わる
- 見出しは本文の要約になっており、本文と重複せず、削っても意味が変わらない修飾語が残っていない
- 箇条書きの項目間に問題→解決・主張→補足のような展開がある場合、一括表示ではなく段階表示 (`v-clicks`) の方が伝わりやすくないか検討されている
- 静止画 1 枚で UI やプロセスなど動きのある対象を説明している場合、静止画では伝わらない情報がないか (伝わらない場合は GIF 化・複数カット化を提案)
- ワークフロー図等の構造図は、矢印の向きとグループの包含関係が図の中で自己矛盾していない
- 箇条書き・本文の助詞・接続詞から因果・対比・並列・時系列・循環の関係性が読み取れる場合、文章のまま放置せず図解パターンへの変換が検討されている (関係性の薄い単純な列挙まで図解化を強制しない)

### Step 3: JSON 出力

レビュー結果を以下のスキーマで `<SHOTS_DIR>/../findings.json` に保存する。

```json
{
  "summary": {
    "hasCritical": true,
    "criticalCount": 1,
    "warningCount": 2,
    "noteCount": 1,
    "overallComment": "全体所見"
  },
  "findings": [
    {
      "slideNumber": 3,
      "severity": "critical",
      "category": "layout",
      "issue": "問題点の要約",
      "evidence": "スクショ上でそう判断した根拠",
      "suggestedFix": "修正案",
      "requiresHumanDecision": false
    }
  ]
}
```

ルール:
- `requiresHumanDecision`: 内容・構成・表現の好みに関わる場合は `true`。レイアウト等の機械的問題は `false`
- `slideNumber` は 1 始まり (PNG ファイル名の数字部分と同じ)
- `findings` は severity を `critical → warning → note` の順で並べる
- `suggestedFix` は **抽象的な表現で済ませない**。修正対象のプロパティを `slides.md` から特定し、
   **「現在値 → 推奨値」** の形で具体的に書く。たとえば:
  - 画像サイズ: `max-h-[70vh] → max-h-[85vh]` (見切れがあれば縮める方向、小さすぎるなら拡大方向)
  - フォント: `text-lg → text-2xl`、見出しなら `text-3xl → text-5xl`
  - グリッド比率: `grid-cols-2 → grid-cols-5 + col-span-2 / col-span-3` (画像を主役にしたい場合)
  - 行間/余白: `space-y-2 → space-y-6`、`mt-4 → mt-10`
  - アバター/カードサイズ: `w-60 h-60 → w-72 h-72`
  - 値を確定できない場合 (要ユーザー判断) でも、**最低 2 つの候補値** (例: `max-h-[70vh]` / `max-h-[80vh]`) を提示し、現在値も明記する
- 修正対象が画像素材自体 (写真の切り抜き、解像度) の場合は「ユーザーがアセットを差し替える必要あり」と
   `suggestedFix` に明記し、`requiresHumanDecision: true` にする
- `visualization` の指摘は構成判断 (どの図解パターンに変換するか) を含むため、常に `requiresHumanDecision: true` にする。
   `suggestedFix` には図解パターン名を具体的に書く (例: 「矢印フロー (`slide-implement` のスニペット参照) へ変換」)

### Step 4: HTML レポート生成 (人間用)

`findings.json` を入力に、`scripts/generate_report_html.py` を実行して `report.html` を生成する。

```bash
python3 .claude/skills/slide-review/scripts/generate_report_html.py <findings.json のパス>
```

成功すると最終行に `report_html=<path>` が出力される。

`report.html` は self-contained (外部依存なし)。レイアウトは **縦積みカード型**:
- 上部: サマリ (critical/warning/note 件数) / 全体所見 / スライド番号ジャンプナビ
- 各スライド: 左にスクショ画像、右に findings (severity 色付きカード、suggestedFix 含む)

### Step 5: 呼び出し元への応答

subagent はこのスキル完了時に、最終応答テキストに以下を含めて返す:

- 生成パス: `screenshot_dir` / `findings.json` / `report.html` の絶対パス
- サマリ: critical / warning / note の件数、`hasCritical` 状態、全体所見
- findings の構造化要約 (severity 順、slide 番号付き、issue + suggestedFix を 1〜2 行で)
- `requiresHumanDecision: true` の項目を明示

例:
```
report_html=/path/to/.review/20260628-162236/report.html
findings_json=/path/to/.review/20260628-162236/findings.json
screenshot_dir=/path/to/.review/20260628-162236/screenshots

サマリ: critical 1 / warning 2 / note 1 (hasCritical=true)
全体所見: 主役画像の占有率不足が複数枚で見られる...

[critical]
- slide-03 / layout: 主役画像が小さすぎる → max-h-[60vh] → max-h-[85vh] (grid-cols-2 → grid-cols-5)

[warning]
- slide-04 / density: 文章と画像が二重提示 → 図 or 文章のどちらかへ統一 (要人間判断)
- slide-06 / visualization: 「崩れる→直す→また崩れる」の循環構造が箇条書きのまま → 循環図へ変換 (要人間判断)
- ...

[note]
- ...
```

呼び出し元 (メイン Claude) はこのテキストと HTML パスをユーザーに提示し、修正方針を確認する。

ユーザーの判断ルール:
- **critical**: 修正方針を 1 件ずつ確認 (基本は全件修正)
- **warning**: 「修正する / 保留 / 却下」のいずれかをユーザーに選ばせる
- **note**: 表示のみ。対応は任意

`requiresHumanDecision: true` の項目は AI が勝手に修正方針を確定しない。必ずユーザーに判断させる。

ユーザーが修正方針を承認したら、スライドを修正し **Step 1 から再ループ** する。

---

## 停止条件

以下のいずれかで終了:
- `summary.hasCritical` が `false` になった
- ループ反復が **3 回** を超えた
- ユーザーが「ここでやめる」「OK」など継続停止の意思を示した

---

## 注意事項・既知の制約

- `slidev export --per-slide` は v-clicks の最終状態を 1 枚にまとめる。クリックごとのレイアウト確認が必要なら `--with-clicks` を付ける
- スクショは `<slide-dir>/.review/<timestamp>/screenshots/` に出力される。過去ラウンドは保持されるので、レビュー履歴も追える
- 大量画像の Read はコンテキストを大きく消費する。スライド数が多い場合 `--range` で分割レビューしてもよい
- `--scale` を上げすぎると Read 時のメモリ負荷が増える。デフォルトの 2 (≈ 1920x1080) で十分
- `.review/` ディレクトリは Slidev プロジェクト側の `.gitignore` に登録しておくとよい
- 内容の正しさ (技術的事実、論理の流れ) はこのスキルの対象外
- **トーンの扱い**: 見出し・キャッチコピーのトーン (自己陶酔/演出過多など) の設計は
   **アウトライン段階の責務** で、本来は `slide-outline` 側で決まる。
   ただし実際に文章がレンダリングされた画面を見て初めて「気持ち悪さ」に気づくことがあるため、
   実装後のレビューで気づいた場合は `wording` カテゴリで `note` + `requiresHumanDecision: true` として報告してよい。
   **AI が独断でトーンを直さない** — 好みの判断は必ずユーザーに委ね、
   ユーザーが不要と判断したら `slide-outline` の申し送り事項には残さず終了する
- 画像素材自体の品質 (写真の見切れ、解像度不足) はクロップ済みかをユーザーに確認させる。Claude では再撮影できない
- **`visualization` の扱い**: 文章→図解の変換判断は本来 **アウトライン段階の責務** で、`slide-outline` 側の
   助詞・接続詞チェックで潰しておくのが基本。ただし実装済みの文言をレンダリングして初めて
   「これは図解した方が伝わる」と気づくことがあるため、実装後のレビューで検出した場合は
   `visualization` カテゴリで `warning` + `requiresHumanDecision: true` として報告する。
   ユーザーが変換不要と判断したら、そのスライドは以後のラウンドで再指摘しない
