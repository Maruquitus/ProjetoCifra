
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
import os
import midi
from colorama import init
init()
from colorama import Fore, Back, Style
clear = lambda: os.system('cls')


músicas = []

for root, dirs, files in os.walk("Cifras/", topdown=False):
   for name in files:
      if name[-4::] == ".txt":
        músicas.append(name.replace(".txt", ""))


def load(tít):
    global acordes, semAcordes, cifra, tom, título
    with open(f"Cifras/{tít}.txt", "r") as a:
        l = a.read()
        título = l[0:l.find("\n")]
        l = l.replace(título, "")
        tom = l[0:l.find("\n")]
        cifra = l
    semAcordes = cifra
    acordes = []
    while semAcordes.count("<b>") > 0:
        i, f = semAcordes.find("<b>"), semAcordes.find("</b>")
        acordes.append(semAcordes[i+3:f])
        semAcordes = semAcordes.replace(semAcordes[i:f+4], "**", 1)

def download(url):
    url = url + "#tabs=false&instrument=keyboard"
    options = Options()
    options.add_experimental_option(
"prefs", {"profile.managed_default_content_settings.images": 2}
)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--headless")
    options.add_argument("--window-size=%s" % "1366,768")
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(
        service= Service(), 
        options=options,
    )
    print(f"{Fore.LIGHTGREEN_EX}Baixando cifra...")
    print(f"{Fore.LIGHTWHITE_EX} * Conectando a www.cifraclub.com.br...")
    driver.get(url)
    print(f"{Fore.LIGHTBLUE_EX}Salvando...")
    ti = driver.find_element(By.CSS_SELECTOR, '.t1').get_attribute('textContent')
    tom = driver.find_elements(By.CSS_SELECTOR, '.js-modal-trigger')[3].get_attribute('text')
    cifra = driver.find_element(By.CSS_SELECTOR, 'pre').get_attribute('innerHTML')
    f = url.find("/", 29)
    título = url[f+1: url.find("/", f+1)]

    if not os.path.exists('Cifras'):
        os.makedirs('Cifras')

    with open(f"Cifras/{título}.txt", "w+") as a:
        a.write(ti + "\n")
        a.write(tom + "\n")
        a.write(cifra)
    load(título)

qnt = len(músicas)

if qnt > 0:
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Foram encontradas {Fore.LIGHTMAGENTA_EX}{qnt} {Fore.LIGHTGREEN_EX}músicas no diretório atual, selecione a que deseja tocar.{Fore.RESET}")
    for m in range(qnt):
        print(f"{Fore.LIGHTMAGENTA_EX}{m+1}. {Fore.CYAN} {músicas[m]}")
    print(f"{Fore.LIGHTMAGENTA_EX}{m+2}. {Fore.YELLOW} Baixar cifra")
    e = input(f"{Fore.BLUE}Digite um número: {Fore.LIGHTMAGENTA_EX}")
    if int(e) != m+2:
        load(músicas[int(e)-1])
    else:
        e = input(f"{Fore.LIGHTYELLOW_EX}Insira o URL da cifra para baixar: {Fore.LIGHTMAGENTA_EX}")
        download(e)
else:
    print(f"{Fore.LIGHTRED_EX}Nenhuma cifra encontrada na pasta")
    e = input(f"{Fore.LIGHTYELLOW_EX}Insira o URL da cifra para baixar: {Fore.LIGHTMAGENTA_EX}")
    download(e)

ultAC = 0

linhas = []
lAcorde = 0
def scroll(c, linha):
    global ultAC
    global lAcorde, linhas

    linhas = []
    lAcorde = 0
    i = 0
    f = 0
    a = 0
    while f != -1:
        f = c.find("\n", i)
        if f != -1:
            linhas.append(f)
        i = f+1

    a = c.find("**")
    if a != -1:
        lAcorde = a

    for l in range(linha, len(linhas)):
        if l+1 < len(linhas):
            if lAcorde >= linhas[l] and lAcorde < linhas[l+1]:
                lAcorde = l
                break
        else:
            lAcorde = l

    i = 0
    
    if linha+17 >= len(linhas):
        res = c[linhas[-18]:linhas[-1]]
    else:
        res = c[linhas[linha]:linhas[linha+17]]
    
    return res

cifra = semAcordes.replace("**", f"{Fore.LIGHTBLACK_EX}**{Fore.RESET}")
indAcorde = 0
acordeAtual = acordes[0] 
antigaC = ""
cifra = cifra.replace('\n', '', 1)
tom = cifra[0:cifra.find("\n")]
cifra = cifra[1::]

clear()
print(f"""\r{Style.BRIGHT}{Fore.CYAN}{título}{Fore.RESET}{Style.NORMAL}
Tom:{Fore.LIGHTMAGENTA_EX}{tom}{Fore.LIGHTBLACK_EX}
|--------------------------|{Fore.RESET}
{scroll(cifra, 0)}
{Fore.LIGHTBLACK_EX}|--------------------------|{Fore.RESET}
Acorde tocado: {Fore.BLUE}**""")
antigaC = cifra

aAntigo = ""

linhaAtual = 0
primeiravez = True

#Joguinho
while True:
    try:
        if lAcorde-10 > linhaAtual:
            linhaAtual = lAcorde-10
    except:
        linhaAtual += 1
    acordeTocado = midi.identificarAcorde()
    pos = [acordeTocado, midi.bemol(acordeTocado)]
    if indAcorde >= len(acordes):
        pos = []
        acordeAtual = ''
    offset = int(indAcorde+1 < len(acordes))
    acertou = 0
    for p in pos:
        if midi.limpar(p, 1) == midi.limpar(acordeAtual, 1):
            acertou += 2
        if midi.limpar(p, 1) == midi.limpar(acordes[indAcorde-1], 1) or midi.limpar(p, 1) == midi.limpar(acordes[indAcorde+offset], 1):
            acertou += 0.5
    if acertou >= 2:
        try:
            indAcorde += 1
            cifra = cifra.replace("**", f"{Fore.LIGHTMAGENTA_EX}{acordeAtual}{Fore.RESET} ", 1)
            acordeAtual = acordes[indAcorde]
        except:
            acordeAtual = ''
            
    if acertou == 0:
        cifra = cifra.replace("**", f"{Fore.LIGHTYELLOW_EX}**{Fore.RESET} ", 1)

    if cifra != antigaC or acordeTocado != aAntigo or primeiravez:
        primeiravez = False
        i = False
        clear()
        
        print(f"""\r{Style.BRIGHT}{Fore.CYAN}{título}{Fore.RESET}{Style.NORMAL}
Tom:{Fore.LIGHTMAGENTA_EX}{tom}{Fore.LIGHTBLACK_EX}
|--------------------------|{Fore.RESET}
{scroll(cifra, int(linhaAtual))}
{Fore.LIGHTBLACK_EX}|--------------------------|{Fore.RESET}
Acorde tocado: {Fore.BLUE}{acordeTocado}""")
        antigaC = cifra
        aAntigo = acordeTocado
