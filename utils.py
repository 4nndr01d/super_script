import time


def await_user(seconds):
    print('Контроль передается пользователю')
    for i in range(seconds):
        time.sleep(1)
        if i % 5 == 0:
            print(f"Осталось {seconds - i} сек...")
    print('Контроль возвращается боту')