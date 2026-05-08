from math import gcd
from fractions import Fraction
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram

# ===========================
# Parameters (Matching Manuscript §3.3)
# ===========================
TOTAL_QUBITS = 9
N_COUNT = 5   # counting register
N_WORK = 4    # work register
SHOTS = 2048

# ===========================
# Quantum modular exponentiation (N = 15 only)
#
# Per manuscript §3.2 (revised): the hardcoded function c_amod15(i, power)
# performs the operation  |y> -> |y * i^power mod 15>
# for the limited set of valid bases i in {2, 7, 8, 11, 13}.
# 'power' is the exponent, specifically 2^j where j is the index of the
# control qubit in the counting register.
# ===========================
def c_amod15(i, power):
    """Controlled-U gate that performs |y> -> |y * i^power mod 15> on a 4-qubit register."""
    if i not in [2, 7, 8, 11, 13]:
        raise ValueError("This base 'i' is not supported by the hardcoded N=15 circuit.")

    U = QuantumCircuit(4)
    for _ in range(power):
        if i in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if i in [7, 8]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if i == 11:
            U.swap(1, 3)
            U.swap(0, 2)
        if i in [7, 11, 13]:
            for q in range(4):
                U.x(q)

    gate = U.to_gate()
    gate.name = f"c_mult({i}^{power}%15)"
    return gate.control()

# ===========================
# Main Program
# ===========================
def run_shors():
    """Main function to run the algorithm."""
    print("--- Shor's Algorithm Simulator (9 qubits) ---")

    # Hardcoded values for the N=15 simulation
    N = 15
    i = 7
    print(f"Factoring N={N} using base i={i} with {SHOTS} shots.")

    g = gcd(i, N)
    if g > 1:
        print(f"SUCCESS (Classical Luck): Factors are {g} and {N//g}.")
        return

    # --- Build the Quantum Circuit ---
    print("\nBuilding quantum circuit...")
    qc = QuantumCircuit(TOTAL_QUBITS, N_COUNT)

    # Step 1: Hadamards on counting register
    qc.h(range(N_COUNT))

    # Step 2: Initialize work register to |1>  (i^0 = 1)
    qc.x(N_COUNT)

    # Step 3: Controlled modular exponentiation -- U^(2^j) for j = control qubit index
    work_qubits = list(range(N_COUNT, N_COUNT + N_WORK))
    for q in range(N_COUNT):
        gate = c_amod15(i, 2**q)
        qc.append(gate, [q] + work_qubits)

    # Step 4: Inverse QFT
    qc.append(QFT(num_qubits=N_COUNT, inverse=True, do_swaps=True), range(N_COUNT))

    # Step 5: Measurement
    qc.measure(range(N_COUNT), range(N_COUNT))

    circuit_file = f"shor_circuit_N{N}_i{i}.png"
    qc.draw("mpl", filename=circuit_file, style={"fontsize": 10})
    print(f"Circuit diagram saved as {circuit_file}")

    # --- Simulation ---
    print("Circuit built. Simulating on AerSimulator...")
    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=SHOTS).result()
    counts = result.get_counts()
    print("Simulation complete.")

    # --- Plot histogram (Raw Counts)
    print("Generating plots...")
    plot_histogram(
        counts,
        figsize=(12, 6),
        title=f"Shor's Algorithm Results (N={N}, i={i})",
        bar_labels=True
    )
    plt.xlabel("Measurement outcome (binary)")
    plt.ylabel("Counts")
    plt.xticks(rotation=90)
    plt.tight_layout()
    filename1 = f"shor_histogram_N{N}_i{i}.png"
    plt.savefig(filename1)
    print(f"Histogram saved as {filename1}")

    # --- Plot probability distribution (Normalized)
    sorted_counts = dict(sorted(counts.items(), key=lambda kv: int(kv[0], 2)))
    probs = {k: v/SHOTS for k, v in sorted_counts.items()}
    plt.figure(figsize=(12, 6))
    plt.bar(probs.keys(), probs.values())
    plt.xlabel("Measurement outcome (binary)")
    plt.ylabel("Probability")
    plt.title(f"Probability Distribution (N={N}, i={i})")
    plt.xticks(rotation=90)
    plt.tight_layout()
    filename2 = f"shor_probabilities_N{N}_i{i}.png"
    plt.savefig(filename2)
    print(f"Probability plot saved as {filename2}")

    # --- Classical Post-processing ---
    print(f"\nMeasurement results: {counts}")
    non_zero_counts = {k: v for k, v in counts.items() if int(k, 2) != 0}
    if not non_zero_counts:
        print("Only measured 0. No phase information found.")
        return

    bitstr = max(non_zero_counts, key=non_zero_counts.get)
    k = int(bitstr, 2)

    print(f"\nMost frequent non-zero measurement: {bitstr} (decimal {k})")
    print(f"Phase = {k} / {2**N_COUNT} = {k / (2**N_COUNT)}")

    # Continued fraction to find period p
    frac = Fraction(k, 2**N_COUNT).limit_denominator(N)
    p = frac.denominator
    print(f"Estimated period p = {p}")

    if p % 2 != 0:
        print("Failed: Period p is odd.")
        return

    # Calculate factors:  gcd(i^(p/2) +/- 1, N)
    fac1 = gcd(pow(i, p//2, N) - 1, N)
    fac2 = gcd(pow(i, p//2, N) + 1, N)

    if 1 < fac1 < N or 1 < fac2 < N:
        factors = [f for f in (fac1, fac2) if 1 < f < N]
        if len(factors) == 1:
            factors.append(N // factors[0])
        print(f"\n!!! SUCCESS: Factors of {N} are {factors[0]} and {factors[1]} !!!")
    else:
        print("Failed to find non-trivial factors.")

# ===========================
# Entry point
# ===========================
if __name__ == "__main__":
    run_shors()
