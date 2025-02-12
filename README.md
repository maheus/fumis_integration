[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![hacs_badge](https://github.com/maheus/fumis_integration/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/maheus/fumis_integration/actions/)
# Fumis integration for Home Assistant

This is a _custom component_ for [Home Assistant](https://www.home-assistant.io/).

This integration using a modified lib [python-fumis](https://github.com/frenck/python-fumis).

The Fumis integration allows you to control and get stoves informations who use the api fumis (https://api.fumis.si).

### HACS

HACS > Custom repositories
HACS > Integrations > Explore & Add Repositories > Fumis > Install this repository

### Manually

Copy `custom_components/fumis` in `config/custom_components` of your Home Assistant and restart HA.

## Configuration

Adding integration with HA ui (configuration -> integrations -> add integration -> search fumis).

## known problems

For one HETA green 200, if you deactivate the ecomode, then you must activate the possibility of accessing this menu.
For reactivate that:
```
curl -d '{"unit": {"id": "YOUR_MAC", "type": 0, "pin": "YOUR_PASSWORD"},"controller": {"diagnostic": {"parameters": [{"id": 53, "value": 1}]}} ,"apiVersion": "1"}' -H  "Accept: application/json" -H 'appname: mtest' -H 'User-Agent: mtest' -H 'username: YOUR_MAC' -H 'password: YOUR_PASSWORD'  -X POST 'https://api.fumis.si/v1/status/'
```

## Contributors

For a full list of all authors and contributors,
check [the contributor's page](https://github.com/maheus/fumis_integration/graphs/contributors).

### Thanks to:
[@Aohzan](https://github.com/Aohzan): for your help and disponibility

## Licence
MIT License

Copyright (c) [2022] [Mlehoux]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
