#!/usr/bin/bash

# ping_scan.sh - wykrywanie aktywnych hostów za pomocą ping

# skrypt obsługuje tylko sieci z maską 255.255.255.0
echo "Podaj pierwsze 3 oktety adresu IP (np. 192.168.1.):"
echo -n "> "

read net  # prefiks sieciowy

# skanowanie adresów IP od X.X.X.1 do X.X.X.254
for h in {1..254}; do  # h - część hosta
	ip="$net$h"  # adres IPv4

	# -c 2 -> wysłanie dwóch pakietów ICMP
	# -q -> quiet output
	# -W 1 -> czekanie 1 sekundę na odpowiedź
	# > /dev/null -> przekierowanie STDOUT do "niczego"
	if ping -c 2 -q -W 1 $ip > /dev/null; then
		# otrzymano odpowiedź
		echo "$ip działa!"  # host jest aktywny
	fi
done
