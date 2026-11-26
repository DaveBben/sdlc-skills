# A hardware or real-device spike

A simulator answers what the code does, not what the device does. Timing, power, radio, sensors, heat and what the OS allows in the background are answered on the real device.

* **Measure on the real device;** a simulator or emulator only rules things out.
* **Test more than one unit** when the question is about the design rather than one device: parts vary from board to board, and phones from maker to maker and OS version to OS version.
* **State the conditions:** for a board, its revision, unit serial numbers, firmware version, supply voltage, temperature and wiring; for a phone or console, its model, OS version and power-saving state. A result holds only for them.
* **Read the result back from the device,** over serial, a logic analyzer, a scope capture or the device's log, and have the script parse it into pass or fail.
* **Measure power and timing on the release build with the debug probe detached:** an attached probe keeps the chip out of deep sleep and changes timing. State the instrument and its resolution and sample rate; a USB meter cannot read µA sleep current.
* **Power-cycle between runs** when the question is about startup.
* **Flash firmware freely.** Ask before writing fuses, option bytes or lock bits: they can lock the chip for good.
* **Ask before running a part outside its rated voltage, current or temperature.**
* **Ask the person for each step that needs hands,** such as wiring, a power cycle, a button press or moving the device. Say exactly what to do, and wait for them.
* **Timebox in bench sessions.**
