#!/bin/sh
isort bchdesktopwallet
isort setup.py
black bchdesktopwallet
black setup.py

