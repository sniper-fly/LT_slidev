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

<div class="flex-1 flex flex-col justify-center text-3xl leading-relaxed space-y-16">

<v-clicks>

- LT はやりたいけど、スライド作りの面倒さで腰が引ける
- パワポでポチポチと配置を合わせる
- レイアウト崩れを都度手で直す

</v-clicks>

</div>
</div>

<!--
共感フックとして短く済ませる。次スライドの「AIで解決すればいい」への振りになる。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">AI と Slidev で解決すればいいのでは?</div>

<div class="flex-1 flex flex-col justify-center text-3xl leading-relaxed space-y-10">

<v-clicks>

- <strong>Slidev とは</strong>: Markdown だけでスライドが書ける <span class="whitespace-nowrap">OSS フレームワーク</span><br>
  <span class="text-xl opacity-70">(コードのシンタックスハイライトや <span class="whitespace-nowrap">Vue コンポーネント</span>の埋め込みなど、<span class="whitespace-nowrap">開発者向け</span>の機能を持つ)</span>
- AI に書かせれば、自動でいい感じにしてくれるはず

</v-clicks>

</div>
</div>

<!--
この「はず」が次のスライドで裏切られる。装飾は入れず、期待感だけを素朴に提示する。
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

<div class="flex-1 flex flex-col justify-center text-3xl leading-relaxed space-y-10">

<v-clicks>

- 崩れたレイアウトを直すよう、AI に<span class="whitespace-nowrap">指示を出し直す羽目になる</span>
- 最近提唱されている<span class="whitespace-nowrap">"ループエンジニアリング"</span>という<span class="whitespace-nowrap">考え方を、スライド作成にも適用</span>してみる

</v-clicks>

</div>
</div>

<!--
「指示を工夫すれば直る」という反論を先回りして潰す。
3 枚目「パワポでポチポチ」→ このスライド「AI に書かせても手直し指示という別の仕事が生まれる」という伏線と回収の対比。
-->

---

<div class="h-full flex flex-col">

<div class="text-5xl font-bold shrink-0">ループエンジニアリングとは</div>

<div class="flex-1 flex flex-col justify-center text-2xl">

<table class="w-full border-collapse">
<colgroup>
<col style="width: 24%">
<col style="width: 32%">
<col style="width: 44%">
</colgroup>
<thead>
<tr class="border-b-2 border-white/30">
<th class="text-left py-2 px-3"></th>
<th class="text-left py-2 px-3 opacity-70 whitespace-nowrap">プロンプトエンジニアリング</th>
<th class="text-left py-2 px-3 text-cyan-300 whitespace-nowrap">ループエンジニアリング</th>
</tr>
</thead>
<tbody class="leading-snug">
<tr class="border-b border-white/10">
<td class="py-2 px-3 font-bold text-green-300">人間が<br>設計するもの</td>
<td class="py-2 px-3 opacity-80">プロンプト<br><span class="text-xl opacity-70">(1 回の指示文)</span></td>
<td class="py-2 px-3">ループ全体<br><span class="text-xl opacity-70">(ゴール・検証基準・終了条件・<span class="whitespace-nowrap">実行環境</span>)</span></td>
</tr>
<tr class="border-b border-white/10">
<td class="py-2 px-3 font-bold opacity-60">検証基準</td>
<td class="py-2 px-3 opacity-80">人間の目視確認</td>
<td class="py-2 px-3">Test / Lint 等の機械的基準 +<br><strong>AI 自体を判定者として組み込む</strong></td>
</tr>
<tr>
<td class="py-2 px-3 font-bold opacity-60">実行主体</td>
<td class="py-2 px-3 opacity-80">人間が都度実行</td>
<td class="py-2 px-3">AI が自律的に反復実行</td>
</tr>
</tbody>
</table>

</div>
</div>

<!--
出典 (Zenn 記事、The New Stack 等) は口頭で軽く触れる程度、スライドには出さない。
-->

---

<div class="h-full flex flex-col">

<div class="shrink-0">
<div class="text-4xl font-bold">ループエンジニアリングの定義 3 種 <span class="text-2xl opacity-60">(私見)</span></div>
</div>

<div class="flex-1 flex flex-col justify-center space-y-3 mt-2">

<div class="bg-blue-900/30 border border-blue-500/40 rounded-lg px-8 py-4">
<div class="text-3xl"><strong class="text-blue-300">① 目標達成ループ</strong></div>
<div class="text-xl opacity-80 mt-2">目標達成まで実装と検証を繰り返すループ</div>
</div>

<div class="bg-green-900/30 border border-green-500/40 rounded-lg px-8 py-4">
<div class="text-3xl"><strong class="text-green-300">② 環境改善ループ</strong></div>
<div class="text-xl opacity-80 mt-2">知識を記録・抽象化し、作業環境自体を改善し続けるループ</div>
</div>

<div class="bg-purple-900/30 border border-purple-500/40 rounded-lg px-8 py-4">
<div class="text-3xl"><strong class="text-purple-300">③ 問題発見ループ</strong></div>
<div class="text-xl opacity-80 mt-2">そもそも何を実装すべきかを発見・定義し、<br>目標達成ループに投入するループ</div>
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

<div class="text-5xl font-bold shrink-0">人間がレビューしやすい UI</div>

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

- スライド作成も AI 時代なら<span class="whitespace-nowrap">「ワークフローとして再設計」できる</span>
- ルールを書くだけでは AI は逸脱する<br><span class="whitespace-nowrap">検証基準のチューニングという地道な仕事が残る</span>
- <strong>このスライドも、この方式で作りました</strong>

</v-clicks>

</div>
</div>

<!--
動線 (Zenn 記事等) は現時点でなし。今後記事化する場合は別途追加。
-->
