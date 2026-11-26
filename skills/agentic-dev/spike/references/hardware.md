# A hardware spike

A simulator answers what the code does, not what the board does. Timing, power, radio, sensors and heat are answered on the real device.

* **Measure on the real device;** a simulator or emulator only rules things out.
* **Test more than one unit** when the question is about the design rather than one board: parts vary from board to board.
* **State the conditions:** board revision, unit serial numbers, firmware version, supply voltage, temperature and wiring. A result holds only for them.
* **Read the result back from the device,** over serial, a logic analyzer or a scope capture, and have the script parse it into pass or fail.
* **Repeat the measurement** and report the spread; one reading is not a result. Power-cycle between runs when the question is about startup.
* **Flash firmware freely.** Ask before writing fuses, option bytes or lock bits: they can lock the chip for good.
* **Ask before running a part outside its rated voltage, current or temperature.**
* **Ask the person for each step that needs hands,** such as wiring, a power cycle, a button press or moving the device. Say exactly what to do, and wait for them.
* **Timebox in bench sessions.**
