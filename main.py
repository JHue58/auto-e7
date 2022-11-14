import time

import click
import click as c
import yaml


def get_conf():
    with open('conf.yml', 'r', encoding='utf-8') as file:
        cfg = file.read()
    params = yaml.load(cfg, Loader=yaml.SafeLoader)
    return params


def inf_check(conf: dict):
    for i in conf:
        if conf[i] == -1:
            conf[i] = float('inf')


if '__main__' == __name__:
    conf = get_conf()
    inf_check(conf)
    print(
        '\n'.join([
            f"刷取模式: {conf['mode']}",
            f"重复次数: {conf['count']}次",
            f"自动购买体力: {conf['ap_buy']}",
            f"自动购买体力次数: {conf['ap_count']}次",
            f"点击等待时间: {conf['click_time']}秒",
            f"是否执行挂机任务: {conf['guaji']}",
            f"挂机任务重复次数: {conf['guaji_count']}次",
            f"是否自动执行紧急任务:{conf['urgent']}",
        ])
    )

    c.conf = conf
    print('脚本将在5S后启动')
    main_count = 0
    time.sleep(5)

    while True:
        if conf['guaji']:
            print('执行挂机任务检查')
            c.check_auto_mission()
        if conf['mode'] == '主线':
            c.click_maoxian()
            main_count += 1
        elif conf['mode'] == '活动':
            c.click_zhixian()
            main_count += 1
        print(f'第{main_count}次刷取中')
        c.click_v(count=float('inf'))
        print(f'刷取成功')
        c.click_enter()
        c.click_dating()
