RED TEAM:

BEGINNING:
DDOS the website

AFTER BLOCK:
Connect with vpn and continue the attack
SQL INJECTION: uname ADMIN passwd ' OR '1'='1

Click on the recovery page where it gives you the email

On dashboard there's an upload field -> upload rockyou.txt to break md5 hash

After getting the email:
Phissing email -> access to emails

IN EMAILS:
Sysadmin has sent an email regarding on where to find his password in case of emergencies
In drafts there's an email saying that the email password == ssh password

AFTER ACCESS:
Find root password location
Run sudo apt update && sudo apt install hashcat -y
Upload rockyou.txt from the website
Dictionary attack on the md5 hash after installing hashcat
Use: echo "84d961568a65073a3bcf0eb216b2a576" > test && hashcat -m 0 -a 0 test /app/uploads/rockyou.txt

AFTER PRIV ESC:
Drop the db and leave a "You got pwned message on the website"

BLUE TEAM:

BEGINNING:
Build and enable the firewall

AFTER:
Monitor network activity to find the attacker's IP

AFTER PWN:
Block his IP, change passwords, system cleanup, recover website and send the report to the developers to patch up the vulnerabilities