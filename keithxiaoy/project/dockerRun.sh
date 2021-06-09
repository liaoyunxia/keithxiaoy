#!/bin/bash

supervisord -c /root/Git/jk_p2p_app/etc/supervisord.conf
tail -f /dev/null
