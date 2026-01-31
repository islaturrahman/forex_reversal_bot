# 🖥️ Panduan Deploy ke Linux VPS

## Persiapan VPS

### 1. Login ke VPS
```bash
ssh root@your_vps_ip
# atau
ssh username@your_vps_ip
```

### 2. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 3. Install Dependencies
```bash
# Install Python 3 dan tools
sudo apt-get install -y python3 python3-pip python3-venv git screen

# Verifikasi instalasi
python3 --version
pip3 --version
```

## Deploy Bot

### Opsi 1: Menggunakan Script Otomatis (RECOMMENDED)

```bash
# Clone repository
git clone YOUR_REPO_URL
cd reversal_bot

# Jalankan script deployment
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### Opsi 2: Manual Setup

```bash
# Clone repository
git clone YOUR_REPO_URL
cd reversal_bot

# Buat virtual environment
python3 -m venv venv

# Aktivasi virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy dan edit .env
cp .env.example .env
nano .env
```

## Konfigurasi

### Edit file .env
```bash
nano .env
```

Isi dengan credentials Anda:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EXCHANGE=oanda
SYMBOLS=XAU/USD,XAU/EUR
TIMEFRAMES=15m,1h,4h
```

Simpan dengan: `Ctrl+O`, Enter, `Ctrl+X`

## Menjalankan Bot

### 1. Test Bot (Demo)
```bash
source venv/bin/activate
python demo_gold.py
```

### 2. Jalankan Bot Sekali
```bash
source venv/bin/activate
python main.py
```

### 3. Jalankan di Background (RECOMMENDED)

#### Opsi A: Menggunakan nohup
```bash
source venv/bin/activate
nohup python main.py > bot.log 2>&1 &

# Lihat process ID
echo $!

# Cek bot berjalan
ps aux | grep main.py

# Lihat log
tail -f bot.log
tail -f reversal_bot.log
```

#### Opsi B: Menggunakan screen (RECOMMENDED)
```bash
# Install screen (jika belum)
sudo apt-get install screen

# Buat session baru
screen -S goldbot

# Aktivasi venv dan jalankan bot
source venv/bin/activate
python main.py

# Detach dari screen (bot tetap jalan)
# Tekan: Ctrl+A lalu D

# Attach kembali ke session
screen -r goldbot

# List semua screen sessions
screen -ls

# Kill session
screen -X -S goldbot quit
```

#### Opsi C: Menggunakan tmux
```bash
# Install tmux
sudo apt-get install tmux

# Buat session baru
tmux new -s goldbot

# Jalankan bot
source venv/bin/activate
python main.py

# Detach: Ctrl+B lalu D
# Attach: tmux attach -t goldbot
```

#### Opsi D: Systemd Service (PRODUCTION)
```bash
# Buat service file
sudo nano /etc/systemd/system/goldbot.service
```

Isi dengan:
```ini
[Unit]
Description=GOLD Reversal Pattern Detection Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/reversal_bot
Environment="PATH=/path/to/reversal_bot/venv/bin"
ExecStart=/path/to/reversal_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Jalankan service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable goldbot

# Start service
sudo systemctl start goldbot

# Check status
sudo systemctl status goldbot

# View logs
sudo journalctl -u goldbot -f

# Stop service
sudo systemctl stop goldbot

# Restart service
sudo systemctl restart goldbot
```

## Monitoring Bot

### 1. Cek Process Berjalan
```bash
ps aux | grep main.py
ps aux | grep python
```

### 2. Lihat Log Real-time
```bash
tail -f reversal_bot.log
tail -f bot.log
```

### 3. Lihat Log Terakhir
```bash
tail -n 100 reversal_bot.log
```

### 4. Monitor Resource Usage
```bash
# CPU dan Memory
top
htop  # install: sudo apt-get install htop

# Disk usage
df -h

# Network
netstat -tuln
```

## Maintenance

### Update Bot
```bash
cd reversal_bot
git pull origin master
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart bot
# Jika pakai screen:
screen -r goldbot
# Ctrl+C untuk stop, lalu python main.py

# Jika pakai systemd:
sudo systemctl restart goldbot
```

### Backup Configuration
```bash
# Backup .env file
cp .env .env.backup

# Backup ke local
scp username@vps_ip:/path/to/reversal_bot/.env ~/backup/
```

### Clean Logs
```bash
# Truncate log file
> reversal_bot.log
> bot.log

# Atau hapus log lama
find . -name "*.log" -mtime +7 -delete
```

## Troubleshooting

### Bot Tidak Jalan
```bash
# Cek error di log
tail -f reversal_bot.log

# Cek Python errors
python main.py  # jalankan manual untuk lihat error

# Cek dependencies
pip list
pip install -r requirements.txt
```

### Koneksi Telegram Gagal
```bash
# Test koneksi
curl https://api.telegram.org/botYOUR_TOKEN/getMe

# Cek firewall
sudo ufw status
sudo ufw allow 443/tcp
```

### Memory Habis
```bash
# Lihat memory usage
free -h

# Kill process
pkill -f main.py

# Restart dengan limit
ulimit -v 1000000  # limit 1GB
python main.py
```

### Bot Crash Terus
```bash
# Lihat system logs
sudo journalctl -xe

# Cek disk space
df -h

# Tambah swap jika RAM kurang
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Security Tips

### 1. Firewall
```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTPS (for Telegram)
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### 2. Protect .env File
```bash
chmod 600 .env
```

### 3. Update Regularly
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 4. Monitor Login Attempts
```bash
sudo tail -f /var/log/auth.log
```

## Auto-Restart on Crash

### Menggunakan cron + script
```bash
# Buat script checker
nano check_bot.sh
```

Isi:
```bash
#!/bin/bash
if ! pgrep -f "python main.py" > /dev/null
then
    cd /path/to/reversal_bot
    source venv/bin/activate
    nohup python main.py > bot.log 2>&1 &
fi
```

```bash
chmod +x check_bot.sh

# Tambah ke crontab (cek setiap 5 menit)
crontab -e

# Tambahkan:
*/5 * * * * /path/to/check_bot.sh
```

## Performance Tips

### 1. Reduce Scan Interval
Edit `.env`:
```bash
SCAN_INTERVAL=300  # 5 menit instead of 60 detik
```

### 2. Reduce Lookback Periods
```bash
LOOKBACK_PERIODS=50  # instead of 100
```

### 3. Monitor Specific Timeframes
```bash
TIMEFRAMES=1h,4h  # remove 15m
```

## Quick Commands Reference

```bash
# Start bot
screen -S goldbot
source venv/bin/activate && python main.py

# Check bot
screen -ls
ps aux | grep main.py

# View logs
tail -f reversal_bot.log

# Stop bot
screen -r goldbot  # then Ctrl+C
# or
pkill -f main.py

# Update bot
git pull && pip install -r requirements.txt --upgrade
```

## 🎉 Done!

Bot Anda sekarang berjalan 24/7 di VPS dan akan mengirim notifikasi Telegram setiap kali menemukan pola reversal pada GOLD!
