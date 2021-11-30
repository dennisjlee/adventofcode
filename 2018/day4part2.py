#!/usr/bin/env python3

from collections import defaultdict, Counter
import sys
import re

def main(filename):
    guard_regex = re.compile(r'.*Guard #(\d+) begins shift')
    time_regex = re.compile(r'\[\d\d\d\d-\d\d-\d\d 00:(\d\d)\] (falls asleep|wakes up)')
    with open(filename) as f:
        lines = sorted(f.readlines())

    current_guard = None
    minutes_by_guard = defaultdict(Counter)
    i = 0
    while i < len(lines):
        line = lines[i]
        guard_match = guard_regex.match(line)
        if guard_match:
            current_guard = int(guard_match.group(1))
        else:
            time_match1 = time_regex.match(line)
            time_match2 = time_regex.match(lines[i+1])
            if time_match1 and time_match2:
                i += 1
                start_minute = int(time_match1.group(1))
                end_minute = int(time_match2.group(1))
                minutes_by_guard[current_guard].update(range(start_minute, end_minute))
        i += 1

    most_sleepy_combo = None
    max_asleep_incidents = 0
    for guard, minutes in minutes_by_guard.items():
        max_minute, count = minutes.most_common(1)[0]
        if count > max_asleep_incidents:
            max_asleep_incidents = count
            most_sleepy_combo = (guard, max_minute)

    print('Most sleepy combo', most_sleepy_combo)
    print('Max sleeping incidents', max_asleep_incidents)
    print('Answer', most_sleepy_combo[0] * most_sleepy_combo[1])


if __name__ == '__main__':
    main(sys.argv[1])
