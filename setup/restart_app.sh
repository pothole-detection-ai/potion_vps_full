cd /home/detectionpotholes
/usr/bin/pkill -f app.py
/usr/bin/nohup /usr/bin/python3 /home/detectionpotholes/app.py &> /home/detectionpotholes/logs/logfile.log &
