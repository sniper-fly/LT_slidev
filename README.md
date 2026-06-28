# LT_slidev

sniper-fly の LT スライドを [`slidev-workspace`](https://github.com/leochiu-a/slidev-workspace) で 1 リポジトリ管理しているリポジトリです。

## クイックリファレンス

```bash
pnpm install                                       # 初回のみ
pnpm --filter ./slides/<topic> dev                 # 特定スライドを開発
pnpm dev                                           # 一覧 UI をローカルで起動
pnpm build                                         # 全スライド + 一覧ページを dist/ にビルド
pnpm export-og                                     # 各スライドの OG 画像を生成 (任意)
```

## このリポジトリ固有の設定

- `baseUrl: /LT_slidev` (`slidev-workspace.yaml`)
- 公開 URL パターン: `https://sniper-fly.github.io/LT_slidev/<topic>/`
- 一覧ページ: `https://sniper-fly.github.io/LT_slidev/`

## 新しいスライドを追加するには

1. `cp -r slides/_template slides/<new-topic>` で雛形をコピー
2. `slides/<new-topic>/package.json` の `name` と `dev` スクリプトの `--base /<new-topic>/` を新しいトピック名に書き換え
3. `slides/<new-topic>/slides.md` を書く
4. `pnpm install` で新パッケージを workspace に認識させる

詳しい仕様 (frontmatter で使える設定、サムネイル優先順位、`exclude` でのスキップなど) は公式 [`SKILL.md`](https://github.com/leochiu-a/slidev-workspace/tree/main/.claude/skills/slidev-migrate) と [公式ドキュメント](https://leochiu-a.github.io/slidev-workspace/) を参照。

## 既存スライド

- `slides/_template/` — 新スライドの雛形。`slidev-workspace.yaml` の `exclude` で公開ビルドからは除外しています。
- `slides/dokusen-anime-kuchiku/` — 過去のビアバッシュ LT「独占配信アニメ録画し忘れを一匹残らず駆逐する」。
- `slides/heartgarden/` — HeartGarden の LT (鋭意制作中)。

## 共通コンポーネント・レイアウトを使い回したくなったら

現時点では作成していません (YAGNI)。2 つ目以降のスライドで重複が出てきた段階で `packages/shared/` を切る方針です。共有方法の選択肢は 2 つあります。

- (a) Slidev addon として書き、各スライドの frontmatter に `addons: ["../../packages/shared"]` と指定
- (b) `slides/<topic>/setup/main.ts` で `defineAppSetup` 経由で `app.component()` を使い global 登録

どちらも Slidev 本体の公式機構なので、`slidev-workspace` 側で阻害されません。

## デプロイ

`main` への push で GitHub Actions (`.github/workflows/deploy.yml`) が `pnpm build` → `actions/upload-pages-artifact` → `actions/deploy-pages` を実行し、GitHub Pages に公開します。

## 参考リンク

- [slidev-workspace 公式 docs](https://leochiu-a.github.io/slidev-workspace/)
- [migration skill (`SKILL.md`)](https://github.com/leochiu-a/slidev-workspace/tree/main/.claude/skills/slidev-migrate)
- [デプロイガイド](https://leochiu-a.github.io/slidev-workspace/getting-started/deploy.html)
- [Slidev 公式ドキュメント](https://sli.dev/)
