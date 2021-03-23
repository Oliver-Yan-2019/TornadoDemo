#!/usr/bin/env bash
if [ "$MODE" = "snowflake" ];
then
  echo "in snowflake"
  snowflake_start_server

else
  python application.py
fi