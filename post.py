import yaml
import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def set_value(form, tag, value):
    if(tag) == 'input' or 'textarea':
        form.send_keys(value)
    elif(tag) == 'select':
        form = Select(form)
        form.select_by_visible_text(value)
    elif(tag) == 'button':
        form.click()
    else:
        print("error")
    time.sleep(0.3)

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

with open('friend-profile.yml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    yaml.dump(config)

with open('css-selector.yml', 'r') as stream:
    selector = yaml.load(stream, Loader=yaml.FullLoader)
    yaml.dump_all(selector)

print("access to post page....")
driver.get('https://gamewith.jp/uma-musume/article/show/260740');
driver.implicitly_wait(20);
# driver.execute_script("window.scrollTo(0, 1000);")

print("close ads....")
driver.find_element(By.CSS_SELECTOR, selector['root']['adCloseButton']).click()

print("open post modal....")
gds_shadow = driver.find_element(By.TAG_NAME, "gds-umamusume-friends-list").shadow_root
button = gds_shadow.find_element(By.CSS_SELECTOR, selector['root']['openModalButton'])
button.click()

print("input profile....")
for ganre_name, ganre_items in config.items():
    for key, value in ganre_items.items():
        
        if type(value) is str or type(value) is int:
            css_selector = selector['root'][ganre_name] + selector[ganre_name][key]
            form = gds_shadow.find_element(By.CSS_SELECTOR, css_selector)
            set_value(form, form.tag_name, value)
        elif type(value) is list:
            button_selector = selector['root'][ganre_name] + selector[ganre_name][key.rstrip("s") + "AddButton"]
            factor_selector = selector['root'][ganre_name] + selector[ganre_name][key]
            level_selector = selector['root'][ganre_name] + selector[ganre_name][key + "Level"]
            for i in range(len(value)-1):
                form = gds_shadow.find_element(By.CSS_SELECTOR, button_selector)
                form.click()
                time.sleep(0.3)
            form_factors = gds_shadow.find_elements(By.CSS_SELECTOR, factor_selector)
            form_levels = gds_shadow.find_elements(By.CSS_SELECTOR, level_selector)

            i = 0
            for factor in value:
                set_value(form_factors[i], form_factors[i].tag_name, factor['name'])
                set_value(form_levels[i], form_levels[i].tag_name, factor['level'])
                i += 1
        else:
            continue

print("post profile....")
driver.execute_script("window.scrollTo(0, 2000);")
button = gds_shadow.find_element(By.CSS_SELECTOR, selector['root']['postButton'])
button.click()

print("post successful!")
time.sleep(5)
driver.execute_script("window.scrollTo(0, 300);")
time.sleep(5)
post_card = gds_shadow.find_element(By.CSS_SELECTOR, selector['root']['postCard'])
screenshot = post_card.screenshot_as_base64

print("write image to artifact...")
file_base64 = './screenshot.base64'
with open(file_base64, mode='w') as f:
    f.write(screenshot)

print("all steps was done!")
