# Cloudflare & Backup Setup for Cyndro

## Cloudflare Integration
1. Sign up at https://cloudflare.com and add your domain.
2. Update your domain registrar's nameservers to Cloudflare's (shown in Cloudflare dashboard).
3. Enable SSL/TLS (Full/Strict), DDoS protection, and Web Application Firewall (WAF) in Cloudflare dashboard.
4. Set up page rules to always use HTTPS.

## Automated Backups (Linux Example)
- Add this cron job to back up your site files daily at 2am:

```
0 2 * * * tar -czf /backups/cyndro-$(date +\%F).tar.gz /var/www/cyndro
```
- For database backups, add a cron job for your DB engine (e.g., PostgreSQL, MySQL, SQLite).

## File Permissions
- Set web files to be owned by the web server user (e.g., www-data):
```
sudo chown -R www-data:www-data /var/www/cyndro
sudo chmod -R 750 /var/www/cyndro
```

## Remove Default Files
- Delete default index.html, test pages, and unused scripts from your web root and server config folders.

---

For more details, see the nginx_security_example.conf file and your cloud provider's documentation.