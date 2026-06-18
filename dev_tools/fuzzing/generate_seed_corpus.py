#!/usr/bin/env python3
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates a seed corpus for oss-fuzz integration.

The corpus generated here is used by `fuzz_circuit.py` in the oss-fuzz project:
https://github.com/google/oss-fuzz/blob/master/projects/cirq/fuzz_circuit.py

The fuzz target expects sequences of bytes that Atheris's FuzzedDataProvider
consumes. Since it consumes these bytes in ways that are heavily dependent on
how FuzzedDataProvider is implemented, providing a rich set of random byte
streams is the standard way to seed the fuzzer.
"""

import os
import random
import zipfile
import tempfile

def generate_random_seed(length=1024):
    """Generates a random sequence of bytes for the seed corpus."""
    # The fuzzer consumes varying amounts of ints, we just provide random bytes
    # as FuzzedDataProvider translates these random bytes into its int requests.
    return bytes([random.randint(0, 255) for _ in range(length)])

def main():
    NUM_SEEDS = 200
    SEED_PREFIX = "cirq_fuzzing_"
    ZIP_NAME = "public.zip"

    # Ensure deterministic random generation for reproducibility if ever needed
    # though for a seed corpus, actual randomness is fine. We use a fixed seed
    # to guarantee we generate the same corpus each time the script is run.
    random.seed(42)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate seed files
        seed_files = []
        for i in range(1, NUM_SEEDS + 1):
            seed_filename = f"{SEED_PREFIX}{i:03d}.bin"
            seed_path = os.path.join(temp_dir, seed_filename)

            # Vary the length of the seeds to hit different limits in the fuzzer
            # The fuzzer consumes up to 5 ops, plus 2 ints for qubits and ops count.
            # Max bytes consumed per operation could be several depending on Atheris.
            length = random.randint(32, 1024)
            seed_bytes = generate_random_seed(length)

            with open(seed_path, 'wb') as f:
                f.write(seed_bytes)

            seed_files.append((seed_path, seed_filename))

        # Create zip file
        zip_path = os.path.join(os.path.dirname(__file__), ZIP_NAME)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filepath, arcname in seed_files:
                zf.write(filepath, arcname)

        print(f"Successfully generated seed corpus at {zip_path}")
        print(f"Included {NUM_SEEDS} files in the zip archive.")

if __name__ == "__main__":
    main()
