# Bot Ancap

um bot para o discord que simula uma economia anarco capitalista ficticia, esta sendo criado para um experimento em um servidor

## Instalação

instale o `requirements.txt`

```shell
pip install -r requirements.txt
```

se o pip nao estiver no path do seu sistema use `python -m` ou `python3 -m`

crie um banco de dados postgresql com o `users.sql` e use o `config-template.ini` e crie um `config.ini` com os dados requeridos para o bot funcionar.

## comandos

```
Adm:
  demote    tira o cargo de moderador
  mod       contrata polícia privada(moderadores) pro seu canal
  mute      Impede um usuário de falar no seu canal (use * para usar em @everyone)
  unmute    Impede um usuário de falar no seu canal (use * para usar em @everyone)
Basics:
  info      Informações sobre o bot
  math      
  ping      Calcula a latência do bot
Economy:
  canal     Compra um canal só seu
  init      Cria sua conta
  saldo     Mostra seu saldo
  trabalhar Ganha dinheiro (pode ser usado de 1 em 1 minuto)
  trans     da dinheiro ao seu amiguinho
Gambling:
  bicho     Resultados do jogo do bicho
  d20       Rola um dado de 20 lados, 20x a aposta caso ganhe
  dado      Rola um dado, 6x a aposta caso ganhe
  moeda     Joga uma moeda, 2x a aposta caso ganhe
```

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
