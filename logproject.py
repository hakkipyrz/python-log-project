import time
from datetime import datetime, timedelta

f = open("log.txt", "r")

ip_dict = {}
ip_time_dict = {}
banned_ips_dict = {}


for line in f:
    logtxt = str(line)
    log_split = logtxt.split()
    ip = log_split[0]
    timestamp = log_split[3][1:]
    dt_timestamp = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S")
    ip_time = ip + "---" + timestamp

    if ip in ip_dict:
        ip_dict[ip] += 1
    else:
        ip_dict[ip] = 1

    if ip_time in ip_time_dict:
        ip_time_dict[ip_time] += 1
    else:
        ip_time_dict[ip_time] = 1


def anomaly_detection():
    for ip_time, count in ip_time_dict.items():
        if count >= 5:
            print(f"Dikkat! {ip_time} için anormal durum tespit edildi, {count} istek gönderildi.")


def banned_ips():
    for ip_time, count in ip_time_dict.items():
        if count >= 5:
            timestamp_str = ip_time.split("---")[1]
            ban_time = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
            banned_ips_dict[ip_time] = ban_time


def check_bans():
    for ip_time, ban_time in list(banned_ips_dict.items()):
        ban_duration = (datetime.now() - ban_time).total_seconds()
        if ban_duration >= 2592000:  # 30 gün = 2592000 saniye
            ban_end_time = ban_time + timedelta(seconds=2592000)
            print(f"{ip_time} için ban süresi doldu ({int(ban_duration)} saniye). Ban kaldırıldı. Yasak kaldırılma zamanı: {ban_end_time.strftime('%d/%b/%Y:%H:%M:%S')}")
            del banned_ips_dict[ip_time]


print(f"IP istekleri: {ip_dict}")
print("-" * 50)


ip_dict_sorting = sorted(ip_dict.items(), key=lambda x: x[1], reverse=True)
print("IP İstek Sayısı (Büyükten Küçüğe):\n")
for ip, count in ip_dict_sorting:
    print(f"{ip} -> {count} istek")
print("-" * 50)


ip_time_dict_sorting = sorted(ip_time_dict.items(), key=lambda x: x[1], reverse=True)
print("IP'leri İlk İstek Zamanından Son İstek Zamanına Göre Sıralama:\n")
for ip_time, count in ip_time_dict_sorting:
    print(f"{ip_time} -> {count} istek")
print("-" * 50)


anomaly_detection()
banned_ips()
print("-" * 50)


print("Banlanan IP'ler:\n")
for ip_time, ban_time in banned_ips_dict.items():
    print(f"{ip_time} => Banlandı!, Ban tarihi: {ban_time.strftime('%d/%b/%Y:%H:%M:%S')}")

print("-" * 50)


print("Banlanan IP'ler Kontrol Ediliyor...\n")
time.sleep(5)

check_bans()


print("-" * 50)
print("Son Durumda Banlanan IP'ler:\n")
for ip_time, ban_time in banned_ips_dict.items():
    print(f"{ip_time} => Ban tarihi: {ban_time.strftime('%d/%b/%Y:%H:%M:%S')}")

