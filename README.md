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

* Python 3.11+
* pipx
* git
* hatch

## Install

```
pipx install git+https://github.com/heathdbrown/roku
```

## Usage

```
roku device <IP>

roku apps <IP>
```

## Development / Quick Usage

- Install 'hatch' if not already installed

```bash
pipx install hatch
```

- Git clone

```bash
git clone https://github.com/heathdbrown/roku.git
cd roku
hatch shell
```

### Day 2 Development

```bash
cd roku
hatch shell
```

## Contribute

See [the contribute file](contribute.md)!

PRs accepted.
