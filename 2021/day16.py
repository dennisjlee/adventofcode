from __future__ import annotations

import operator
import sys
from functools import reduce
from typing import Optional


class Packet:
    version: int
    type_id: int
    literal: Optional[int]
    length: int
    subpackets: list[Packet]

    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = type_id
        self.literal = None
        self.subpackets = []

    @staticmethod
    def parse(bits: str, start_index=0):
        index = start_index
        version = int(bits[index:index + 3], 2)
        index += 3
        type_id = int(bits[index:index + 3], 2)
        index += 3
        packet = Packet(version, type_id)

        if type_id == 4:
            value_buffer = []
            chunk_index = 0
            for chunk_index in range((len(bits) - index) // 5):
                chunk_start = index + 5 * chunk_index
                chunk = bits[chunk_start:chunk_start + 5]
                value_buffer.append(chunk[1:])
                if chunk[0] == '0':
                    break
            packet.literal = int(''.join(value_buffer), 2)
            index += (chunk_index + 1) * 5
        else:
            length_type_id = int(bits[index], 2)
            index += 1
            if length_type_id == 0:
                total_length = int(bits[index:index + 15], 2)
                index += 15
                target_index = index + total_length
                while index < target_index:
                    subpacket = Packet.parse(bits, index)
                    index += subpacket.length
                    packet.subpackets.append(subpacket)
            else:
                subpacket_count = int(bits[index:index + 11], 2)
                index += 11
                for _ in range(subpacket_count):
                    subpacket = Packet.parse(bits, index)
                    index += subpacket.length
                    packet.subpackets.append(subpacket)

        packet.length = index - start_index

        return packet

    @staticmethod
    def parse_hex(hex: str) -> Packet:
        n = int(hex, 16)
        binary_string = bin(n)[2:]
        binary_string = binary_string.zfill(next_multiple4(len(binary_string)))
        return Packet.parse(binary_string)

    def sum_version(self):
        return self.version + sum(s.sum_version() for s in self.subpackets)

    def value(self):
        t = self.type_id
        if t == 4:
            return self.literal

        subvalues = [s.value() for s in self.subpackets]
        if t == 0:
            return sum(subvalues)
        elif t == 1:
            return reduce(operator.mul, subvalues, 1)
        elif t == 2:
            return min(subvalues)
        elif t == 3:
            return max(subvalues)
        elif t == 5:
            return int(subvalues[0] > subvalues[1])
        elif t == 6:
            return int(subvalues[0] < subvalues[1])
        elif t == 7:
            return int(subvalues[0] == subvalues[1])


def next_multiple4(n: int):
    return n + (4 - (n % 4) if (n % 4) else 0)


def main():
    with open(sys.argv[1]) as f:
        hex = f.read().strip()

    # part 1
    packet = Packet.parse_hex(hex)
    print(packet.sum_version())

    # part 2
    print(packet.value())


if __name__ == '__main__':
    main()
