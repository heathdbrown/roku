# Roku_cli.py

> Python script for messing with the roku from the cli


## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contribute](#contribute)
- [License](#license)


## Background

NMAP and TCPDUMP showed interesting traffic at my house. I noticed an IP responding to a weird port. It was my roku.

I search the web for the open port and found https://sdkdocs.roku.com/display/sdkdoc/External+Control+API#ExternalControlAPI-GeneralECPcommands

This is what followed...

## Prerequisites

* Python 2.7+
* pip
* git

## Install

```
git clone <>
cd <>
pip install -r requirements.txt
```

## Usage

```
roku_cli.py ! find the roku

roku_cli.py <roku IP> --channels
```

| Options | Usage |
|---------|-------|
| none    | Attempt to find the roku by sedning multicast M-SEARCH |
| --channels | List out the channels|
| --active-channel | Grab the active channel on the roku |
|

## Contribute

See [the contribute file](contribute.md)!

PRs accepted.
