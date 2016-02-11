#!/bin/bash

mkdir -p /tmp/pkg/etc
mkdir -p /tmp/pkg/usr/share/libpam-script

cp l2s.conf /tmp/pkg/etc

cp session_handler.py /tmp/pkg/usr/share/libpam-script/pam_script_acct
cp session_handler.py /tmp/pkg/usr/share/libpam-script/pam_script_ses_close
cp session_handler.py /tmp/pkg/usr/share/libpam-script/pam_script_ses_open
cp session_handler.py /tmp/pkg/usr/share/libpam-script/pam_script_passwd

fpm \
    -s dir \
    -t deb \
    -C /tmp/pkg \
    --name l2s \
    --description 'L2S - Logins to Slack' \
    --vendor 'Ragnar B. Johannsson' \
    --license 'BSD' \
    --url 'http://github.com/ragnar-johannsson/l2s' \
    --maintainer 'ragnar@igo.is' \
    --version '0.1' \
    --depends 'libpam-script' \
    --depends 'python'

rm -rf /tmp/pkg
