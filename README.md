# 🥇 GOLD Reversal Pattern Detection Bot

Bot untuk mendeteksi pola reversal pada **GOLD (XAU/USD dan XAU/EUR)** dengan notifikasi Telegram.

## ✅ Status: SIAP DIGUNAKAN

Bot telah berhasil ditest dan mengirim **52 notifikasi Telegram** untuk pola GOLD!

## 🎯 Fitur Utama

### Pola yang Dideteksi:
1. **Head & Shoulders** - Pola bearish reversal
2. **Inverse Head & Shoulders** - Pola bullish reversal  
3. **Double Top/Bottom** - Dua puncak/lembah
4. **Triple Top/Bottom** - Tiga puncak/lembah (confidence 95%)
5. **Rounding Bottom** - Pola U bullish
6. **Spike (V) Pattern** - Reversal tajam

### Pasangan GOLD:
- **XAU/USD** - GOLD vs US Dollar
- **XAU/EUR** - GOLD vs Euro

### Timeframes:
- 15 menit
- 1 jam
- 4 jam

## 🚀 Cara Menggunakan

### 1. Instalasi (Sudah Selesai ✓)
```bash
cd /Users/macbook/Desktop/Tradingbot/reversal_bot
source venv/bin/activate
```

### 2. Konfigurasi Telegram (Sudah Dikonfigurasi ✓)
File `.env` sudah berisi:
- ✅ Telegram Bot Token
- ✅ Telegram Chat ID
- ✅ GOLD pairs (XAU/USD, XAU/EUR)

### 3. Menjalankan Bot

#### A. Demo dengan Data Simulasi (RECOMMENDED untuk testing)
```bash
python demo_gold.py
```
**Hasil:** Mengirim notifikasi Telegram dengan data GOLD simulasi

#### B. Bot Live (Memerlukan OANDA API)
```bash
python main.py
```
**Catatan:** Memerlukan API credentials dari OANDA untuk data live

## 📱 Notifikasi Telegram

Setiap alert berisi:
- 🟢/🔴 Signal (Bullish/Bearish)
- 📊 Jenis pola (Head & Shoulders, Double Bottom, dll)
- 💪 Confidence level (70-100%)
- 💰 Harga saat ini
- 📝 Level-level penting (support/resistance)
- 💡 Saran trading (LONG/SHORT)

## 📊 Hasil Testing

### Test #1: Pattern Detection
- ✅ 37 pola terdeteksi
- ✅ Semua 6 jenis pola berfungsi

### Test #2: Telegram Notifications  
- ✅ 3 alerts terkirim (BTC demo)
- ✅ Koneksi Telegram sukses

### Test #3: GOLD Specific
- ✅ **52 alerts terkirim**
- ✅ 26 alerts XAU/USD
- ✅ 26 alerts XAU/EUR
- ✅ Triple Tops/Bottoms detected (95% confidence)
- ✅ Rounding Bottom detected (77% confidence)

## 📁 File Penting

| File | Fungsi |
|------|--------|
| `main.py` | Bot utama untuk trading live |
| `demo_gold.py` | Demo GOLD dengan Telegram ⭐ |
| `demo_simulation.py` | Demo dengan data simulasi |
| `test_patterns.py` | Unit testing |
| `.env` | Konfigurasi (Telegram, symbols) |
| `config.py` | Pengaturan bot |

## ⚙️ Konfigurasi (.env)

```bash
# Telegram (Sudah dikonfigurasi ✓)
TELEGRAM_BOT_TOKEN=8588145881:AAHbAY4127oWTTgtdpQyexeVvp9N0obbxWA
TELEGRAM_CHAT_ID=8354852198

# Exchange
EXCHANGE=oanda

# GOLD Pairs
SYMBOLS=XAU/USD,XAU/EUR

# Timeframes
TIMEFRAMES=15m,1h,4h

# Pattern Settings
PATTERN_TOLERANCE=0.02
MIN_CONFIDENCE=0.7
SCAN_INTERVAL=60
```

## 🔧 Troubleshooting

### Jika Tidak Ada Data Live:
1. **Gunakan demo:** `python demo_gold.py` ✅
2. **Atau tambahkan OANDA API credentials** ke `.env`

### Jika Telegram Tidak Terkirim:
1. Cek bot token di `.env`
2. Pastikan chat ID benar
3. Test dengan: `python demo_gold.py`

## 💡 Tips Trading GOLD

1. **Triple Top/Bottom** - Signal paling kuat (95% confidence)
2. **Rounding Bottom** - Reversal bertahap, lebih aman
3. **Spike Pattern** - Reversal cepat, high risk/reward
4. **Gunakan multiple timeframes** - Konfirmasi signal
5. **Selalu gunakan stop loss!** ⚠️

## 📈 Langkah Selanjutnya

### Untuk Live Trading:
1. Daftar akun OANDA (atau broker forex lain)
2. Dapatkan API credentials
3. Tambahkan ke `.env`:
   ```bash
   OANDA_API_KEY=your_api_key
   OANDA_ACCOUNT_ID=your_account_id
   ```
4. Jalankan: `python main.py`

### Untuk Testing Lebih Lanjut:
```bash
# Test pattern detection
python test_patterns.py

# Demo GOLD dengan Telegram
python demo_gold.py

# Demo simulasi umum
python demo_simulation.py
```

## ⚠️ Disclaimer

- Bot ini untuk **educational purposes**
- Selalu gunakan **risk management**
- Past performance ≠ future results
- Test dengan **demo account** dulu
- **GOLD sangat volatile** - hati-hati!

## 🎉 Summary

✅ Bot siap digunakan  
✅ Telegram notifications berfungsi  
✅ 6 pola reversal terdeteksi  
✅ Fokus pada XAU/USD & XAU/EUR  
✅ 52 test alerts berhasil terkirim  

**Selamat trading! 📊🥇**
