#! /bin/bash

t whois -C never -c $1 | tail -n +2 | head -n 1 | cut -d, -f1
