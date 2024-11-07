# How to configure

## WiFi hotspot

Copy and paste the file `10-wifi-hotspot.yaml` to `/etc/netplan/` and run the following command:

```bash
sudo netplan generate
sudo netplan apply
```

## Connect Raspberry Pi your WiFi network

Modified the file `/etc/netplan/50-cloud-init.yaml` (on RPi) following the template of `50-cloud-init.yaml`

## Set up device tree overlay

Copy and paste the file `config.txt` to `/boot/` and run the following command:

```bash
sudo reboot
```