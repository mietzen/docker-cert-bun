# Docker Certbun

Slightly modernized and dockerized version of: https://github.com/porkbundomains/certbun

# Usage (e.g. with nginx):

```yaml
version: "3"
services:
  certbun:
    build: "mietzen/porkbun-certbun:latest"
    container_name: certbun
    environment:
      DOMAIN: "domain.com" # Your Porkbun domain
      SECRETAPIKEY: "<YOUR-SECRETAPIKEY>" # Your Porkbun Secret-API-Key
      APIKEY: "<YOUR-APIKEY>" # Your Porkbun API-Key
      SLEEP: 24 # In Hours 
    volumes:
      - ssl:/etc/ssl
    restart: unless-stopped

  nginx:
    image: nginx:1-slim
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl.conf:/etc/nginx/ssl.conf:ro
      - ./nginx/proxy.conf:/etc/nginx/proxy.conf:ro
      - ./nginx/dhparams.pem:/etc/nginx/dhparams.pem:ro
      - ssl:/etc/ssl
    command: "/bin/sh -c 'while :; do sleep 12h & wait $${!}; nginx -s reload; echo 'reloading config'; done & nginx -g \"daemon off;\"'"
    restart: unless-stopped
    networks:
      - nginx

volumes:
  ssl:

networks:
  nginx:
    external: true

```
