from web import driver
import asyncio
from selenium.webdriver.common.by import By


async def handle_help():
    print("可用指令列表：")
    for command, details in commands.items():
        print(f"#{command} - {details['info']}")


async def handle_list():
    # 查找历史对话的 li 元素
    history_items = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid^="history-item-"]')

    if not history_items:
        print("没有找到历史对话。")
        return

    # 提取前10个对话的文本内容，并打印
    for i, item in enumerate(history_items[:10]):  # 限制为前10个
        title_element = item.find_element(By.CSS_SELECTOR, 'a')
        title_text = title_element.text
        print(f"{i + 1}. {title_text}")

    # 获取用户输入的数字
    while True:
        try:
            user_input = await asyncio.to_thread(input, "请输入要查看的对话编号: ")
            choice = int(user_input) - 1  # 将用户输入的1-10映射到索引0-9

            if 0 <= choice < len(history_items[:10]):
                # 点击对应的历史对话
                history_items[choice].find_element(By.CSS_SELECTOR, 'a').click()
                print(f"已选择对话: {history_items[choice].text}")
                break
            else:
                print("输入的编号超出范围，请重新输入。")
        except ValueError:
            print("请输入有效的数字。")

# 定义指令映射
commands = {
    'help': {'handler': handle_help, 'info': "cmd list"},
    'list': {'handler': handle_list, 'info': "show chat history list"},
    # 在这里可以添加更多的指令映射
}


# 检查指令并调用对应的函数
async def handle_command(command):
    command_name = command.lstrip('#')
    if command_name in commands:
        await commands[command_name]['handler']()  # 调用相应的指令函数
    else:
        print(f"未知指令: {command_name}")
        await handle_help()  # 调用帮助函数
