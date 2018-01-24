#!/bin/bash
nohup python3 pricegrabber.py >grabber.log &
nohup python3 dashboard.py >dashboard.log &
