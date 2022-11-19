These commands configure `ufw` firewall on Ubuntu 20.04LTS, use at your own risk:

Configure the needed ports:
```bash
sudo ufw allow 22
sudo ufw allow 6000/tcp
sudo ufw allow 9000/tcp
```

Enable `ufw`:
```bash
sudo ufw enable
```

`ufw` Status:
```bash
sudo ufw status
```