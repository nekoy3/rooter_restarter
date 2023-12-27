import subprocess
import datetime

def log(string):
    return "[" + str(datetime.datetime.now()) + "]: " + string + "\n"

#動的にAレコードを変えるために設定ファイルを読み込んで変数に格納してcurlコマンドを実行したい

d = {}
with open('./config.txt') as f:
    lines = f.read()
    d = dict(zip(lines.split("\n")[6:11], lines.split("\n")[0:5]))
with open('./ip_addr.txt') as f:
    lines = f.read()
    d = {**d, 'ip_addr': lines}

f = open('restart_router.log', 'a')
f.write(log("running record set..."))
curl = [
    "curl",
    "--request", "PUT",
    "--url", "\"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}\"".format(
        zone_id=d['zone_id'],
        record_id=d['record_id']
    ),
    "--header", "\'Content-Type: application/json\'",
    "--header", "\"X-Auth-Email: {mail}\"".format(mail=d['mail']),
    "--header", "\"Authorization: Bearer {api_token}\"".format(api_token=d['api_token']),
    "--data", '\'{{"content": "{ip_addr}", "name": "{domain}", "proxied": true, "type": "A", "comment": "Domain verification record"}}\''.format(
        ip_addr=d['ip_addr'],
        domain=d['domain']
    )
]

curl_cmd = "".join([i + " " for i in curl])
r = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
result = str(r).split(",")

for s in result:
#    print("l: " + s)
    if s.startswith('\"success') or s.startswith('\"error'):
#        print(s)
        f.write(log(s))

f.write(log("Done!"))
f.close()