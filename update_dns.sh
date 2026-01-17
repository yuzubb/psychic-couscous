#!/bin/bash
DOMAIN="mashumaro.duckdns.org"
TOKEN="5386118d-85d9-4a5d-a32a-5463362bad71
"

# Duck DNSを更新するコマンド
curl -s "https://www.duckdns.org/update?domains=${DOMAIN}&token=${TOKEN}&ip="
echo "\nUpdated at $(date)"
