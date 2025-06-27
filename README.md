# GitHub PRマージ時にUSB電源をONにするシステム

このシステムは、GitHubのプルリクエストがマージされたことをトリガーとして、ローカルPCに接続されたUSBデバイスの電源を自動的にONにします。

## 必要なもの

*   **Python 3**: [公式サイト](https://www.python.org/downloads/) からインストールしてください。
*   **uhubctl**: USBポートの電源を制御するためのコマンドラインツールです。
    *   インストール方法は [uhubctlのGitHubリポジトリ](https://github.com/mvp/uhubctl) を参照してください。
    *   Windowsの場合は、ソースからコンパイルするか、利用可能なバイナリを探す必要があります。
*   **Git**: [公式サイト](https://git-scm.com/downloads) からインストールしてください。

## セットアップ

1.  **リポジトリのクローンまたはダウンロード:**

    ```bash
    git clone <このリポジトリのURL>
    cd <リポジトリ名>
    ```

2.  **Pythonの依存ライブラリをインストール:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **`local_usb_controller.py` の設定:**

    スクリプト内の以下の項目を、お使いの環境に合わせて編集してください。

    *   `UHUBCTL_COMMAND`: `uhubctl` で電源をONにしたいUSBポートを指定するコマンドを記述します。
        *   まず、ターミナルで `uhubctl` を実行し、制御したいUSBハブとポートの情報を確認します。
        *   その情報を元に、電源をONにするための正確なコマンド（例: `uhubctl -l 1-2 -p 2 -a on`）をここに設定します。

4.  **GitHub Actionsの設定:**

    *   このリポジトリをGitHubにプッシュすると、`.github/workflows/mqtt-publish.yml` が自動的にActionsとして設定されます。
    *   このワークフローは、プルリクエストがマージされると、`test.mosquitto.org` の `github/pr/merged` トピックにメッセージを送信します。

## 使い方

1.  **ローカルスクリプトの実行:**

    以下のコマンドで、ローカルPCのスクリプトを起動します。これにより、MQTTブローカーからのメッセージを待ち受け状態になります。

    ```bash
    python local_usb_controller.py
    ```

2.  **GitHubでプルリクエストをマージ:**

    このリポジトリでプルリクエストが作成され、それがマージされると、GitHub Actionsが作動します。

3.  **USB電源ON:**

    ローカルで実行しているスクリプトがMQTTメッセージを受信し、`UHUBCTL_COMMAND` で指定したコマンドを実行して、USBポートの電源をONにします。

## 注意事項

*   `test.mosquitto.org` は公開されているMQTTブローカーです。機密性の高い情報には使用しないでください。
*   `uhubctl` が対応しているUSBハブが必要です。すべてのハブで動作するわけではありません。
*   このシステムは簡易的なものであり、エラーハンドリングなどは最小限になっています。

## このシステムをAIに作成させるためのプロンプトと準備

### プロンプトの例

以下のような詳細なプロンプトをAIに与えることで、このシステムを効率的に作成させることができます。

```
システム概要: GitHub PRが承認されたときに、GitHub ActionsからMQTTを経由してローカルPCのUSBポートの電源をONにするシステムを作成してください。

要件:
- 言語: Python メイン
- 用途: 一回限りの使い捨てシステム
- 優先事項: シンプルで理解しやすく、コード量は最小限
- 設定方法: コード内の一部を書き換えるだけで動作すること

技術スタック:
- GitHub Actions: PR承認時のトリガー (後にPRマージ時に変更)
- MQTT: paho-mqttライブラリ使用、test.mosquitto.orgを利用
- USB制御: uhubctlコマンドを使用
- Python 3: ローカルPC用のスクリプト

動作フロー:
1. GitHubでPRが承認される（pull_request_review - submitted - approved）
2. GitHub ActionsがMQTTブローカーにメッセージをpublish
3. ローカルPCのPythonスクリプトがMQTTメッセージをsubscribe
4. メッセージ受信時にuhubctlコマンドでUSBポートをON

作成すべきファイル:
- .github/workflows/mqtt-publish.yml - GitHub Actionsワークフローファイル
- local_usb_controller.py - ローカルで実行するPythonスクリプト
- requirements.txt - Pythonの依存ライブラリ
- README.md - 設定と使用方法の説明書

期待する出力:
- 動作確認済みのコード一式
- 簡潔で実用的なREADME
- 設定変更箇所の明確な記載
```

### 人間が事前に用意する必要があるもの

AIにこのシステムを作成させる前に、人間側で以下のものを準備しておく必要があります。

*   **GitHubリポジトリ**: 空のリポジトリでも構いません。AIがコードをプッシュするために必要です。
*   **GitHub Personal Access Token (PAT)**: AIがGitHubリポジトリにアクセスし、Actionsを操作するために必要です。以下のスコープを付与してください。
    *   `repo` (リポジトリの読み書き権限)
    *   `workflow` (GitHub Actionsのワークフローの読み書き権限)
*   **ローカルPCへのPython 3のインストール**: ローカルで実行するスクリプトのために必要です。
*   **ローカルPCへの `uhubctl` のインストールと設定**: USBポートを制御するためのコマンドラインツールです。お使いのOSに合わせてインストールし、パスを通しておく必要があります。
*   **インターネット接続**: MQTTブローカー (`test.mosquitto.org`) への接続のために必要です。