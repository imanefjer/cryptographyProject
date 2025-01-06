import requests
import json
from dataclasses import dataclass
from typing import List, Dict
import time
import base64

@dataclass
class InterceptedData:
    timestamp: float
    sender: str
    ciphertext: str

@dataclass
class KeyData:
    timestamp: float
    sender: str
    n: str
    e: int

class BenchmarkAttack:
    def __init__(self, eve_server: str = "http://127.0.0.1:8002"):
        self.eve_url = eve_server
        self.messages: List[InterceptedData] = []
        self.keys: List[KeyData] = []
        
    def fetch_intercepted_data(self) -> tuple[List[InterceptedData], List[KeyData]]:
        """Fetch all intercepted messages and keys from Eve's server"""
        try:
            # In a real implementation, we'd need endpoints to get the stored data
            # For now, we'll simulate it with direct data
            messages = [
                InterceptedData(
                    timestamp=time.time(),
                    sender="alice",
                    ciphertext="encrypted_data_here"
                )
            ]
            
            keys = [
                KeyData(
                    timestamp=time.time(),
                    sender="alice",
                    n="ABC123",
                    e=65537
                )
            ]
            
            return messages, keys
            
        except requests.RequestException as e:
            print(f"Error fetching data from Eve's server: {e}")
            return [], []

    def decode_ciphertext(self, ciphertext: str) -> bytes:
        """Convert intercepted ciphertext string to bytes"""
        try:
            return base64.b64decode(ciphertext)
        except Exception as e:
            print(f"Error decoding ciphertext: {e}")
            return b''

    def create_oracle(self, target_url: str):
        """Create padding oracle function for the target server"""
        def oracle(ciphertext: bytes) -> bool:
            try:
                # In real implementation, this would send the ciphertext to target
                # and check if it returns a padding error
                # This is a placeholder implementation
                return True
            except Exception as e:
                print(f"Oracle error: {e}")
                return False
        return oracle

    def run_benchmark(self, num_samples: int = 1) -> Dict:
        """Run padding oracle attack benchmark"""
        results = {
            'total_time': 0,
            'successful_attacks': 0,
            'failed_attacks': 0,
            'avg_oracle_calls': 0,
            'samples': []
        }

        messages, keys = self.fetch_intercepted_data()
        if not messages or not keys:
            print("No intercepted data available")
            return results

        for i in range(min(num_samples, len(messages))):
            message = messages[i]
            matching_key = next(
                (k for k in keys if k.sender == message.sender),
                None
            )
            
            if not matching_key:
                print(f"No matching key found for {message.sender}")
                continue

            try:
                start_time = time.time()
                
                # Create oracle for this target
                oracle = self.create_oracle(f"http://{message.sender}:8001")
                
                # Setup attack parameters
                ciphertext = self.decode_ciphertext(message.ciphertext)
                if not ciphertext:
                    continue

                # Initialize padding oracle attack
                # Using the implementation from previous artifact
                attack = PaddingOracleAttack(
                    pub_key=RSAPublicKey(
                        n=int(matching_key.n, 16),
                        e=matching_key.e
                    ),
                    block_size=256,  # Assuming 2048-bit RSA
                    oracle_fn=oracle
                )

                # Run attack
                plaintext = attack.decrypt(ciphertext)
                
                # Record results
                attack_time = time.time() - start_time
                results['samples'].append({
                    'sender': message.sender,
                    'time': attack_time,
                    'oracle_calls': attack.calls
                })
                
                results['successful_attacks'] += 1
                results['total_time'] += attack_time
                results['avg_oracle_calls'] += attack.calls

            except Exception as e:
                print(f"Attack failed for {message.sender}: {e}")
                results['failed_attacks'] += 1

        # Calculate averages
        if results['successful_attacks'] > 0:
            results['avg_oracle_calls'] //= results['successful_attacks']
            results['avg_time'] = results['total_time'] / results['successful_attacks']

        return results

def main():
    # Initialize benchmark
    benchmark = BenchmarkAttack()
    
    print("Starting padding oracle attack benchmark...")
    print("Fetching intercepted messages from Eve's server...")
    
    # Run benchmark with 5 samples
    results = benchmark.run_benchmark(num_samples=5)
    
    # Print results
    print("\nBenchmark Results:")
    print("-" * 50)
    print(f"Successful attacks: {results['successful_attacks']}")
    print(f"Failed attacks: {results['failed_attacks']}")
    if results['successful_attacks'] > 0:
        print(f"Average time per successful attack: {results['avg_time']:.2f} seconds")
        print(f"Average oracle calls per attack: {results['avg_oracle_calls']}")
    
    # Print individual sample results
    print("\nDetailed Sample Results:")
    print("-" * 50)
    for sample in results['samples']:
        print(f"Sender: {sample['sender']}")
        print(f"Attack time: {sample['time']:.2f} seconds")
        print(f"Oracle calls: {sample['oracle_calls']}")
        print("-" * 25)

if __name__ == "__main__":
    main()