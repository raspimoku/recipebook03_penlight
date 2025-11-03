#!/usr/bin/env python3
import http.server
import ssl
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 自己署名証明書の生成コマンドを表示
print("=" * 60)
print("自己署名証明書が必要です。以下のコマンドで生成してください：")
print()
print("openssl req -x509 -newkey rsa:2048 -nodes \\")
print("  -keyout key.pem -out cert.pem -days 365 \\")
print("  -subj '/CN=localhost'")
print()
print("=" * 60)

# 証明書の存在確認
if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
    print("\nエラー: cert.pem と key.pem が見つかりません")
    print("上記のコマンドを実行してから、再度このスクリプトを実行してください")
    exit(1)

handler = MyHTTPRequestHandler
httpd = http.server.HTTPServer(('localhost', PORT), handler)

# SSL設定
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"\nHTTPSサーバーを起動しました")
print(f"アクセスURL: https://localhost:{PORT}")
print(f"\n注意: 自己署名証明書のため、ブラウザで警告が表示されます")
print(f"      「詳細設定」→「localhost にアクセスする（安全ではありません）」を選択してください")
print(f"\nCtrl+C で停止\n")

httpd.serve_forever()
