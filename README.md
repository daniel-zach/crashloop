# Crashloop

## Visão Geral  
“Crashloop” é uma reinvenção do clássico “breakout” com um toque roguelike: você controla uma plataforma e rebate uma bola para quebrar blocos, mas a cada fase a estrutura muda, os poderes evoluem e o risco cresce.

## Dependências
### Pygame

    python3 -m pip install pygame

### Numpy

    python3 -m pip install numpy

## Mecânica Básica  
- Rebata a bola para destruir blocos e avançar fases.  
- A cada nova rodada, a disposição dos blocos, os efeitos e os desafios mudam.  
- Entre as rodadas, você escolhe upgrades, modificadores e habilidades que alteram o comportamento da bola, dos blocos e da plataforma.  
- Quando a fase termina, um novo nível de desafio surge. Se falhar, volta ao início ou a um checkpoint, dependendo do modo.

## Recursos Principais  

### Progressão roguelike  
- Cada sessão é diferente: disposição dos blocos, power-ups disponíveis e modificadores aleatórios.  
- A cada “loop” você acumula melhorias permanentes (por exemplo habilidades desbloqueadas) e escolhas temporárias para a próxima fase.

### Dinâmica de breakout modernizada  
- A bola e os blocos têm estatísticas ou efeitos especiais: blocos que regeneram, bolas que mudam de comportamento, blocos que rebatem contra você, etc.  
- A plataforma pode ser melhorada.

### Escolhas e riscos  
- Após cada fase você escolhe entre múltiplos power-ups ou modificadores. Balanceando vantagem e risco. 
- Há modos de “loop” mais difícil onde os blocos têm efeitos deletérios ou comportamentos imprevisíveis.

### Construção de meta-progressão  
- Você desbloqueia habilidades, melhorias permanentes e novos tipos de bola/plataforma conforme joga.  
- Cada volta bem-sucedida dá acesso a mais conteúdo e permite que você vá mais longe no próximo loop.

## Estado Atual do Projeto  

Versão inicial com as mecânicas básicas: 
- Vida dos blocos.  
- Sistema de power-ups/upgrade.  
- Loop de meta-progressão. 

## Prints do Jogo
### Tela de Titulo
![Tela de Titulo do Crashloop](https://file.garden/aTHbGAX8eEY4Irux/Crashloop/screencap0.png)
### Jogo
![O primeiro nível de uma rodada de Crashloop.](https://file.garden/aTHbGAX8eEY4Irux/Crashloop/screencap1.png)
![Um nível mais avançado de uma rodada de Crashloop](https://file.garden/aTHbGAX8eEY4Irux/Crashloop/screencap2.png)
---
<br>Universidade Federal Rural de Pernambuco 
<br>Bacharelado em Sistemas de Informação
<br>Desenvolvido para a disciplina de Principios de programação.

**Criado por:** [Daniel Zacheu](https://github.com/daniel-zach) e [João Pedro Leite](https://github.com/johnpleite)

**Sob orientação de:** [Cleyton Magalhaes](https://github.com/cvanut)

**Licença:** Este projeto está sob a licença [MIT](LICENSE).
