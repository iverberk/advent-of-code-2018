serial = 5719
grid = {}
for y in range(1, 300+1):
    for x in range(1, 300+1):
        rack_id = x + 10
        power_level = (rack_id * y + serial) * rack_id
        if power_level >= 100:
            power_level = (power_level // 100) % 10 - 5
        else:
            power_level = -5

        grid[(x, y)] = power_level

max_sum = 0
max_x, max_y = 0, 0
max_size = 0
for size in range(0, 300):
    for y in range(1, 300-size):
        for x in range(1, 300-size):
            s = 0
            for dy in range(0, size):
                for dx in range(0, size):
                    s += grid[(x+dx, y+dy)]

            if s > max_sum:
                max_x = x
                max_y = y
                max_sum = s
                max_size = size
    print(max_x, max_y, max_size)

print("{},{}: {}".format(max_x, max_y, max_sum))
