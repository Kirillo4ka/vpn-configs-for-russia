# EaveVPN Configs
        
Последнее обновление системы: `2026-04-18 18:28:25` (MSK)  
Всего конфигураций в базе: `590`  
Всего QR-кодов сгенерировано: `7`

---

## 📖 Введение и Терминология

Добро пожаловать в репозиторий автоматизированной сборки VPN-конфигураций EaveVPN. Данный проект создан для обеспечения свободного доступа к информации и защиты личных данных. Все конфигурации проходят автоматическое тестирование скорости и доступности перед публикацией. Обновление происходит каждые 6 часов.

Крайне важно понимать разницу между типами предоставляемых подписок, чтобы выбрать подходящий вариант для ваших нужд.

### Что такое Black List (Черный список)?

**Black List** — это режим работы VPN, при котором **весь интернет-трафик** вашего устройства направляется через удаленный сервер.

* **Назначение:** Полная анонимизация, защита в публичных Wi-Fi сетях, доступ к ресурсам, заблокированным по географическому признаку.
* **В России:** Работает как "классический" VPN. Скрывает ваш реальный IP от всех сайтов.

### Что такое White List (Белый список / Обход блокировок)?

**White List** — это специализированный режим, созданный специально для пользователей из России. В этом режиме через VPN направляется **только трафик к заблокированным ресурсам**.

* **Назначение:** **Обход блокировок Роскомнадзора** (Instagram, Facebook, Twitter, зарубежные СМИ и т.д.) без потери скорости на российских сайтах.
* **Как это работает:** Скрипт использует современный протокол (например, VLESS Reality), который маскирует VPN-трафик под обычное посещение разрешенного сайта.
* **Преимущество:** Российские сайты (VK, Mail.ru, банки, Госуслуги) открываются напрямую на максимальной скорости.

---

## 🗂 Актуальные подписки

| Имя файла | Тип | Платформа | Протоколы | Серверов | Скачать TXT | QR-код |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **BLACK_SS+All_RUS.txt** | Black List | Full | `Hysteria, Shadowsocks, Trojan, VMESS` | `105` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/BLACK_SS+All_RUS.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/BLACK_SS+All_RUS-QR.png) |
| **BLACK_VLESS_RUS.txt** | Black List | Mobile/Full | `VLESS` | `218` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/BLACK_VLESS_RUS.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/BLACK_VLESS_RUS-QR.png) |
| **BLACK_VLESS_RUS_mobile.txt** | Black List | Mobile | `Hysteria, Shadowsocks, Trojan, VLESS, VMESS` | `150` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/BLACK_VLESS_RUS_mobile.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/BLACK_VLESS_RUS_mobile-QR.png) |
| **Vless-Reality-White-Lists-Rus-Mobile.txt** | White List | Mobile | `Shadowsocks, Trojan, VLESS` | `44` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/Vless-Reality-White-Lists-Rus-Mobile-QR.png) |
| **WHITE-CIDR-RU-all.txt** | White List | Full | `Shadowsocks, Trojan, VLESS` | `44` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/WHITE-CIDR-RU-all.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/WHITE-CIDR-RU-all-QR.png) |
| **WHITE-CIDR-RU-checked.txt** | White List | Mobile/Full | `VLESS` | `19` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/WHITE-CIDR-RU-checked.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/WHITE-CIDR-RU-checked-QR.png) |
| **WHITE-SNI-RU-all.txt** | White List | Full | `Hysteria, VLESS` | `10` | [📥 TXT](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/WHITE-SNI-RU-all.txt) | [🔲 QR](https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/qr-codes/WHITE-SNI-RU-all-QR.png) |


---

### 📋 Важные замечания

* Конфигурации бесплатны и предоставляются "как есть".
* Обновляйте подписку в приложении каждые 3-4 часа.
* Формат: **TXT** (совместим с V2RayTun, Happ, Streisand, Hiddify, NekoBox и др.)
* **QR-коды**: для каждого файла конфигурации создан отдельный QR-код в папке `qr-codes/`
* Для быстрой настройки: отсканируйте QR-код камерой или приложением.

*Automated by [Kirillo4ka](https://github.com/Kirillo4ka)*  
*Telegram: [@EaveVPN](https://t.me/EaveVPN)*
