# 日常的な開発フローガイド

## 日時
2026-01-17

## 目的
Kiro、Claude Code、Codexの実際の使い分けと、日常的な開発ルーティンを明確化する

---

## 基本的な開発サイクル

### 1. 新機能開発の流れ

```
Human → Kiro → Claude Code → テスト → (失敗時) Codex → Human
```

#### ステップ1: 要件整理（Human + Kiro）

**使うツール**: Kiro

**やること**:
- 「〇〇機能を追加したい」と Kiro に伝える
- Kiroが仕様書を作成・更新する
  - `docs/requirements.md` - 何を作るか
  - `docs/design.md` - どう作るか
  - `docs/tasks.md` - 作業の分解

**例**:
```
Human: 「電卓に減算機能を追加したい」
Kiro: 「requirements.mdに減算機能の要件を追加します」
```

**成果物**: `docs/` 配下の仕様書

---

#### ステップ2: 実装（Claude Code）

**使うツール**: Claude Code

**やること**:
- `CLAUDE.md` を読み込ませる
- `docs/` の仕様書を参照させる
- 「この仕様を実装してください」と依頼

**例**:
```
Human: 「docs/tasks.md のタスク#2を実装してください」
Claude Code: 「subtract関数を実装します」
```

**成果物**: `src/` 配下の実装コード

---

#### ステップ3: テスト実行（Human）

**やること**:
```bash
pytest tests/
```

**判断**:
- ✅ テスト成功 → 完了
- ❌ テスト失敗 → ステップ4へ

---

#### ステップ4: デバッグ（Codex）

**使うツール**: Codex

**やること**:
- `CODEX.md` を読み込ませる
- エラーメッセージを渡す
- 「このエラーを修正してください」と依頼

**例**:
```
Human: 「test_subtract が失敗しました。エラーログを添付します」
Codex: 「subtract関数の型チェックが原因です。修正します」
```

**成果物**: 修正されたコード

---

#### ステップ5: 判断記録（Human）

**やること**:
- `reports/` に判断ログを記録
- なぜその修正をしたのか
- 仕様との整合性を確認

**例**: `reports/003_subtract_implementation.md`

---

## 2. バグ修正の流れ

```
Human → Codex → テスト → (仕様不明時) Kiro → Human
```

### パターンA: 明確なバグ

**使うツール**: Codex のみ

```
Human: 「add(1, 2) が 4 を返します」
Codex: 「計算ロジックのバグです。修正します」
```

### パターンB: 仕様が不明確

**使うツール**: Codex → Kiro

```
Codex: 「add(None, 1) の動作が仕様書に記載されていません」
Human: 「Kiro、エラー処理の仕様を追加してください」
Kiro: 「requirements.md にエラー処理の要件を追加します」
```

---

## 3. リファクタリングの流れ

```
Human → Kiro → Claude Code → テスト
```

**重要**: リファクタリングは「仕様変更」なので、Kiro から始める

```
Human: 「コードを整理したい」
Kiro: 「design.md にリファクタリング方針を追加します」
Claude Code: 「方針に従ってリファクタリングします」
```

---

## 実際の使い分けチャート

### どのAIを使うべきか？

```
質問: 何をしたい？

├─ 仕様を書きたい / 整理したい
│  → Kiro
│
├─ 新しい機能を実装したい
│  → Kiro（仕様） → Claude Code（実装）
│
├─ バグを修正したい
│  ├─ 原因が明確
│  │  → Codex
│  └─ 仕様が不明確
│     → Codex（事実整理） → Kiro（仕様明確化） → Codex（修正）
│
├─ コードを改善したい
│  → Kiro（方針） → Claude Code（実装）
│
└─ 判断が必要
   → Human
```

---

## よくある質問

### Q1: 小さな修正でも Kiro を通すべき？

**A**: 判断基準:
- タイポ修正 → 直接修正してOK
- ロジック変更 → Kiro で仕様確認
- 新機能追加 → 必ず Kiro から

### Q2: Claude Code と Codex の境界は？

**A**:
- **Claude Code**: 「これから作る」
- **Codex**: 「すでにあるものを直す」

### Q3: テストコードは誰が書く？

**A**:
- 新規テスト → Claude Code
- テスト修正 → Codex
- テスト方針 → Kiro

### Q4: 全部 Kiro でやってもいい？

**A**: 可能だが非効率
- Kiro は「仕様管理」に特化させる
- 実装は Claude Code に任せる方が速い

---

## 実践例: 減算機能の追加

### 実際の会話フロー

```
# ステップ1: 要件整理
Human → Kiro:
「電卓に減算機能を追加したい」

Kiro:
「requirements.md に減算機能の要件を追加します」
「design.md に subtract関数の設計を追加します」
「tasks.md にタスクを追加します」

# ステップ2: 実装
Human → Claude Code:
「CLAUDE.md を読んで、docs/tasks.md のタスク#2を実装してください」

Claude Code:
「subtract関数を src/example_app.py に実装します」
「test_subtract を tests/test_example.py に追加します」

# ステップ3: テスト
Human:
$ pytest tests/
→ FAILED: test_subtract

# ステップ4: デバッグ
Human → Codex:
「CODEX.md を読んで、このエラーを修正してください」
（エラーログを添付）

Codex:
「subtract関数の引数チェックが不足していました。修正します」

# ステップ5: 再テスト
Human:
$ pytest tests/
→ PASSED

# ステップ6: 記録
Human:
reports/003_subtract_implementation.md を作成
```

---

## まとめ

### 各AIの使い時

| AI | 使う場面 | 成果物 |
|---|---|---|
| **Kiro** | 仕様を書く・整理する | `docs/` |
| **Claude Code** | 新しく作る | `src/`, `tests/` |
| **Codex** | 壊れたものを直す | 修正コード |
| **Human** | 判断する・記録する | `reports/` |

### 迷ったら

1. 「これは仕様の話？実装の話？」を考える
2. 仕様の話 → Kiro
3. 実装の話 → Claude Code or Codex
4. 判断が必要 → Human

---

## 次のステップ

このガイドを使って、実際に機能追加やバグ修正を試してみてください。

運用しながら、自分のプロジェクトに合わせてカスタマイズしていくことをお勧めします。
