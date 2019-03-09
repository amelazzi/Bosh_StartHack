import json
import time
from constants import json_mis_path
from create_messages import check_belt, check_blinkers, plot_points, check_lights, check_speed


with open(json_mis_path, 'w') as json_file:
    json.dump([{}],json_file)
check_time = {
    "belt": 5,
    "lights": 5,
}

if __name__ == '__main__':
    start_time = time.time()
    while(1):
        mistakes = []
        if (check_time['belt'] == 0):
            check_time['belt'] = 5
            m = check_belt()
            if (m):
                mistakes.append(m)

        m = check_blinkers()
        if (m):
            mistakes.append(m)

        if (check_time['lights'] == 0):
            check_time['lights'] = 5
            m = check_lights()
            if (m):
                mistakes.append(m)


        m = check_speed()
        if (m):
            mistakes.append(m)

        plot_points()

        for i in check_time:
            check_time[i] -= 1

        with open (json_mis_path) as json_file:
            data = json.load(json_file)
        print(data)
        for i in mistakes:
            if (i not in data[0]):
                data.append({'time' :"%.2f" % (time.time() - start_time) + ' seconds.', "error" : i })
                data[0][i] = 0

        with open (json_mis_path, 'w') as json_file:
            json.dump(data, json_file)


        time.sleep(1)

