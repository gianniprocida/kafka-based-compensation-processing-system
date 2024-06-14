#!/bin/bash

sleep 30;


uvicorn main:app --host 0.0.0.0 --port 8088;