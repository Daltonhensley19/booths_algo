import platform
import os


# Function which, as the name implies, tests a single bit. We use this
# in order to "remember" the sign of the word (i.e. bit-17) after a right shift
def is_kth_bit_set(n: int, k: int) -> bool:
    if (n & (1 << (k - 1))):
        return True
    else:
        return False


# Function which can extract the following parts of the 17-bit word
# `a`, `q`, `q1`, and the final answer `aq`.
def get_value(num: int, choice: str) -> int:

    requested_value = 0
    if choice == "a":
        requested_value = (num >> 9) & 0xFF
    elif choice == "q":
        requested_value = (num >> 1) & 0xFF
    elif choice == "q1":
        requested_value = num & 1
    elif choice == "aq":
        requested_value = (num >> 1) & 0xFFFF
    else:
        print("ERROR: invaild register!\n")

    return requested_value


# Function which safely clears the terminal
def safe_clear():
    if platform.system() == "win32":
        os.system("cls")
    else:
        os.system("clear")


def main():
    N = 0
    a = 0x00
    q_1 = 0

    a_q_merge = 0b0000_0000_0000_0000_0

    q = int(input("Enter a value in range [-2^8, 2^8-1]\n"))
    safe_clear()

    while q < -2**8 or q > 2**8 - 1:
        print("ERROR: Try again. Enter number for q.\n")

        q = int(input("Enter a value in range [-2^8, 2^8-1]\n"))
        safe_clear()

    m = int(input("Enter a value in range [-2^8, 2^8-1]\n"))
    safe_clear()

    while m < -2**8 or m > 2**8 - 1:
        print("ERROR: Try again. Enter number for m.\n")

        m = int(input("Enter a value in range [-2^8, 2^8-1]\n"))
        safe_clear()

    print("Intialization: ")
    print(f"a\t\t\tq\t\t\tq1\t\tm")
    print(f"{a:>08b}\t\t{q:>08b}\t\t{q_1}\t\t{m:>08b}")

    a_q_merge ^= (a << 9)
    a_q_merge ^= (q << 1)
    a_q_merge ^= q_1

    print(f"{a_q_merge:>017b}")

    while N != 8:
        if is_kth_bit_set(a_q_merge, 2) and is_kth_bit_set(a_q_merge, 1):
            if is_kth_bit_set(a_q_merge, 17):
                a_q_merge >>= 1
                a_q_merge |= 0b1000_0000_0000_0000_0
            else:
                a_q_merge >>= 1

            N += 1

            print(f"Cycle {N} +++++++ Step 1 1\n")
        elif not is_kth_bit_set(a_q_merge, 2) and not is_kth_bit_set(
                a_q_merge, 1):
            if is_kth_bit_set(a_q_merge, 17):
                a_q_merge >>= 1
                a_q_merge |= 0b1000_0000_0000_0000_0
            else:
                a_q_merge >>= 1

            N += 1

            print(f"Cycle {N} +++++++ Step 0 0\n")
        elif is_kth_bit_set(a_q_merge, 2) and not is_kth_bit_set(a_q_merge, 1):
            a = (get_value(a_q_merge, "a") + (~m) + 1) & 0xFF
            a_q_merge = (a_q_merge & 0b0000_0000_1111_1111_1)
            a_q_merge |= (a << 9)

            if is_kth_bit_set(a_q_merge, 17):
                a_q_merge >>= 1
                a_q_merge |= 0b1000_0000_0000_0000_0
            else:
                a_q_merge >>= 1

            N += 1
            print(f"Cycle {N} +++++++ Step 1 0\n")
        elif not is_kth_bit_set(a_q_merge, 2) and is_kth_bit_set(a_q_merge, 1):
            a = (get_value(a_q_merge, "a") + m) & 0xFF
            a_q_merge = (a_q_merge & 0b0000_0000_1111_1111_1)
            a_q_merge |= (a << 9)

            if is_kth_bit_set(a_q_merge, 17):
                a_q_merge >>= 1
                a_q_merge |= 0b1000_0000_0000_0000_0
            else:
                a_q_merge >>= 1

            N += 1

            print(f"Cycle {N} +++++++ Step 0 1\n")

    print(
        f"Answer: {get_value(a_q_merge, 'aq'):>016b} ({get_value(a_q_merge, 'aq')})"
    )
    print(f"{get_value(a_q_merge, 'a'):>08b}")


main()
