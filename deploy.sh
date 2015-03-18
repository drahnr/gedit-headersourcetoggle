#!/usr/bin/env bash


GEDIT_PLUGIN_DIR="$HOME/.local/share/gedit/plugins/"
mkdir -p "$GEDIT_PLUGIN_DIR"
cp -vf ./headersourcetoggle.plugin "$GEDIT_PLUGIN_DIR"
cp -vf ./headersourcetoggle.py "$GEDIT_PLUGIN_DIR"
