---
theme: default
title: 俺は、すべてのAIサンドボックスを過去にする!
info: |
  HeartGarden — AI コーディング時代の多層防御サンドボックス。
  Loop Engineering 時代の AI コーディングで、安全性と速度・利便性を両立させる試み。
transition: slide-left
fonts:
  sans: Noto Sans JP
  mono: Fira Code
highlighter: shiki
colorSchema: dark
duration: 5min
---

<div class="h-full flex flex-col items-center justify-center text-center">

<div class="text-5xl font-bold leading-tight title-gradient">
俺は、すべてのAIサンドボックスを<br>過去にする!
</div>

<div class="mt-10 text-xl opacity-80">
AI コーディング時代の多層防御サンドボックス
</div>

</div>

<style>
.title-gradient {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 50%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>

---

# 自己紹介

<div class="flex justify-between items-center mt-4">
<div class="flex-1">

<div class="mb-6">
<span class="text-gray-400 text-sm">Name</span>

### 中井 亮
</div>

<div class="mb-6">
<span class="text-gray-400 text-sm">Team</span>

PF開発本部 第4開発部<br>CSプラットフォーム AIチーム
</div>

<div>
<span class="text-gray-400 text-sm">bio</span>

- あにめぶ！部長
- 左ききのエレン、面白いよね
- ソフトウェア工学の話とか好き
  - 斧で木を切ることより斧を研ぐほうが好きかも
- `#times_nakai_ryo`

</div>

</div>
<div class="ml-8">
<img src="https://avatars.githubusercontent.com/u/50983271?v=4" class="w-60 h-60 rounded-full object-cover border-4 border-white/80" />
</div>
</div>

---

# コーディングエージェント承認地獄

<div class="grid grid-cols-5 gap-10 mt-6">
<div class="col-span-2 space-y-6 text-xl leading-relaxed">

- 理想: 仕事を投げて、終わったら成果物を見る

<v-clicks>

- 現実: 作業が終わるまで張り付いて**お守り**

- 承認疲れでとりあえず **YES 連打**

</v-clicks>

</div>
<div class="col-span-3 relative" style="height: 85vh;">

<div v-click="[1, 2]" class="absolute inset-0 flex items-start justify-center overflow-visible">
  <img src="./assets/approve_hell.png" class="rounded shadow max-w-full max-h-full object-contain" style="transform: translateX(-3em) scale(1.65); transform-origin: top left;" />
</div>

<div v-click="2" class="absolute inset-0 flex items-start justify-center">
  <img src="./assets/yes_jotaro.jpg" class="rounded shadow max-w-full max-h-full object-contain" />
</div>

</div>
</div>

<!--
AI を使う人なら誰でも体感する痛み。共感フックとして開幕で打ち抜く。
Loop Engineering の話につなげる: ループの肝は「待たないこと」なのに、承認で待たされたら本末転倒。
-->

---

# ほったらかすと時々主人に牙をむいてくる AI

<div class="mt-2 text-xl leading-relaxed space-y-6">

<v-clicks>

- <span class="whitespace-nowrap font-mono">--dangerously-skip-permissions</span> で承認をすべてスキップできる
- 手放しで **99% は問題ない**
- でも、信頼して任せすぎた結果... **`rm -rf ~/`**

</v-clicks>

</div>

<div v-after class="mt-4">
  <img src="./assets/rm_rf.png" class="rounded shadow w-full max-h-[60vh] object-contain" />
</div>

<!--
バズツイートでホスト破壊された実例。手放しの代償は重い。
ここまでで「都度承認は摩擦、手放しは危険」というジレンマを提示。
-->

---

# じゃあ Docker コンテナで囲めば...?

<div class="mt-8 text-xl leading-relaxed space-y-6">

<v-clicks>

- たしかに、**ホスト環境を壊されるリスクは消える**
- しかし、別の痛みが現れる
  - 開発に必要なツールが揃っていない → **Dockerfile を自分で盆栽する手間**
  - 必要な道具が増えるたびに **毎回イメージをビルドし直す手間**
- **コンテナでも防げない問題がある**

</v-clicks>

</div>

<!--
コンテナは一見万能だが、運用面の痛み (盆栽 / 再ビルド) と、
このあと 6 枚目で出てくる「コンテナでは防げない情報流出」という二段構成。
-->

---

# コンテナで守れるのは<br>ホストのファイルだけ

<div class="mt-6 text-xl leading-relaxed space-y-6">

<div class="opacity-80">
実害シナリオ: Brave 検索 API キーを環境変数で渡したコンテナで Web 検索を実行
</div>

<v-clicks>

- 環境変数 <code>BRAVE_API_KEY=xxx</code> を AI の作業環境に渡す
- AI が Brave Search で Web 検索を実行
- 検索結果の Web ページに <strong>Prompt Injection</strong> が紛れていた
- AI が Prompt Injection に従い、<strong>API キーを外部サーバーへ POST</strong>
- → コンテナの FS 分離は無力。<strong>持っている秘密は漏れる</strong>

</v-clicks>

</div>

<!--
ここが LT の核心。コンテナは外部通信の「内容」までは検閲しない。
PI を入口で完全には防ぎきれないので、漏れても気づく・漏れにくいアーキを組む必要がある。
-->

---
layout: full
---

<div style="position: absolute; inset: 2% 4%; display: flex; align-items: center; justify-content: center;">
  <img src="./assets/tradeoff.png" style="width: 100%; height: 100%; object-fit: contain;" />
</div>

<!--
口頭で「安全性と速度・利便性双方を満たすものがない。右上が空いている。ここに HeartGarden を作りました」と宣言する。
画像を絶対配置で viewport いっぱいに広げて object-contain で最大化。
-->

---
layout: center
class: text-center
---

<div class="text-4xl opacity-80 mb-6">そこで</div>

<div class="text-6xl font-bold title-gradient leading-tight">
HeartGarden を作りました
</div>

<style>
.title-gradient {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 50%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>

<!--
7 (右上が空いている) と 8 (使い方) のつなぎ。
ここで初めて HeartGarden の名前を強調する。
-->

---

# 使い方

<div class="h-full flex flex-col items-center justify-center -mt-8">

<div class="text-6xl font-mono bg-gray-900/60 rounded-lg px-12 py-8 border border-white/20">
<span class="text-green-400">$</span> hg claude
</div>

<div class="mt-12 text-xl opacity-90 text-center leading-relaxed">
Podman のコンテナ上で Claude Code が起動します
</div>

</div>

<!--
エージェント実装に依存しない設計。Claude Code 以外に Codex / OpenCode などでも同じ枠組み。
5 枚目の「永続化されない」痛みも mise + 名前付きボリュームで解決済み。
-->

---

# HeartGarden の 5 つの機能

<div class="grid grid-cols-3 gap-5 mt-8">

<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-5 py-6">
<div class="text-3xl">🛡️</div>
<div class="font-bold mt-2 text-green-300 text-base">FS 分離</div>
<div class="text-sm mt-1 opacity-80">ホストとコンテナの<br>ファイルシステムが分離 (Podman)</div>
</div>

<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-5 py-6">
<div class="text-3xl">🔑</div>
<div class="font-bold mt-2 text-green-300 text-base">鍵を知らずに認証</div>
<div class="text-sm mt-1 opacity-80">AI が API キーを<br>知らなくても認証できる</div>
</div>

<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-5 py-6">
<div class="text-3xl">🔍</div>
<div class="font-bold mt-2 text-green-300 text-base">PI 検知</div>
<div class="text-sm mt-1 opacity-80">プロンプトインジェクションを<br>入口で検知</div>
</div>

<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-5 py-6">
<div class="text-3xl">📜</div>
<div class="font-bold mt-2 text-green-300 text-base">通信監査</div>
<div class="text-sm mt-1 opacity-80">アウトバウンドのリクエストを<br>記録・監査できる</div>
</div>

<div class="bg-cyan-900/30 border border-cyan-500/40 rounded-lg px-5 py-6 col-span-2">
<div class="text-3xl">⚡</div>
<div class="font-bold mt-2 text-cyan-300 text-base">mise 標準搭載 & 永続化</div>
<div class="text-sm mt-1 opacity-80">開発ツールはコンテナを消しても残る → 毎回 Dockerfile を再ビルドしなくていい</div>
</div>

</div>

<!--
安全系 4 + 利便系 1 で色分け。
実現手段 (Bifrost / egress-proxy / Guardrails) はあえて出さない。次のアーキ図で説明。
-->

---
layout: full
---

<div style="position: absolute; inset: 2% 4%; display: flex; align-items: center; justify-content: center;">
  <img src="./assets/architecture.png" style="width: 100%; height: 100%; object-fit: contain;" />
</div>

<!--
口頭で「3 層で守る — 入口・出口・鍵分離」と説明。
- 入口: Bedrock Guardrails で PI を検知
- 出口: mitmproxy + 三段 DLP で外部通信を監査
- 鍵分離: Bifrost が LLM API キーを、egress-proxy がツール API キーを肩代わり
Workspace は鍵を持たない。だから漏れない。
-->

---

# まとめ

<div class="grid grid-cols-5 gap-8 mt-8 items-center">

<div class="col-span-3 text-xl leading-relaxed space-y-6">

- 100% 安心してほったらかせる環境を作るのは大変
- 銀の弾丸ではない、まだ課題もある
- <span class="whitespace-nowrap">コンテナだけでは塞ぎきれない</span><span class="whitespace-nowrap">アウトバウンドのリクエスト</span>に関する<span class="whitespace-nowrap">脆弱性に対する解決策</span>の提案
- Zenn の解説記事を書きました →

</div>

<div class="col-span-2 flex flex-col items-center">

<img src="./assets/QR_637531.png" class="w-48 h-48 bg-white p-2 rounded" />

<div class="mt-3 text-xs opacity-70 text-center">Zenn 記事</div>
<div class="text-xs font-mono opacity-80 text-center break-all">
zenn.dev/sniper-fly/articles/<br>heartgarden-multilayer-sandbox
</div>

</div>

</div>

<!--
締めの一言を口頭で添えて終わる。
QR コードを読んで Zenn 記事へ。GitHub は記事から辿れる。
-->
