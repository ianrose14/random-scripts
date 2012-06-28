#!/usr/bin/env python

"""This module simply defines a number of constant values, as specified in the
802.11 standard."""

# Frame types
WIFI_TYPE_MGMT=0
WIFI_TYPE_CTRL=1
WIFI_TYPE_DATA=2

# Management subtypes
WIFI_SUBTYPE_ASSOC_REQ = 0
WIFI_SUBTYPE_ASSOC_RESP = 1
WIFI_SUBTYPE_REASSOC_REQ = 2
WIFI_SUBTYPE_REASSOC_RESP = 3
WIFI_SUBTYPE_PROBE_REQ = 4
WIFI_SUBTYPE_PROBE_RESP = 5
WIFI_SUBTYPE_BEACON = 8
WIFI_SUBTYPE_ATIM = 9
WIFI_SUBTYPE_DISASSOC = 10
WIFI_SUBTYPE_AUTH = 11
WIFI_SUBTYPE_DEAUTH = 12

# Control subtypes
WIFI_SUBTYPE_PS_POLL = 10
WIFI_SUBTYPE_RTS = 11
WIFI_SUBTYPE_CTS = 12
WIFI_SUBTYPE_ACK = 13
WIFI_SUBTYPE_CF_END = 14
WIFI_SUBTYPE_CF_END_CF_ACK = 15

# Data subtype bitmasks
WIFI_SUBTYPE_DATA_MASK = 0
WIFI_SUBTYPE_CF_ACK_MASK = 1
WIFI_SUBTYPE_CF_POLL_MASK = 2
WIFI_SUBTYPE_NULL_MASK = 4

# Beacon frame "information elements"
WIFI_INFOELT_SSID=0
WIFI_INFOELT_RATES=1
WIFI_INFOELT_FHSET=2
WIFI_INFOELT_DSSET=3
WIFI_INFOELT_CFSET=4
WIFI_INFOELT_TIM=5  # traffic indication map
WIFI_INFOELT_IBSSSET=6
WIFI_INFOELT_COUNTRY=7
WIFI_INFOELT_HOPPING_PATTERN_PARAMS=8
WIFI_INFOELT_HOPPING_PATTERN_TABLE=9
WIFI_INFOELT_CHALLENGE=16
WIFI_INFOELT_ERPINFO=42  # "ERP information" (802.11g)
WIFI_INFOELT_QOS_CAPABILITY=46   # QoS capability
WIFI_INFOELT_RSNINFO=48  # "Robust Security Network" (802.11i)
WIFI_INFOELT_ESRATES=50  # "Extended Supported Rates" (802.11g)
WIFI_INFOELT_VENDOR=221  # or "Wi-Fi Protected Access"