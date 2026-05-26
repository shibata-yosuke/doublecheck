# doublecheck

`doublecheck` は、調査票の Excel ファイルと Freeasy の Preview URL を見比べて、設問や分岐、表現の不整合を確認するための `Codex CLI` 用プラグインです。

この README は、エンジニアではない人でも導入できるように、`Codex CLI` の準備から順番に説明しています。

## 1. できること

`doublecheck` を使うと、次の流れで確認作業を進められます。

1. 調査票の `.xlsx` ファイルを読む
2. Freeasy の Preview 画面を開く
3. 設問文、選択肢、分岐、スケール、画像の見やすさなどを確認する
4. Preview画面はスクリーンショットを取得して、目視確認を行う
5. 問題点を会話画面に表示する
6. 結果を日本語の `doublecheck_YYYY_MM_DD_HHmm.md` という Markdown ファイルでも保存する

## 2. 事前に必要なもの

Windows 11 または macOS のどちらかで使えます。

事前に必要なのは次の 3 つです。

1. `ChatGPT` の利用できるアカウント
2. `Node.js`
3. `Codex CLI`

`doublecheck` 自体は配布スクリプトで入りますが、`Codex CLI` 本体は先に入れておく必要があります。

## 3. Codex CLI を 0 からセットアップする

### 3-1. Node.js を入れる

`Codex CLI` は `npm` を使ってインストールします。`npm` は通常 `Node.js` を入れると一緒に使えるようになります。

Node.js の公式サイト:

https://nodejs.org/

インストール後、ターミナルで次のコマンドが動けば準備完了です。

Windows:

```powershell
node --version
npm --version
```

macOS:

```sh
node --version
npm --version
```

### 3-2. Codex CLI を入れる

OpenAI の案内に沿って、`Codex CLI` をインストールします。

Windows / macOS 共通:

```sh
npm i -g @openai/codex
```

### 3-3. Codex CLI にログインする

インストール後、次を実行します。

```sh
codex --login
```

ブラウザが開いたら、`Sign in with ChatGPT` でログインします。

ログイン完了後、次のように `codex` コマンドが起動できれば準備完了です。

```sh
codex
```

## 4. このプラグインを入れる

このプラグインは、GitHub をブラウザで開かなくても、1 行で導入できます。

配布元:

https://github.com/shibata-yosuke/doublecheck

### 4-1. いちばん簡単な入れ方

#### Windows 11

PowerShell で次を実行します。

```powershell
irm https://raw.githubusercontent.com/shibata-yosuke/doublecheck/main/install-remote.ps1 | iex
```

#### macOS

ターミナルで次を実行します。

```sh
curl -fsSL https://raw.githubusercontent.com/shibata-yosuke/doublecheck/main/install-remote.sh | bash
```

この方法では、GitHub 上のこのリポジトリから必要ファイルを自動取得して、インストールまで進みます。

### 4-2. インストール後にプラグインを有効化する

インストールが終わっただけでは、すぐには使えないことがあります。

`Codex CLI` を起動して、`/plugins` から `doublecheck` をオンにしてください。

手順:

1. ターミナルで `codex` を起動する
2. `Codex CLI` の入力欄で `/plugins` と入力する
3. プラグイン一覧から `doublecheck` を見つける
4. `doublecheck` を `On` にする

有効化が終わったら、通常どおり `doublecheck <Preview_URL> <Excelファイル名>` で使えます。

### 4-3. 手元にこのフォルダがある場合の入れ方

このリポジトリ一式をすでに手元へ置いている場合は、ローカルの配布スクリプトでも入れられます。

### Windows 11

PowerShell でこのフォルダを開いて、次を実行します。

```powershell
.\install-doublecheck.ps1
```

### macOS

ターミナルでこのフォルダを開いて、次を実行します。

```sh
./install-doublecheck.sh
```

この処理で、主に次の 2 つが行われます。

1. `doublecheck` プラグイン本体を `~/plugins/doublecheck` に配置
2. `Codex CLI` の個人用 marketplace に `doublecheck` を登録

## 5. 使い方

### 5-1. 事前準備

使う前に、次の 2 つを手元に用意します。

1. 調査票の Excel ファイル
2. Freeasy の Preview URL

Excel ファイルは `.xlsx` 形式を使ってください。

### 5-2. 作業フォルダを開く

調査票の Excel ファイルが入っているフォルダで、`Codex CLI` を起動します。

例:

```sh
cd 調査票が入っているフォルダ
codex
```

もしまだ有効化していない場合は、先に `/plugins` を開いて `doublecheck` を `On` にしてください。

### 5-3. doublecheck を実行する

`Codex CLI` の会話入力で、次の形で実行します。

```text
doublecheck <Preview_URL> <Excelファイル名>
```

例:

```text
doublecheck https://monitor.research-plus.net/enquete_preview_list/?e=xxxx questionnaire.xlsx
```

### 5-4. 実行結果

正常に完了すると、次の 2 つが出ます。

1. `Codex CLI` の画面に要点が表示される
2. 実行したフォルダに日本語の Markdown レポートが保存される

また、Preview 画面については、スクリーンショットを使った目視確認を行う前提です。  
スクリーンショットが取得できない場合や、見た目を確認できない場合は、レビュー完了扱いにしない運用です。

保存されるファイル名の例:

```text
doublecheck_2026_05_26_1437.md
```

## 6. よくあるエラー

### Excel ファイルが見つからない

`doublecheck` を実行したフォルダに対象の `.xlsx` があるか確認してください。

### `.xlsx` 以外のファイルを指定した

このプラグインは `.xlsx` 前提です。`.xlsm` や `.csv` ではなく、`.xlsx` を使ってください。

### `npx` が見つからない

`Node.js` が正しく入っていない可能性があります。`node --version` と `npm --version` を確認してください。

### `codex --login` ができない

`Codex CLI` が最新版でない可能性があります。OpenAI の案内に従って更新してください。

## 7. アンインストール

### 7-1. 1 行でアンインストールする

#### Windows 11

```powershell
irm https://raw.githubusercontent.com/shibata-yosuke/doublecheck/main/uninstall-remote.ps1 | iex
```

#### macOS

```sh
curl -fsSL https://raw.githubusercontent.com/shibata-yosuke/doublecheck/main/uninstall-remote.sh | bash
```

### 7-2. 手元にこのフォルダがある場合

不要になったら、次のスクリプトで削除できます。

### Windows 11

```powershell
.\uninstall-doublecheck.ps1
```

### macOS

```sh
./uninstall-doublecheck.sh
```

この処理で、次の 2 つを削除します。

1. `~/plugins/doublecheck`
2. 個人用 marketplace に登録された `doublecheck` エントリ

## 8. ファイル構成

主なファイルは次の通りです。

- [plugin/doublecheck](C:/Users/yamat/Documents/doublecheck/plugin/doublecheck): 配布されるプラグイン本体
- [install-doublecheck.ps1](C:/Users/yamat/Documents/doublecheck/install-doublecheck.ps1): Windows 用インストーラ
- [install-doublecheck.sh](C:/Users/yamat/Documents/doublecheck/install-doublecheck.sh): macOS 用インストーラ
- [install-remote.ps1](C:/Users/yamat/Documents/doublecheck/install-remote.ps1): GitHub から直接入れる Windows 用ブートストラップ
- [install-remote.sh](C:/Users/yamat/Documents/doublecheck/install-remote.sh): GitHub から直接入れる macOS 用ブートストラップ
- [uninstall-doublecheck.ps1](C:/Users/yamat/Documents/doublecheck/uninstall-doublecheck.ps1): Windows 用アンインストーラ
- [uninstall-doublecheck.sh](C:/Users/yamat/Documents/doublecheck/uninstall-doublecheck.sh): macOS 用アンインストーラ
- [uninstall-remote.ps1](C:/Users/yamat/Documents/doublecheck/uninstall-remote.ps1): GitHub から直接実行する Windows 用アンインストーラ
- [uninstall-remote.sh](C:/Users/yamat/Documents/doublecheck/uninstall-remote.sh): GitHub から直接実行する macOS 用アンインストーラ
- [scripts/upsert_marketplace.py](C:/Users/yamat/Documents/doublecheck/scripts/upsert_marketplace.py): marketplace 登録・解除の共通処理
- [tests](C:/Users/yamat/Documents/doublecheck/tests): テスト


## 参考

`Codex CLI` のセットアップとログインは、OpenAI の公式情報を元にしています。

- OpenAI Help: Codex CLI and Sign in with ChatGPT  
  https://help.openai.com/en/articles/11381614-api-codex-cli-and-sign-in-with-chatgpt
- OpenAI Help: Using Codex with your ChatGPT plan  
  https://help.openai.com/en/articles/11369540/
