import yaml
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.ui import Select

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

driver = webdriver.Chrome()

with open('friend-profile.yml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    yaml.dump(config)

with open('css-selector.yml', 'r') as stream:
    selector = yaml.load(stream, Loader=yaml.FullLoader)
    yaml.dump_all(selector)

print("access to post page....")
driver.get('https://gamewith.jp/uma-musume/article/show/260740');
driver.implicitly_wait(20);
driver.execute_script("window.scrollTo(0, 1000);")

print("open post modal....")
gds = driver.find_element_by_tag_name("gds-uma-musume-friends")
gdsShadow = driver.execute_script('return arguments[0].shadowRoot', gds)
button = gdsShadow.find_element_by_css_selector(selector['root']['openModalButton'])
button.click()

print("input profile....")
for ganre_name, ganre_items in config.items():
    for key, value in ganre_items.items():
        
        if type(value) is str or type(value) is int:
            css_selector = selector['root'][ganre_name] + selector[ganre_name][key]
            form = gdsShadow.find_element_by_css_selector(css_selector)
            set_value(form, form.tag_name, value)
        elif type(value) is list:
            button_selector = selector['root'][ganre_name] + selector[ganre_name][key.rstrip("s") + "AddButton"]
            factor_selector = selector['root'][ganre_name] + selector[ganre_name][key]
            level_selector = selector['root'][ganre_name] + selector[ganre_name][key + "Level"]
            for i in range(len(value)-1):
                form = gdsShadow.find_element_by_css_selector(button_selector)
                form.click()
            form_factors = gdsShadow.find_elements_by_css_selector(factor_selector)
            form_levels = gdsShadow.find_elements_by_css_selector(level_selector)

            i = 0
            for factor in value:
                set_value(form_factors[i], form_factors[i].tag_name, factor['name'])
                set_value(form_levels[i], form_levels[i].tag_name, factor['level'])
                i += 1
        else:
            continue

print("post profile....")
driver.execute_script("window.scrollTo(0, 2000);")
button = gdsShadow.find_element_by_css_selector(selector['root']['postButton'])
button.click()

print("post successful!")
