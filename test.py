from fibo_stark import generate_proof, fib_to, verify_proof
from merkle_tree import bin_length


def fri_proof_bin_length(fri_proof):
    return sum([32 + bin_length(x[1]) + bin_length(x[2]) for x in fri_proof[:-1]]) + len(b''.join(fri_proof[-1]))


def test_stark():
    # Input has to be a power of two, we also count zero, hence the - 1
    INPUT = 2 ** 9 - 1
    print("# Full STARK test")
    print(" Computing STARK for the %d-th Fibonacci number" % (INPUT + 1))
    output = fib_to(INPUT)[-1]
    proof = generate_proof(INPUT)
    m_root, l_root, main_branches, linear_comb_branches, fri_proof = proof
    L1 = bin_length(main_branches) + bin_length(linear_comb_branches)
    L2 = fri_proof_bin_length(fri_proof)
    print("Approx proof length: %d (branches), %d (FRI proof), %d (total)" % (L1, L2, L1 + L2))
    assert verify_proof(INPUT, output, proof)


def performance_test(n):
    for i in range(12, n):
        print("index:", i)
        INPUT = 2 ** i - 1
        print("# Full STARK test")
        print(" Computing STARK for the %d-th Fibonacci number" % (INPUT + 1))
        output = fib_to(INPUT)[-1]
        proof = generate_proof(INPUT)
        m_root, l_root, main_branches, linear_comb_branches, fri_proof = proof
        L1 = bin_length(main_branches) + bin_length(linear_comb_branches)
        L2 = fri_proof_bin_length(fri_proof)
        print("Approx proof length: %d (branches), %d (FRI proof), %d (total)" % (L1, L2, L1 + L2))
        assert verify_proof(INPUT, output, proof)
    print("done")


if __name__ == '__main__':
    # test_stark()
    performance_test(15)
