import time

import pyautogui as pg

TRY = 200
path = lambda x: f"E7/{x}.png"
last_op = None
conf: dict = None

buy_count = 0
guaji_count = 0
main_count = 0

not_print_img = ['v']


def click(*arg):
    time.sleep(conf['click_time'])
    print(f'click {arg}')
    pg.click(*arg)


def get_pin(img, count=0):
    global last_op
    while True:
        time.sleep(0.1)
        if count >= TRY and count != float('inf'):
            print('超过尝试次数，正在回溯上一次操作')
            if last_op is None:
                raise Exception('回溯失败，脚本已终止')
            else:
                last = last_op
                last_op = None
                op = get_pin(last)
                click(op)
                count = 0
        if not (img in not_print_img):
            print(f"正在定位{img}")
        res = pg.locateCenterOnScreen(path(img), confidence=0.7)
        if res is not None:
            break
        count += 1
    if not (img in not_print_img):
        print(f"定位成功{img} {res}")
    last_op = img
    return res


def click_v(count=0):
    v = get_pin('v', count=count)
    click(v)


def click_enter():
    for i in range(20):
        tjl = pg.locateCenterOnScreen(path("tjl"))
        f = pg.locateCenterOnScreen(path("f"))
        if tjl is not None and f is None:
            enter_t = get_pin('enter_t')
            click(enter_t)
        elif tjl is None and f is not None:
            cancel = get_pin('cancel')
            click(cancel)
    enter = get_pin('enter')
    click(enter)


def click_re():
    re = get_pin('re')
    click(re)


def click_ttk():
    ttk = get_pin('ttk')
    click(ttk)
    team = get_pin('team')
    click(team)
    click_kaishi()


def click_maoxian():
    maoxian = get_pin('maoxian')
    click(maoxian)
    seven = get_pin('7')
    click(seven)
    if conf['epic_hou']:
        epic = get_pin('epich')
    else:
        epic = get_pin('epic')
    click(epic)

    time.sleep(3)
    click_ttk()


def click_zhixian():
    zhixian = get_pin('zhixian')
    click(zhixian)
    st = get_pin('st')
    click(st.x, st.y + 50)
    in_zhixian = get_pin('in_zhixian')
    click(in_zhixian.x, in_zhixian.y + 100)
    mx = get_pin('mx')
    click(mx)
    click_ttk()


def click_menu_dating():
    menu = get_pin('menu')
    click(menu)
    dating = get_pin('go_dating')
    return dating


def click_dating():
    dating = get_pin('dating')
    for i in range(20):
        jinji = pg.locateCenterOnScreen(path("jinji"))
        if jinji is not None:
            print('出现紧急任务')
            if not (conf['urgent']):
                print('不执行紧急任务')
                enter_t = get_pin('enter_t')
                click(enter_t)
            else:
                print('执行紧急任务')
                go = get_pin('go')
                click(go)
                team = get_pin('team')
                click(team)
                click_kaishi()
                print(f'执行紧急任务中')
                click_v(count=float('inf'))
                click_enter()
                print(f'紧急任务执行完毕')
                dating = click_menu_dating()

    click(dating)


def click_kaishi():
    global buy_count
    kaishi = get_pin('kaishi')
    click(kaishi)
    for i in range(20):
        buy = pg.locateCenterOnScreen(path("buy"), confidence=0.7)
        if buy is not None:
            if not (conf['ap_buy']):
                raise Exception('体力不足')
            if buy_count >= conf['ap_count']:
                raise Exception('体力不足，达到购买次数上限')
            yezi = get_pin('yezi')
            click(yezi)
            click(buy)
            kaishi = get_pin('kaishi')
            click(kaishi)
            buy_count += 1
            break


def click_zuixiaohua():
    zxh = get_pin('zuixiaohua')
    click(zxh)
    enter = get_pin('enter_b')
    click(enter)


def check_auto_mission():
    global guaji_count
    if guaji_count >= conf['guaji_count']:
        return
    bag = get_pin("bag")

    click(bag.x - 50, bag.y + 20)

    while True:
        ing = pg.locateCenterOnScreen(path("in"))
        fin = pg.locateCenterOnScreen(path("jieshu"))
        shop = pg.locateCenterOnScreen(path('shop'))
        if ing is None and fin is None and shop is None:
            continue
        elif ing != None and fin == None and shop is None:
            click(bag.x - 50, bag.y + 20)
        elif ing == None and fin != None and shop is None:  # 重启自动任务
            big = get_pin("zuidahua")
            click(big)
            click_v()
            click_enter()
            click_re()
            click_kaishi()
            click_zuixiaohua()
            guaji_count += 1
        else:
            print('挂机任务已退出执行(异常退出)')
            guaji_count = float('inf')
            click(click_menu_dating())

        break



