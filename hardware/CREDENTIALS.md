# Hardware credential provisioning

The firmware does not contain real Wi-Fi credentials. Before flashing either device, copy the relevant example header to a local `credentials.h` file and replace the placeholder values.

```bash
cp hardware/rover/credentials.example.h hardware/rover/credentials.h
cp hardware/esp32cam/credentials.example.h hardware/esp32cam/credentials.h
```

The local `credentials.h` files are ignored by Git. Never commit them, paste their values into source code, or include them in issue reports. The rover header defines `AROHAN_AP_SSID`, `AROHAN_AP_PASS`, `AROHAN_STA_SSID`, and `AROHAN_STA_PASS`. The ESP32-CAM header defines `AROHAN_WIFI_SSID` and `AROHAN_WIFI_PASSWORD`.

Because a previous revision exposed Wi-Fi values, those credentials must be rotated before any device is connected to a real network. Removing literals from the current source does not revoke credentials that may already have been copied from Git history.

The default source values intentionally leave station credentials empty. This allows the firmware to compile for documentation and static checks while preventing an unconfigured checkout from silently joining a network.

