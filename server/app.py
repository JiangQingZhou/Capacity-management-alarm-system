import datetime

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/getMsg": {"origins": "*"}, r"/getchart": {"origins": "*"}})


@app.route('/getchart', methods=['GET', 'POST'])
@cross_origin()
def get_chart():
    data = request.json.get('data')
    label = request.json.get('model')
    period = request.json.get('period')

    path = '../result/' + label + '_data' + data + '.csv'
    ori_path = '../origin_data/' + 'data' + data + '.csv'
    reader = pd.read_csv(path).values.tolist()
    ori_reader = pd.read_csv(ori_path).values.tolist()

    origin_data = []
    for i in ori_reader:
        origin_data.append(i[1])
    values = [0, 0, 0, 0, 0]
    up_values = [0, 0, 0, 0, 0]
    down_values = [0, 0, 0, 0, 0]
    collect_time = []

    start_date = ori_reader[0][0].replace('/', '-')
    dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    print(dt)

    tot = len(origin_data) + int(period)

    for index, value in enumerate(reader):
        if index == tot:
            print(index)
            break
        values.append(value[1])
        up_values.append(1.2 * value[1])
        down_values.append(0.8 * value[1])
        out_date = (dt + datetime.timedelta(days=index)).strftime("%Y-%m-%d")
        collect_time.append(out_date)

    res = {
        'values': values,
        'collect_time': collect_time,
        'up_values': up_values,
        'down_values': down_values,
        'origin_data': origin_data,
    }
    print(values)
    print(collect_time)
    return res


@app.route('/getalarm', methods=['GET', 'POST'])
@cross_origin()
def get_alarm():
    data = request.json.get('data')
    label = request.json.get('model')

    str = '00'
    if len(data) == 2:
        str = '0'

    path = '../result/' + label + '_' + str + data + '.csv'
    ori_path = '../origin_data/' + str + data + '.csv'
    reader = pd.read_csv(path).values.tolist()
    ori_reader = pd.read_csv(ori_path).values.tolist()

    origin_data = []
    collect_time = []
    for i in ori_reader:
        origin_data.append(i[2])
        collect_time.append(i[0])

    values = [0, 0, 0, 0, 0]
    up_values = [0, 0, 0, 0, 0]
    down_values = [0, 0, 0, 0, 0]
    alarm_arr = ['n', 'n', 'n', 'n', 'n']
    tot = len(origin_data)

    for index, value in enumerate(reader):
        if index + 5 == tot:
            print(index)
            break
        high = 1.2 * value[1]
        low = 0.8 * value[1]
        if origin_data[index + 5] > high:
            alarm_arr.append('Higher')
        elif origin_data[index + 5] < low:
            alarm_arr.append('Lower')
        else:
            alarm_arr.append('n')
        values.append(value[1])
        up_values.append(high)
        down_values.append(low)

    res = {
        'values': values,
        'collect_time': collect_time,
        'up_values': up_values,
        'down_values': down_values,
        'origin_data': origin_data,
        'alarm': alarm_arr
    }
    # print(alarm_arr)
    print(values)
    return res


if __name__ == '__main__':
    app.run()
