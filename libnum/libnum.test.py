#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import libnum
import operator

class primes(unittest.TestCase):
    def test_primes(self):
        for method in (None, "Eratosphen sieve"):
            p = libnum.primes(100000, method=method)
            self.assertEqual(p[0], 2)
            self.assertEqual(len(p), 9592)
            self.assertEqual(p[9591], 99991)  # 9592th prime number
            self.assertRaises(TypeError, libnum.primes, "")
            
            self.assertEqual(libnum.primes(-1), [])
            self.assertEqual(libnum.primes(1), [])
        self.assertRaises(TypeError, libnum.primes, 1000000, "fake")

    def test_factorize(self):
        plist0 = [3, 5, 5, 5, 5, 5, 19, 19, 1993]
        n = reduce(operator.mul, plist0, 1)
        plist1 = libnum.factorize(n)
        self.assertEqual(plist0, plist1)

        self.assertEqual(libnum.factorize(1), [1])
        self.assertEqual(libnum.factorize(2), [2])
        self.assertEqual(libnum.factorize(4), [2, 2])
        self.assertRaises(ValueError, libnum.factorize, 0)
        self.assertRaises(TypeError, libnum.factorize, "")
    
    def test_genprime(self):
        for size in [2, 10, 64, 128, 129]:
            p = libnum.generate_prime(size, k=25)
            self.assertEqual(libnum.len_in_bits(p), size)
            self.assertTrue(libnum.ferma_test(p, k=15))

        self.assertRaises(ValueError, libnum.generate_prime, 1)
        self.assertRaises(TypeError, libnum.generate_prime, "")

    def test_genprime_str(self):
        begin = "preved medved \xde\xad\xbe\xef\x00\x00\x00\x00"
        n = libnum.generate_prime_from_string(begin)
        s = libnum.n2s(n)
        self.assertTrue(s.startswith(begin))
        self.assertTrue(libnum.ferma_test(n, 15))
        self.assertRaises(TypeError, libnum.generate_prime_from_string, 31337)
        self.assertRaises(ValueError, libnum.generate_prime_from_string, "test", 8)
        self.assertRaises(ValueError, libnum.generate_prime_from_string, "test", -8)

    def test_fermatest(self):
        self.assertTrue(libnum.ferma_test(3, 50))
        self.assertTrue(libnum.ferma_test(1993, 50))
        self.assertTrue(libnum.ferma_test(17333, 50))
        self.assertTrue(libnum.ferma_test(1582541, 50))
        self.assertTrue(not libnum.ferma_test(4, 50))
        self.assertTrue(not libnum.ferma_test(1994, 50))
        self.assertTrue(not libnum.ferma_test(1995, 50))
        self.assertRaises(TypeError, libnum.ferma_test, "test")


class strings(unittest.TestCase):
    def test_s2n(self):
        s = "long string to test"
        val = 2418187513319072758194084480823884981773628276
        self.assertEqual(libnum.s2n(s), val)
        self.assertRaises(TypeError, libnum.s2n, 100)

    def test_n2s(self):
        s = "long string to test"
        val = 2418187513319072758194084480823884981773628276
        self.assertEqual(libnum.n2s(val), s)
        self.assertRaises(TypeError, libnum.n2s, "qwe")

    def test_s2b(self):
        s = "just string"
        bs = "01101010011101010111001101110100001000000111"
        bs += "00110111010001110010011010010110111001100111"
        self.assertEqual(libnum.s2b(s), bs)
        self.assertRaises(TypeError, libnum.s2b, 123)

    def test_b2s(self):
        s = "just string"
        bs = "01101010011101010111001101110100001000000111"
        bs += "00110111010001110010011010010110111001100111"
        self.assertEqual(libnum.b2s(bs), s)
        self.assertRaises(TypeError, libnum.b2s, 123)
        self.assertRaises(ValueError, libnum.b2s, "deadbeef")


class common_math(unittest.TestCase):
    def test_len_in_bits(self):
        self.assertEqual(libnum.len_in_bits(1023), 10)
        self.assertEqual(libnum.len_in_bits(1024), 11)
        self.assertEqual(libnum.len_in_bits(1), 1)

        self.assertRaises(ValueError, libnum.len_in_bits, 0)
        self.assertRaises(TypeError, libnum.len_in_bits, "qwe")

    def test_nroot(self):
        for x in range(0, 100):
            for p in range(1, 3):
                n = x ** p
                self.assertEqual(libnum.nroot(n, p), x)

        self.assertEqual(libnum.nroot(-64, 3), -4)
        self.assertEqual(libnum.nroot(100, 2), 10)
        self.assertEqual(libnum.nroot(999, 3), 9)
        self.assertEqual(libnum.nroot(1000, 3), 10)        
        self.assertEqual(libnum.nroot(1001, 3), 10)

        self.assertRaises(ValueError, libnum.nroot, 100, -1)
        self.assertRaises(ValueError, libnum.nroot, -100, 4)
        self.assertRaises(ValueError, libnum.nroot, 1, 0)
        self.assertRaises(TypeError, libnum.nroot, "qwe")

    def test_gcd_pair(self):
        self.assertEqual(libnum.gcd(100, 75), 25)
        self.assertEqual(libnum.gcd(-10, 155), 5)
        self.assertEqual(libnum.gcd(30, -77), 1)
        self.assertEqual(libnum.gcd(0, -77), 77)
        self.assertEqual(libnum.gcd(0, 0), 0)
        self.assertEqual(libnum.gcd(13, 0), 13)
        self.assertRaises(TypeError, libnum.gcd, "qwe", 10)
        self.assertRaises(TypeError, libnum.gcd, 10, "qwe")

    def test_gcd_list(self):
        self.assertEqual(libnum.gcd(100, 75, 150, -325), 25)
        self.assertEqual(libnum.gcd(-10, -155, -50), 5)
        self.assertEqual(libnum.gcd(-13), 13)
        self.assertEqual(libnum.gcd(3, 0, 30), 3)
        self.assertRaises(TypeError, libnum.gcd, "qwe")

    def test_lcm_pair(self):
        self.assertEqual(libnum.lcm(100, 75), 300)
        self.assertEqual(libnum.lcm(1, 31), 31)
        self.assertEqual(libnum.lcm(2, 37), 74)

        self.assertRaises(ZeroDivisionError, libnum.lcm, 1, 0)
        self.assertRaises(ZeroDivisionError, libnum.lcm, 0, 1)
        self.assertRaises(TypeError, libnum.lcm, "qwe", 10)
        self.assertRaises(TypeError, libnum.lcm, 10, "qwe")

    def test_lcm_list(self):
        self.assertEqual(libnum.lcm(100, 75), 300)
        self.assertEqual(libnum.lcm(100500), 100500)
        self.assertEqual(libnum.lcm(10, 20, 30, 40, 5, 80), 240)

        self.assertRaises(ZeroDivisionError, libnum.lcm, 123, 0, 0)
        self.assertRaises(ZeroDivisionError, libnum.lcm, 0, 100, 123)
        self.assertRaises(TypeError, libnum.lcm, "qwe", 10)
        self.assertRaises(TypeError, libnum.lcm, 10, "qwe")


class modulus_math(unittest.TestCase):
    def test_has_invmod(self):
        for modulus in range(2, 1000, 31):
            for a in range(2, modulus, 5):
                if libnum.has_invmod(a, modulus):
                    x = libnum.invmod(a, modulus)
                    self.assertEqual((a * x) % modulus, 1)
                else:
                    self.assertNotEqual(libnum.gcd(a, modulus), 1)
        self.assertRaises(ValueError, libnum.has_invmod, 1, 1)
        self.assertRaises(ValueError, libnum.has_invmod, 1, 0)
        self.assertRaises(ValueError, libnum.has_invmod, 1, -100)
        self.assertRaises(TypeError, libnum.has_invmod, "qwe", 10)
        self.assertRaises(TypeError, libnum.has_invmod, 10, "qwe")

    def test_invmod(self):
        for modulus in range(2, 1000, 37):
            for a in range(2, modulus, 5):
                if libnum.has_invmod(a, modulus):
                    x = libnum.invmod(a, modulus)
                    self.assertEqual((a * x) % modulus, 1)
                else:
                    self.assertRaises(ValueError, libnum.invmod, a, modulus)
        self.assertRaises(ValueError, libnum.invmod, 1, 1)
        self.assertRaises(ValueError, libnum.invmod, 1, 0)
        self.assertRaises(ValueError, libnum.invmod, 1, -100)
        self.assertRaises(TypeError, libnum.invmod, "qwe", 10)
        self.assertRaises(TypeError, libnum.invmod, 10, "qwe")

    def test_euclid(self):
        for b in range(1, 1000, 13):
            for a in range(1, 1000, 7):
                g = libnum.gcd(a, b)
                x, y, g2 = libnum.xgcd(a, b)
                self.assertEqual(g, g2)
                self.assertEqual(a * x + b * y, g)
        self.assertEqual(libnum.xgcd(0, 10)[1:], (1, 10))
        self.assertEqual(libnum.xgcd(10, 0)[0::2], (1, 10))
        self.assertEqual(libnum.xgcd(0, 0)[2], 0)
        self.assertRaises(TypeError, libnum.xgcd, "qwe", 10)
        self.assertRaises(TypeError, libnum.xgcd, 10, "qwe")

    def test_sqrt(self):
        for module in [2, 3, 5, 7, 11, 17, 137, 1993]:
            for i in range(0, module):
                if not libnum.prime_has_sqrt(i, module):
                    continue
                s = libnum.prime_sqrtmod(i, module)[0]
                self.assertEqual(s * s % module, i)
        self.assertTrue(sorted(libnum.prime_sqrtmod(3, 11)) == [5, 6])

    def test_crt(self):
        for module in [2, 3, 5, 7, 1993]:
            for a in xrange(module):
                self.assertEqual(libnum.solve_crt([a], [module]), a)
        modules = [2, 3, 5, 19, 137]
        for i in xrange(1000):
            rems = []
            a = 7
            for m in modules:
                rems.append(a % m)
                a += 31337
            a = libnum.solve_crt(rems, modules)
            for i in xrange(len(modules)):
                self.assertEqual(rems[i], a % modules[i])
        self.assertRaises(TypeError, libnum.solve_crt, [1, 2, 3], [1, 2])
        self.assertRaises(ValueError, libnum.solve_crt, [], []);


class stuff(unittest.TestCase):
    def test_grey_code(self):
        pg = 0
        for a in range(10000):
            g = libnum.grey_code(a)
            if a:  # two consequent grey numbers differ only in one bit
                x = g ^ pg
                self.assertEqual(x ^ (x - 1), x * 2 - 1)
            pg = g
            self.assertEqual(a, libnum.rev_grey_code(g))
        self.assertRaises(TypeError, libnum.grey_code, "qwe")


if __name__ == "__main__":
    unittest.main()
