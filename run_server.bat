@echo off
pushd %~dp0
SET PYTHONPATH=%CD%
python scripts/spider_server
popd
