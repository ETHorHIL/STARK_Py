# Fibonacci_STARK
A "for fun" STARK for a Fibonacci sequence based on Vitaliks MIMC STARK. Obviously this code is not to be used for anything serious.

I took Vitaliks implementation described [here](https://vitalik.ca/general/2018/07/21/starks_part_3.html), and changed it from
proving computation of a VDF to just proving the computational trace of a Fibonacci number. There is no easy compilation into a R1CS like in Pinocchio so you have to dig into the guts to achieve that change.
You can just open the test.py file and change the Fibonacci number to compute in test_stark().

# Performance
![Image description](https://github.com/ETHorHIL/Fibonacci_STARK/blob/cleaning_up/prover_time.PNG)

![Image description](https://github.com/ETHorHIL/Fibonacci_STARK/blob/cleaning_up/verifier_time.PNG)

![Image description](https://github.com/ETHorHIL/Fibonacci_STARK/blob/cleaning_up/computation.PNG)
