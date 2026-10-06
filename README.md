# El Hareketiyle Silgi Tahtası

OpenCV ve MediaPipe ile geliştirilmiş, el hareketiyle çalışan bir "silgi tahtası". Ekran beyaz bir tahta ile başlar. İşaret parmağını kamera önünde hareket ettirdikçe tahta silinir ve altından kameradaki görüntün (ya da düz bir renk) görünür.

## Nasıl çalışır?

Projenin merkezinde tek kanallı bir **maske** var:

- Maske siyahsa o pikselde beyaz tahta görünür.
- Maske beyazsa o pikselde kamera görüntüsü (ya da seçilen düz renk) görünür.

Parmak ucu bulunduğunda maskeye çizim yapılır, her karede maske ile tahta birleştirilir. Yani ortada gerçek bir "silgi" yok: maskeye çizim yapılıyor ve sonuç silgi gibi görünüyor.

Parmak takibi için MediaPipe **HandLandmarker** kullanılıyor. Elin 21 noktasından işaret parmağı ucu (nokta 8) konum olarak alınıyor. Hızlı harekette çizgilerin kopmaması için her karedeki nokta, bir önceki noktayla `cv2.line` ile birleştiriliyor.

## Kontroller

| Girdi | Ne yapar? |
|---|---|
| Sadece işaret parmağı açık | Siler |
| Yumruk / başka el pozisyonu | Silmeyi durdurur |
| `c` | Tahtayı sıfırlar (tamamen beyaz) |
| `m` | Silinen alanda kamera ↔ siyah arasında geçiş yapar |
| `q` | Çıkış |

Jest tespiti şu mantığa dayanıyor: bir parmağın ucu, o parmağın orta ekleminden daha yukarıdaysa parmak açık sayılıyor. Başparmak jeste dahil değil.

## Kurulum

```bash
pip install opencv-python mediapipe numpy
```

## Çalıştırma

```bash
python main.py
```

## Bilinen sınırlamalar

- **El pozisyonuna duyarlı:** Parmağın açık olup olmadığı "uç, eklemden daha yukarıda mı" kontrolüyle belirleniyor. El yan yatarsa ya da ters dönerse jest tespiti yanlış sonuç verebilir.
- **Takip kopabilir:** Işık kötüyse ya da el çok hızlı hareket ediyorsa takip anlık olarak kaybolabilir ve çizgi kopar.
- **Başparmak yok:** Başparmak yan durduğu için aynı yöntemle tespit edilemiyor, jestte kullanılmıyor.
- **Renk modu toptan çalışıyor:** `m` ile mod değiştirildiğinde silinmiş tüm alan aynı anda değişir. Her çizgi kendi modunu saklamaz, çünkü maske hangi pikselin hangi modda açıldığını tutmuyor.
- **Tek el:** Yalnızca bir el takip ediliyor.
- **Titreme:** Parmak ucu noktasına yumuşatma uygulanmadığı için küçük sıçramalar çizgide görülebilir.

## Yol haritası

- Parmak ucu noktası için hareketli ortalama ile yumuşatma
- Gerçek kalem modu: maskenin yanında renkli bir çizim katmanı
- Daha sağlam parmak tespiti (bilekten uzaklık karşılaştırması)
