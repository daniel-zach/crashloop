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
- Entre as rodadas, você escolhe upgrades e itens que alteram o comportamento da bola, dos blocos e da plataforma.  
- Quando a fase termina, um novo nível de desafio surge. Se falhar, volta ao início.

## Recursos Principais  

### Progressão roguelike  
- Cada sessão é diferente: disposição dos blocos, power-ups disponíveis e modificadores aleatórios.  
- A cada “loop” você acumula melhorias permanentes (upgrades e itens).

### Dinâmica de breakout modernizada  
- A bola e os blocos têm estatísticas e efeitos especiais.  
- Melhorias adicionam elementos completamente novos à gameplay.

### Escolhas 
- Após cada fase você escolhe entre múltiplos itens ou upgrades. É preciso balancear vantagem e risco com uma quantia limitada disponível. 

### Construção de meta-progressão  
- Você desbloqueia habilidades e melhorias permanentes conforme joga.  
- Cada nível dá acesso a mais conteúdo e permite que você vá mais longe.

## Estado Atual do Projeto  

- Sistema de upgrades funcional, incluindo 2 novos upgrades adicionados.  
- Sistema de itens randomizados, atualmente com 4 novos itens disponíveis em cada run.  
- Playlist dinâmica com músicas tocando em sequência durante as fases.  
- Sistema de combos: permite limpar fases inteiras de uma só vez, criando momentos de impacto *extremo*.
- Cores aleatórias para os elementos e background.

## Release notes
### 11/12/2025
- Adicionado cores aleatórias às telhas.
- Adicionado cor aleatória para o fundo.
- Correção do bug onde a bola fica presa na raquete.
- Agora é possível usar A-D e NUM_4-NUM-6 além das setas para controlar a raquete.

## Prints do Jogo
### Tela de Titulo
![Tela de Titulo do Crashloop](https://file.garden/aTokqyD_EwuDgkjD/Crashloop/start_menu)
### Jogo
![O segundo nível de uma rodada de Crashloop.](https://file.garden/aTokqyD_EwuDgkjD/Crashloop/lvl2)
![Um nível mais avançado de uma rodada de Crashloop](https://file.garden/aTokqyD_EwuDgkjD/Crashloop/lvl15)
![Um nível mais avançado de uma rodada de Crashloop](https://file.garden/aTokqyD_EwuDgkjD/Crashloop/combo)
### Menu de Recompensas
![Menu de recompensas](https://file.garden/aTokqyD_EwuDgkjD/Crashloop/reward_screen)
---
<br>Universidade Federal Rural de Pernambuco 
<br>Bacharelado em Sistemas de Informação
<br>Desenvolvido para a disciplina de Principios de programação.

**Criado por:** [Daniel Zacheu](https://github.com/daniel-zach) e [João Pedro Leite](https://github.com/johnpleite)

**Sob orientação de:** [Cleyton Magalhaes](https://github.com/cvanut)

**Licença:** Este projeto está sob a licença [MIT](LICENSE).
