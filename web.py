from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import asyncio
from conf import config
from discord_bot import client

# 初始化Chrome浏览器
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 可选：隐藏浏览器窗口
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(config["CHROME_PROFILE_PATH"])
options.add_argument("--no-sandbox")  # 禁用沙盒模式
options.add_argument("--disable-dev-shm-usage")  # 使用/dev/shm共享内存
options.add_argument("--remote-debugging-port=9222")  # 启用远程调试端口

# 使用Service来启动ChromeDriver
service = Service(config["CHROME_DRIVER_PATH"])
driver = webdriver.Chrome(service=service, options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
    """
})

# 使用selenium-stealth隐藏Selenium特征
stealth(driver,
        languages=["zh-CN", "zh"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# 打开ChatGPT页面
driver.get("https://chat.openai.com/chat")

# 提示登录，用户需要手动登录
input("请在浏览器中登录ChatGPT账户，然后按下Enter键继续...")


async def send_message_to_chatgpt(message):
    # 显式等待，直到输入框可见并可交互
    input_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "prompt-textarea"))
    )

    # 在输入框中输入消息
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)  # 模拟按下回车键

    await asyncio.sleep(3)

    # 等待ChatGPT响应
    WebDriverWait(driver, 120).until(
        EC.invisibility_of_element_located((By.XPATH, '//button[@data-testid="stop-button"]'))
    )

    # 获取所有的对话元素
    conversation_turns = driver.find_elements(By.TAG_NAME, "article")

    # 获取最后一条对话内容
    if conversation_turns:
        last_turn = conversation_turns[-1]  # 获取最后一个article元素
        last_turn_text = last_turn.text  # 获取文本内容
        print("最后一条对话内容:", last_turn_text)

        # 调用 Discord 发送消息功能
        await client.send_message_to_discord(last_turn_text)
    else:
        print("没有找到对话内容")
        return


def driver_exit():
    driver.quit()
