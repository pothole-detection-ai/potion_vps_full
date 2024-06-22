cd /root/potion_new
/usr/bin/pkill -f app.py
/usr/bin/nohup /usr/bin/python3 /root/potion_new/app.py &> /root/potion_new/logs/logfile.log &
