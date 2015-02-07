#!/bin/bash
CDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PYTHONPATH=$CDIR python "${CDIR}/scripts/spider_server"
