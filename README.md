# Shor's Algorithm Simulation on MAHTI

This repository contains the Python source code for the simulation of Shor's quantum factoring algorithm, as detailed in the research article [my article will be pasted here]. The code is built using the Qiskit framework and was developed to factor the integer N=15 as a proof-of-concept for establishing a quantum simulation environment on the Finnish CSC's MAHTI supercomputer.

This implementation served as the cornerstone for a pilot project at Jamk University of Applied Sciences to validate a reusable high-performance computing (HPC) workflow for quantum simulations.

## Key Features

-   A full implementation of Shor's algorithm for factoring N=15.
-   A 9-qubit quantum circuit (5 counting qubits, 4 work qubits).
-   Built with the Qiskit framework, utilizing the high-performance `AerSimulator`.
-   Generates a histogram of measurement outcomes to visualize the results.
-   Includes classical post-processing to derive the factors from the simulation results.

## Requirements

The simulation was validated with the following software versions:
*   Python 3.10
*   Qiskit 1.1.1
*   Qiskit Aer 0.17.2
*   Matplotlib 3.10.7

All required Python libraries are listed in the `requirements.txt` file.

## Installation and Setup

To set up a local environment and run this simulation, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Shors_Algorithm_Simulation_MAHTI.git
    cd Shors_Algorithm_Simulation_MAHTI
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the simulation, execute the main script from the command line:

```bash
python run_shor_simulation.py
```

The script will perform the following actions:
1.  Construct the 9-qubit quantum circuit for Shor's algorithm with N=15 and a=7.
2.  Execute the circuit on the Qiskit `AerSimulator` for 2048 shots.
3.  Print the most frequent measurement outcome and the calculated period.
4.  Print the successfully computed factors (3 and 5) to the console.
5.  Save a plot of the measurement results as `shor_histogram.png`.

### Expected Output

You should see console output similar to this:

```
Executing Shor's algorithm for N=15 and a=7...
Most frequent measurement: 8
Measured phase: 0.25
Extracted period (p): 4
Factors found: {3, 5}
Simulation successful. Histogram saved to shor_histogram.png.```

And a plot file `shor_histogram.png` will be generated, showing clear peaks at outcomes 0, 8, 16, and 24.

## Citation

If you use this code or the associated research in your work, please cite both the repository and the research article.

### Citing this Repository

```bibtex
@software{Ali_Shor_s_Algorithm_Simulation_2025,
  author = {Ali, Syed Muhammad Muneeb},
  title = {{Shor's algorithm simulation for factoring 15 in Qiskit}},
  month = {10},
  year = {2025},
  publisher = {GitHub},
  version = {1.0.0},
  url = {https://github.com/alimuneeb24/Shors_Algorithm_Simulation_MAHTI}
}
```

### Citing the Paper

> [the full APA citation for your paper will be pasted here once it is published.]

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
