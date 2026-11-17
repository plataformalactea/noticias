#!/bin/sh
cat > $PIL_FUENTE/deploy/test/last_mail.txt
echo "$@" > $PIL_FUENTE/deploy/test/args.txt
