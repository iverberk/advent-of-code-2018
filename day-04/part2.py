import re
from datetime import datetime

events = {}

with open('input') as f:
    for line in f:
        (date, event) = re.match(r"\[(.*)\] (.*)", line).groups()
        events[datetime.strptime(date, '%Y-%m-%d %H:%M')] = event


def sort_events(events):
    for date in sorted(events):
        yield events[date], date.minute


guards = {}
guard = False
sleep_minute = 0

for event, current_minute in sort_events(events):
    if event.startswith('Guard'):
        guard = int(re.match(r"Guard #(\d+).*", event).group(1))
        if guard not in guards:
            guards[guard] = {
                'minutes': {m: 0 for m in range(60)},
                'total': 0
            }

    elif event.startswith("falls") and guard:
        sleep_minute = current_minute

    elif event.startswith("wakes") and guard:
        guards[guard]['total'] += (current_minute - sleep_minute)
        for m in range(sleep_minute, current_minute):
            guards[guard]['minutes'][m] += 1
        sleep_minute = 0

guard_id = 0
max_minute = 0
max_sleep = 0
for guard in guards:
    for minute, total in guards[guard]['minutes'].items():
        if total > max_sleep:
            max_sleep = total
            guard_id = guard
            max_minute = minute

print(guard_id, max_minute)
