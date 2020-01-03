dig $1 +short | while read line ; do iptables -A OUTPUT -d $line -j REJECT ; done

