import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from dotenv import load_dotenv
import os

load_dotenv()

DEEPL_USERNAME = os.getenv("DEEPL_USERNAME")
DEEPL_PASSWORD = os.getenv("DEEPL_PASSWORD")

logging.basicConfig(level=logging.INFO)

def get_deepl_session():
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get("https://www.deepl.com/login")

    try:
        time.sleep(3)
        login_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
        )

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        login_input.send_keys(DEEPL_USERNAME)
        password_input.send_keys(DEEPL_PASSWORD)

        password_input.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable=true][data-dl-no-input-translation=true]"))
        )

    except (TimeoutException, WebDriverException) as e:
        logging.error(f"Error during login: {e}")

    return driver

def translate_text_chunk(session, text_chunk, source_lang="EN", target_lang="RO"):
    div_selector = "div[contenteditable=true][data-dl-no-input-translation=true]"
    div_selector_ro = "div[contenteditable=true][data-dl-no-input-translation=true][lang='ro-RO']"

    try:
        div = WebDriverWait(session, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, div_selector))
        )
        # text_chunk = text_chunk.replace('\n', ' ')
        session.execute_script("arguments[0].innerText = arguments[1];", div, text_chunk)

        time.sleep(5)

        div.send_keys(Keys.RETURN)

        translation_elements = WebDriverWait(session, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"{div_selector_ro} span.--l.--r.sentence_highlight"))
        )

        translated_texts = [element.text for element in translation_elements]
        # print("Translated Texts:", translated_texts)

        return translated_texts

    except TimeoutException:
        logging.error("TimeoutException: Timed out waiting for element")
        return None

    except StaleElementReferenceException:
        logging.warning("StaleElementReferenceException: Element is no longer valid")
        return None

    except Exception as e:
        logging.error(f"Error getting translated text: {e}")
        return None


def process_file(input_file, output_file, chunk_size=10, max_retries=3):
    session = get_deepl_session()

    with open(input_file, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    translated_lines = []

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        text_chunk = ''.join(chunk)

        for retry in range(max_retries):
            translated_text = translate_text_chunk(session, text_chunk)
            if translated_text is not None:
                translated_lines.extend(translated_text)
                # logging.info("Translated text: " + str(translated_text))
                break
            else:
                continue
                # logging.warning(f"Translation failed for chunk (retry {retry + 1}): {text_chunk}")

    session.quit()

    # Handle special cases for appending lines
    modified_lines = []
    skip_next_line = False

    for idx, line in enumerate(translated_lines):
        if line.strip() == '</O>':
            if idx > 0 and modified_lines:
                modified_lines[-1] += line
            continue

        if skip_next_line:
            skip_next_line = False
            continue

        if re.match(r'^\d+\.$', line.strip()) and idx < len(translated_lines) - 1:
            next_line = translated_lines[idx + 1]
            if line.strip() != next_line.strip():
                modified_lines.append(line + next_line)
                skip_next_line = True
            continue

        modified_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        for line in modified_lines:
            output_file.write(line + '\n')


if __name__ == "__main__":
    input_file_path = "text_en.txt"
    output_file_path = "text_ro.txt"

    process_file(input_file_path, output_file_path)

    print("Translations saved to:", output_file_path)