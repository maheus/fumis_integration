3.2.0

- add air pressure sensor
- add rpm sensor
- add stove status if stove is an hybrid stove
- add debug info

3.1.0
----

- add stove combustion chamber temperature

3.0.2
----

- add default value for config flow

3.0.1
----

- fix non async call async_forward_entry_setup

3.0.0
----

- rename stove state to stove status
- move stove state to binary sensor
- add stove current state sensor
- init using SensorEntity,BinarySensorEntity and SensorDeviceClass
# Breaking change
- fix bug unique ID

2.1.1
-----

- fix

2.1.0
-----

- add service set_power_stove (remove after refactor)
- remove main branch in HACS

2.0.3
-----

- fix hacs.json

2.0.2
-----
- prepare to use hacs
- fix codeowners

2.0.0
-----

- refactor
