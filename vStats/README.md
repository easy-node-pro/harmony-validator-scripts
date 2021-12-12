# vStats alerts
Here's how the alerting works.

### Get a token
Send the command `/easynodetoken` to the @vStats Bot on telegram to get your token.

### Download the alert.py script
We suggest storing it in your home folder.

```
cd ~/
wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/vStats/alert.py
```

### Setup token
If you use validatortoolbox you can edit your ~/.easynode.env file to contain the following, replace `token` with your token:
- `VSTATS_BOT='token'`

If you do not use validatortoolbox edit your token into line 20 in place of `token`:
- `VSTATS_BOT='token'`

### Setup cron job
We've included an example cron file for you to download and customize:

```
wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/vStats/validator-alert
```

Update your username and path to the alert.py file. Then as root copy this file into `/etc/cron.d` to start checking every minute.