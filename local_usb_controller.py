import subprocess
import paho.mqtt.client as mqtt

# --- 設定項目 --- #

# MQTTブローカー
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "github/pr/approved"

# uhubctlコマンド
# 例: "uhubctl -l 1-2 -p 2 -a on"
UHUBCTL_COMMAND = "uhubctl -a on"

# --- コード --- #

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTTブローカーに接続しました。")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"MQTTブローカーへの接続に失敗しました。コード: {rc}")

def on_message(client, userdata, msg):
    print(f"メッセージ受信: {msg.topic} {msg.payload.decode()}")
    try:
        print(f"{UHUBCTL_COMMAND} を実行します。")
        subprocess.run(UHUBCTL_COMMAND, shell=True, check=True)
        print("USBポートの電源をONにしました。")
    except subprocess.CalledProcessError as e:
        print(f"コマンドの実行に失敗しました: {e}")
    except FileNotFoundError:
        print("エラー: 'uhubctl' コマンドが見つかりません。uhubctlがインストールされ、パスが通っていることを確認してください。")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("MQTTブローカーへの接続を試みています...")
        client.loop_forever()
    except KeyboardInterrupt:
        print("スクリプトを終了します。")
        client.disconnect()
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
