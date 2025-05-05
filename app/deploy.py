"""
1.
ssh-keygen


2.
cat .ssh/id_rsa.pub

3.

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

4.

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www3/ekzamen_1
ExecStart=/var/www3/ekzamen_1/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target



5.


server {
    listen 80;
    server_name 164.90.226.46;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
       root /var/www/ekzamen_1;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
"""








"""

# Git Pull Qo'lda Bajarish (Deploy uchun)
# Agar siz serverda git pull ni qo'lda bajarishni hohlasangiz, quyidagi qadamlarga amal qiling:
# 
# 1. Serverga ulanish va loyiha papkasiga o'tish
# bash
# 
# 
# ssh your_username@server_ip
# cd /var/www/ekzamen_1
# 
# 
# 2. Git holatini tekshirish
# bash
# git status
# git fetch origin
# 3. O'zgarishlarni qo'lda tortib olish
# bash
# 
# 
# git pull origin main  # yoki branch nomi (master, develop, etc.)
# Agar lokal o'zgarishlar bo'lsa:
# 
# bash
# 
# git stash        # O'zgarishlarni saqlab qo'yish
# git pull origin main
# git stash pop    # O'zgarishlarni qaytarish
# 
# 4. Virtual muhitni faollashtirish
# bash
# 
# source venv/bin/activate
# 
# 5. Yangi paketlarni o'rnatish
# bash
# pip install -r requirements.txt
# 
# 6. Migratsiyalarni bajarish
# bash
# 
# python manage.py migrate
# 7. Static fayllarni yig'ish
# bash
# 
# python manage.py collectstatic --noinput
# 
# 8. Serverlarni qayta ishga tushirish
# bash
# 
# sudo systemctl restart gunicorn
# sudo systemctl restart nginx
# 
# 9. Loglarni tekshirish
# bash
# 
# sudo journalctl -u gunicorn -f
# sudo tail -f /var/log/nginx/error.log

"""