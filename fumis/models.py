"""Models for the Fumis WiRCU."""

import attr

from .const import STATE_MAPPING, STATE_UNKNOWN, STATUS_MAPPING, STATUS_UNKNOWN, STOVE_ID, ECO_MAPPING


@attr.s(auto_attribs=True, frozen=True)
class Info:
    """Object holding information and states of the Fumis WiRCU device."""

    unit_id: str

    unit_version: str
    controller_version: str

    ip: str
    rssi: int
    signal_strength: int

    state: str
    state_id: int
    status: str
    status_id: int

    temperature: float
    target_temperature: float

    heating_time: int
    igniter_starts: int
    misfires: int
    overheatings: int
    uptime: int
    fuel_quality: int
    fuel_quantity: int
    ecomode_type: int
    ecomode_state: int
    timers: list
    kw: float
    actualpower: float
    setpower: int


    @staticmethod
    def from_dict(data: dict):
        """Return device object from Fumis WiRCU device response."""
        controller = data.get("controller", {})
        unit = data.get("unit", {})

        stats = controller.get("statistic", {})
        temperatures = controller.get("temperatures", {})
        power = controller.get("power", {})
        #temperature = temperatures[0] if temperatures else {}
        temperature = [d for d in temperatures if d['id'] == STOVE_ID][0]
        fuels = controller.get("fuels", [])
        fuel = [d for d in fuels if d['id'] == STOVE_ID][0]
        ecoMode = controller.get("ecoMode", {})
        timers = controller.get("timers", [])

        rssi = int(unit.get("rssi", -100))
        if rssi <= -100:
            signal_strength = 0
        elif rssi >= -50:
            signal_strength = 100
        else:
            signal_strength = 2 * (rssi + 100)

        status_id = controller.get("status", -1)
        status = STATUS_MAPPING.get(status_id, STATUS_UNKNOWN)

        state_id = controller.get("command", -1)
        state = STATE_MAPPING.get(state_id, STATE_UNKNOWN)

        ecomode_id = ecoMode.get("ecoModeEnable", -1)
        ecomode_state = ECO_MAPPING.get(ecomode_id, STATE_UNKNOWN)

        return Info(
            controller_version=controller.get("version", "Unknown"),
            heating_time=int(stats.get("heatingTime", 0)),
            igniter_starts=stats.get("igniterStarts", 0),
            ip=unit.get("ip", "Unknown"),
            misfires=stats.get("misfires", 0),
            overheatings=stats.get("overheatings", 0),
            rssi=rssi,
            signal_strength=signal_strength,
            state_id=state_id,
            state=state,
            status_id=status_id,
            status=status,
            actualpower=float(power.get("actualPower", 0)),
            kw=float(power.get("kw", 0)),
            setpower=int(power.get("setPower", 0)),
            target_temperature=temperature.get("set", 0),
            temperature=temperature.get("actual", 0),
            unit_id=unit.get("id", "Unknown"),
            unit_version=unit.get("version", "Unknown"),
            uptime=int(stats.get("uptime", 0)),
            fuel_quality=int(fuel.get("quality", "Unknown")),
            fuel_quantity=(float(fuel.get("quantity", "Unknown")) * 100),
            ecomode_type=int(ecoMode.get("ecoModeSetType", "Unknown")),
            ecomode_state=ecomode_state,
            timers=timers,
        )
