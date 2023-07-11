# Projeto Cifra
Desenvolvido para me ajudar a aprender a pegar músicas de ouvido através do meu teclado midi.

## Códigos
### midi.py
Contém várias funções para trabalhar com conceitos de teoria musical e reconhecimento através de midi.

- **refresh()**
  - Atualiza a lista de notas pressionadas por meio do midi.

- **detecção(acorde)**
  - Reconhece a escrita dos acordes e converte em uma série de variáveis booleanas.
  ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/91712b1c-4566-4fac-94f4-dc5cd7f60c32)

(raiz, menor, sus2, sus4, qBemol, sétima, nona, decimaPrimeira)

- **calcularEscala(escala)**
  - Calcula a escala especificada e retorna suas notas.
    ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/b5391ac6-0402-4007-a98f-1e0ef4ee1950)

- **calcularCampHarm(escala, emnotas, menor)**
  - Calcula o campo harmônico especificado, pode retornar os acordes ou uma lista com suas notas.
  ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/a8ab2ca3-1120-46c1-9a72-b55a81321e0b)
  ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/5d693b73-5dd2-4f79-8021-8d481d313b07)

- **identificarAcorde()**
  - Reconhece o acorde tocado com base nas notas pressionadas.

- **tocarNotas(notasPT, oit=2, força=127, duração=1)**
  - Toca as notas especificadas no dispositivo midi.

- **toqueAcorde(acorde)**
  - Toca o acorde escolhido no teclado midi.

- **limpar(nota, mod)**
  - Limpa a baixa do acorde e as modificações (opcional).                              
  ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/4395a3f4-218c-465e-81fa-6edb83911144)
  ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/78609192-69d1-4355-8e9f-5f6d0fac199b)

- **bemol(acorde)**
  - Retorna a versão bemol do acorde sustenido.                                  
  ![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/deb21c64-007e-498e-b1e5-b4acda6ca9a6)

## main.py
Jogo em que você tem que tocar o próximo acorde da música.
De início, você deve escolher uma música já baixada ou então inserir o url do cifraclub para baixar uma nova.
![image](https://github.com/Maruquitus/ProjetoCifra/assets/58173530/e3984e1e-8aa9-412b-9a70-8434aa67def8)
