#!/bin/sh
tar cvf ../APP.tar ../View/*.pyc ../inp/;
md5sum ../APP.tar >/tmp/cfg
