---
name: slide-review-run
description: |
  Slidev スライドレビューを 1 コマンドで起動するメタスキル。
  ユーザーが `/slide-review-run [<slide-dir>]` と打つと、メイン Claude が
  general-purpose subagent を起動し、slide-review スキルを実行させ、レポートを受け取って提示する。

  以下のようなケースでこのスキルを使うこと:
  - `/slide-review-run` と明示的に呼ばれた場合
  - 「スライドレビュー走らせて」「スライドをレビューして」などユーザー主導でレビュー起動の意図が明確な場合
disable-model-invocation: true
---

# slide-review-run — スライドレビュー起動メタスキル

## 役割

ユーザーが 1 コマンドで Slidev スライドレビューを起動するためのエントリーポイント。
レビュー本体 (スクショ取得・画像評価・JSON/MD 生成) は **subagent (general-purpose)** に委譲し、
メイン Claude のコンテキストを画像で消費しないようにする。

レビュー手順の詳細は `.claude/skills/slide-review/SKILL.md` 側で定義されている。
**このメタスキルは細かい指示を持たず、薄い委譲レイヤーに徹する。**

---

## 実行手順

### Step 1: 対象スライドディレクトリを決定

- 引数で `<slide-dir>` が渡されていればそれを採用 (存在チェックのみ)
- 渡されていなければ、AskUserQuestion でユーザーに指定させる (必要なら候補を提案するが、勝手に決めない)

### Step 2: subagent 起動

`Agent` ツールを以下で呼ぶ:

- `subagent_type`: `"general-purpose"`
- `description`: `"Slide review loop"`
- `prompt`: 最小テンプレート (下記) を使う。状況に応じて追記してよい

#### 最小プロンプトテンプレート

メタスキル側で以下を埋め込んだ上で subagent に渡す:
- `<repo-root>`: `pwd` 等で取得したリポジトリルートの絶対パス
- `<slide-dir>`: 対象スライドディレクトリ (絶対パス推奨)
- `<timestamp>`: capture.sh 実行時に生成される (subagent 側で取得)

```
Skill ツールで `slide-review` スキルを呼び出し、ロードされた手順に従って
以下のスライドを 1 ループ分レビューしてください。

対象スライド: <slide-dir>

実行スクリプト:
- capture.sh: <repo-root>/.claude/skills/slide-review/scripts/capture.sh
  使い方: `bash <repo-root>/.claude/skills/slide-review/scripts/capture.sh <slide-dir>`
  実行後の最終行に `screenshot_dir=<path>` が出力される。そこを SHOTS_DIR として使う。
- generate_report_html.py: <repo-root>/.claude/skills/slide-review/scripts/generate_report_html.py
  使い方: `python3 <path> <findings.json>` → 最終行に `report_html=<path>` を出力

成果物 (すべて <slide-dir>/.review/<timestamp>/ 配下):
- screenshots/*.png  ← capture.sh が生成
- findings.json     ← レビュー結果を書き出し
- report.html       ← generate_report_html.py が findings.json から生成 (人間用)

応答テンプレート (この内容を最終応答に含める):
- 生成パス: screenshot_dir / findings.json / report.html の絶対パス
- サマリ: critical / warning / note の件数、hasCritical 状態、全体所見
- findings 構造化要約 (severity 順、slide 番号付き、issue + suggestedFix を簡潔に)
- requiresHumanDecision: true の項目は明示

※ Markdown ファイルは作らない。応答テキスト = 呼び出し元への戻り値。
```

詳細手順・観点 (layout/readability 等)・JSON スキーマ・制約はすべて `slide-review/SKILL.md` 側に書いてあるので、ここで重複させない。

**追記してよい状況の例** (任意・必要なときだけ):
- レビュー範囲を絞りたい → 「`--range 1-5` を付けて capture.sh を実行」など
- 過去ラウンドの findings を踏まえてほしい → 該当 findings.json のパスを prompt に添える
- 特定観点を重視したい → 「特に layout と readability に注目」など

### Step 3: レポートをユーザーに提示

subagent の応答テキスト (findings 構造化要約) を整形してユーザーに提示する。
あわせて `report.html` の絶対パスを案内する (ブラウザで開けば、スクショと改善点を 1 画面で見られる)。

修正方針の確認ルール:
- critical: 基本全件修正 (1 件ずつ確認)
- warning: 「修正する / 保留 / 却下」をユーザーに選ばせる
- note: 表示のみ。対応は任意
- `requiresHumanDecision: true` の項目は勝手に方針を決めず、必ずユーザー判断

### Step 4: 修正の実行

ユーザー承認後、メイン Claude が `slides.md` 等を Edit で直接修正する。

### Step 5: 再ループ判断

ユーザーに「もう一回レビューしますか?」と確認。
やるなら Step 2 から再度 subagent を起動。

---

## 停止条件

- `summary.hasCritical` が `false` かつユーザーが OK と判断
- ループ反復が **3 回** を超えた
- ユーザーが明示的に停止を指示

## 注意

- メタスキル自身は **画像を Read しない**。Read は subagent 側のみ
- レビュー手順の改修は `slide-review/SKILL.md` 側で行い、このメタは触らない
