def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def generate_prime_numbers():
    primes = []
    for num in range(1, 251):
        if is_prime(num):
            primes.append(num)
    return primes

def save_primes_to_file(primes, filename='results.txt'):
    with open(filename, 'w') as file:
        for prime in primes:
            file.write(f"{prime}\n")
            print(prime)

if __name__ == "__main__":
    prime_numbers = generate_prime_numbers()
    save_primes_to_file(prime_numbers)
