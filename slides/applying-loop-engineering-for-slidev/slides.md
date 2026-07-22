---
theme: default
title: 究極 vs 至高 スライド作成対決 —— Slidev × AI
info: |
  ループエンジニアリングの概念を、Slidev によるスライド作りに適用してみた話。
  このスライド自体も、紹介する方式で作られている。
transition: slide-left
fonts:
  sans: Noto Sans JP
  mono: Fira Code
highlighter: shiki
colorSchema: dark
duration: 5min
layout: full
---

<div style="position: absolute; inset: 2% 4%; display: flex; align-items: center; justify-content: center;">
  <img src="./assets/title_oishinbo_like.png" style="width: 100%; height: 100%; object-fit: contain;" />
</div>

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">自己紹介</div>

<div class="flex-1 flex items-start justify-between mt-6">
<div class="flex-1">

<div class="mb-4">
<span class="text-gray-400 text-xl">Name</span>
<div class="text-3xl font-bold mt-1">中井 亮</div>
</div>

<div class="mb-4">
<span class="text-gray-400 text-xl">Team</span>
<div class="text-2xl mt-1">PF開発本部 第一開発部<br>CSプラットフォーム AIチーム</div>
</div>

<div>
<span class="text-gray-400 text-xl">bio</span>
<div class="text-2xl mt-1 space-y-1">

- あにめぶ！（社内サークル）部長
- 斧で木を切ることより斧を研ぐほうが好きかも

</div>
</div>

</div>
<div class="ml-8 mt-2">
<img src="https://avatars.githubusercontent.com/u/50983271?v=4" class="w-64 h-64 rounded-full object-cover border-4 border-white/80" />
</div>
</div>
</div>

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">スライド作り、めんどくさくないですか</div>

<div class="flex-1 flex flex-col items-center justify-center gap-12">

<div class="grid grid-cols-2 gap-8 w-full px-16">

<div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-8 py-10 text-3xl text-center">
配置調整<br><span class="text-2xl opacity-70">マウスでポチポチ</span>
</div>

<div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-8 py-10 text-3xl text-center">
差分管理が<br>できない
</div>

</div>

</div>
</div>

<!--
LT はやりたいけど面倒で腰が引ける、という前置きは口頭で添える。
共感フックとして短く済ませる。次スライドの「AIで解決すればいい」への振りになる。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">AI と Slidev で解決すればいいのでは?</div>

<div class="flex-1 flex flex-col items-center justify-center gap-8">

<div class="flex items-center justify-center gap-6">

<div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-10 py-8 text-3xl text-center"><span class="whitespace-nowrap">Markdown/コード</span></div>
<div class="text-4xl opacity-60">→</div>
<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-10 py-8 text-3xl text-center">Slidev</div>
<div class="text-4xl opacity-60">→</div>
<div class="bg-purple-900/30 border border-purple-500/40 rounded-lg px-10 py-8 text-3xl text-center"><span class="whitespace-nowrap">スライド</span></div>

</div>

<div class="text-2xl opacity-70 text-center">Slidev: <span class="whitespace-nowrap">Markdown やコードからスライドを作れる</span><br><span class="whitespace-nowrap">(Vue コンポーネントの埋め込みも可能)</span></div>

<div class="text-3xl opacity-80 text-center">ここを AI が書けば自動でできるはず</div>

</div>
</div>

<!--
この「はず」が次のスライドで裏切られる、と匂わせてもよい。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">AI に丸投げすると、こうなりがち</div>

<div class="flex-1 mt-4" style="position: relative;">
  <img src="./assets/broken_example.png" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;" />
</div>

</div>

<!--
「これを AI に一発で作らせたら、こうなった」と一言添えて画像を見せる。結論は次スライドで言う。
画像と説明を同じ画面に同時提示すると分かりづらいという slide-review 指摘を受け、見出しで文脈を示しつつ画像本体は単独で見せる形にした。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">AI の手直しという別の仕事が生まれる</div>

<div class="flex-1 flex flex-col items-center justify-center gap-12">

<div class="grid gap-8 w-full px-16 items-center" style="grid-template-columns: 1fr auto 1fr;">

<div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-8 py-10 text-3xl text-center">
配置調整の面倒
</div>

<div class="text-4xl opacity-60">⇄</div>

<div class="bg-orange-900/30 border border-orange-500/40 rounded-lg px-8 py-10 text-3xl text-center">
<span class="whitespace-nowrap">AI への指示し直しの面倒</span>
</div>

</div>

<div class="text-3xl opacity-80 text-center">面倒さの場所が移動しただけ</div>

</div>
</div>

<!--
「指示を工夫すれば直る」という反論を先回りして潰す。
3 枚目「パワポでポチポチ」→ このスライド「AI に書かせても手直し指示という別の仕事が生まれる」という伏線と回収の対比。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">AI を真に活かすには</div>

<div class="flex-1 flex flex-col justify-center text-3xl leading-relaxed space-y-10">

<v-clicks>

- 真に AI 活用するには、<span class="whitespace-nowrap">業務フローを分解して</span><br><span class="whitespace-nowrap">それぞれを AI に最適化する必要がある</span>
- 最近話題の<span class="whitespace-nowrap">"ループエンジニアリング"</span>を<span class="whitespace-nowrap">適用できないか</span>

</v-clicks>

</div>
</div>

<!--
前スライドの Before/After (面倒さの場所が移動しただけ) を受けて、これは対症療法に過ぎないという流れで問題提起する。
-->

---

<div class="h-full flex flex-col">

<div class="shrink-0">
<div class="text-5xl font-bold">ループエンジニアリングの定義 3 種<br><span class="text-2xl opacity-60">(私見)</span></div>
</div>

<div class="flex-1 flex flex-col justify-center space-y-3 mt-2">

<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-8 py-4">
<div class="text-3xl"><strong class="text-green-300">① 目標達成ループ</strong></div>
<div class="text-2xl opacity-80 mt-2">目標達成まで実装と検証を繰り返すループ</div>
</div>

<div class="bg-cyan-900/30 border border-cyan-500/40 rounded-lg px-8 py-4">
<div class="text-3xl"><strong class="text-cyan-300">② 環境改善ループ</strong></div>
<div class="text-2xl opacity-80 mt-2">知識を記録・抽象化し、作業環境自体を改善し続けるループ</div>
</div>

<div class="bg-purple-900/30 border border-purple-500/40 rounded-lg px-8 py-4">
<div class="text-3xl"><strong class="text-purple-300">③ 問題発見ループ</strong></div>
<div class="text-2xl opacity-80 mt-2">そもそも何を実装すべきかを発見・定義し、<br>目標達成ループに投入するループ</div>
</div>

</div>
</div>

<!--
③ 問題発見ループは次の全体図には未反映であることも触れる (図の対応先が無い)。
番号 (①②③) は次スライドのワークフロー図との対応を口頭で示す。
-->

---
layout: full
---

<div style="position: absolute; inset: 2% 4%; display: flex; align-items: center; justify-content: center;">
  <img src="./assets/workflow.png" style="width: 100%; height: 100%; object-fit: contain;" />
</div>

<!--
ループエンジニアリングの概念を Slidev によるスライド作りに適用してみた、が本スライドのメッセージ。
① 目標達成ループ = ③④、② 環境改善ループ = ②アウトライン + 振り返り、③ 問題発見ループ = 今回の図にはまだ反映していない (今後の拡張余地) と口頭で明示する。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">レビュー自体の妥当性をレビューする</div>

<div class="flex-1 mt-4" style="position: relative;">
  <img src="./assets/review_report.gif" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;" />
</div>

</div>

<!--
report.html は、AI の検証基準そのものが正しく機能しているかを人間がメタ認知するための UI。
AI から AI へのフィードバックはテキストのみで、指摘が妥当かどうか人間が判断しづらい。
スクショと指摘を並べて表示することで、検証基準の妥当性を人間が素早く確認できる。
前スライドの ② 環境改善ループ (検証基準そのものを改善する) の具体例そのものである、と接続する。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">まとめ</div>

<div class="flex-1 flex flex-col justify-center text-3xl leading-snug space-y-5">

<v-clicks>

- ルールを書くだけでは AI は逸脱する<br><span class="whitespace-nowrap">検証基準のチューニングという地道な仕事が残る</span>
- 改行崩れや見切れは検知できるが<br><span class="whitespace-nowrap">演出や言い回しの判断は人間の判断が必要</span>
- <strong>スライド作成の自動化の道は、まだまだ遠い</strong>

</v-clicks>

</div>
</div>

<!--
動線 (Zenn 記事等) は現時点でなし。今後記事化する場合は別途追加。
「このスライドも、この方式で作りました」は口頭で補足する (伏線回収)。
-->
