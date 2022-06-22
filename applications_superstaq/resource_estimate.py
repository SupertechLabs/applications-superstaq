from dataclasses import dataclass

@dataclass
class ResourceEstimate:
    num_single_qubit_gates: int
    num_two_qubit_gates: int
    depth: int