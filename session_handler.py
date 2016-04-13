#!/usr/bin/env python
#
# l2s - logins to slack
#

import json
import os
import sys
import syslog
import urllib
import ConfigParser

SUPPORTED = ("pam_script_ses_open", "pam_script_ses_close")

def handler(func):
    def validator(*args, **kwargs):
        for var in ["PAM_USER", "PAM_SERVICE"]:
            if var not in os.environ:
                return

        try:
            ignore_users = args[0].get("l2s", "ignore_users").split(",")
            if os.environ["PAM_USER"] in ignore_users:
                return
            if os.environ.get("PAM_RUSER"):
                if os.environ["PAM_RUSER"] in ignore_users:
                    return
        except:
            pass

        try:
            valid_services = args[0].get("l2s", "services").split(",")
            if os.environ["PAM_SERVICE"] not in valid_services:
                return
        except:
            pass

        return func(*args, **kwargs)

    return validator

@handler
def pam_script_ses_open(config):
    text = "%s: Session started for user %s" % (os.environ["PAM_SERVICE"], os.environ["PAM_USER"])
    send(origin(text), config)

@handler
def pam_script_ses_close(config):
    text = "%s: Session closed for user %s" % (os.environ["PAM_SERVICE"], os.environ["PAM_USER"])
    send(origin(text), config)

def origin(text):
    if os.environ.get("PAM_RHOST"):
        return ("%s (from %s)" % (text, os.environ["PAM_RHOST"]))
    elif os.environ.get("PAM_RUSER"):
        return ("%s (by user %s)" % (text, os.environ["PAM_RUSER"]))
    else:
        return text

def get_config():
    parser = ConfigParser.SafeConfigParser()

    # Look for l2s.conf in /etc and . relative to the script
    for d in ["/etc", os.path.abspath(os.path.dirname(__file__))]:
        f = os.path.join(d, "l2s.conf")
        if os.path.exists(f):
            parser.read(f)
            return parser

    syslog.syslog(syslog.LOG_ERR, "Unable to find l2s.conf")
    sys.exit()

def send(text, config):
    text = "%s: %s" % (config.get("l2s", "host"), text)
    payload = {
        "username": config.get("l2s", "botname"),
        "icon_emoji": config.get("l2s", "icon"),
        "text": text,
    }

    # Fork so we don't block on the HTTP request
    pid = os.fork()
    if pid != 0:
        sys.exit()

    payload = urllib.urlencode({"payload": json.dumps(payload)})
    urllib.urlopen(config.get("l2s", "url"), payload)

# Call on supported handlers based on our filename
if __name__ == "__main__":
    if os.path.basename(__file__) in SUPPORTED:
        locals()[os.path.basename(__file__)](get_config())
