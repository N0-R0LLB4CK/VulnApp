build: docker build -t vuln-server .

run: docker run -d --name server -p 80:80 -p 22:22 vuln-server

