
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os.path

#driver.get("www.google.com")
url = "https://www.cifraclub.com.br/dragon-ball-gt/sorriso-resplandecente/#instrument=keyboard"

f = url.find("/", 29)
título = url[f+1: url.find("/", f+1)]
if os.path.isfile(f"{título}.txt"):
    with open(f"{título}.txt", "r") as a:
        l = a.read()
        tom = l[0:l.find("\n")]
        cifra = l
    semAcordes = cifra
    acordes = []
    while semAcordes.count("<b>") > 0:
        i, f = semAcordes.find("<b>"), semAcordes.find("</b>")
        acordes.append(semAcordes[i+3:f])
        semAcordes = semAcordes.replace(semAcordes[i:f+4], "**")
    print(acordes)
    print(semAcordes)
else:
    print("Arquivo não encontrado, baixando cifra")
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(
        service= Service(), 
        options=options,
    )
    driver.get(url)
    tom = driver.find_elements(By.CSS_SELECTOR, '.js-modal-trigger')[3].get_attribute('text')
    cifra = driver.find_element(By.CSS_SELECTOR, 'pre').get_attribute('innerHTML')

    with open(f"{título}.txt", "w+") as a:
        a.write(tom + "\n")
        a.write(cifra)
 
#print(cifra)
"""
pesquisa = "Sorriso Resplande"
print("Carregando site...")
driver.get("https://www.cifraclub.com.br")
print("Mandando pesquisa para o elemento")
caixapesquisa = driver.find_element(By.ID, 'js-h-search')

ActionChains(driver)\
        .send_keys_to_element(caixapesquisa, pesquisa)\
        .perform()
primeirores = driver.find_elements(By.CSS_SELECTOR, '.list-suggest li a')[0]"""
