# GitHub PR承認時にUSB電源をONにするシステム

このシステムは、GitHubのプルリクエストが承認されたことをトリガーとして、ローカルPCに接続されたUSBデバイスの電源を自動的にONにします。

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
    *   このワークフローは、プルリクエストが承認されると、`test.mosquitto.org` の `github/pr/approved` トピックにメッセージを送信します。

## 使い方

1.  **ローカルスクリプトの実行:**

    以下のコマンドで、ローカルPCのスクリプトを起動します。これにより、MQTTブローカーからのメッセージを待ち受け状態になります。

    ```bash
    python local_usb_controller.py
    ```

2.  **GitHubでプルリクエストを承認:**

    このリポジトリでプルリクエストが作成され、それが承認されると、GitHub Actionsが作動します。

3.  **USB電源ON:**

    ローカルで実行しているスクリプトがMQTTメッセージを受信し、`UHUBCTL_COMMAND` で指定したコマンドを実行して、USBポートの電源をONにします。

## 注意事項

*   `test.mosquitto.org` は公開されているMQTTブローカーです。機密性の高い情報には使用しないでください。
*   `uhubctl` が対応しているUSBハブが必要です。すべてのハブで動作するわけではありません。
*   このシステムは簡易的なものであり、エラーハンドリングなどは最小限になっています。

## Workflow Test

This is a test to trigger the workflow.

Another small change for test-workflow-2.
