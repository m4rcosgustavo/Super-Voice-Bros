## Documentação do Projeto: Super Voice Bros
### 1. Visão Geral

**Tecnologias Utilizadas:** Python + Pygame + Reconhecimento de Voz

**Descrição:**
Super Voice Bros é um jogo de plataforma 2D no estilo clássico de Mario Bros, com um diferencial inovador: o jogador controla o personagem utilizando comandos de voz. O objetivo é atravessar mundos perigosos e cheios de inimigos usando apenas a voz, exigindo clareza e precisão nos comandos falados.

---

### 2. Descrição Detalhada do Projeto

### Referência Criativa
Super Voice Bros é um jogo de plataforma fortemente inspirado no clássico Super Mario Bros, cuja criatividade, estilo visual e mecânicas marcaram profundamente a história dos videogames. Nosso projeto surge como uma homenagem a esse ícone, trazendo elementos similares — como a progressão por fases, os desafios com obstáculos e inimigos, e o estilo visual retrô —, mas com uma proposta inovadora: o controle por voz.

Neste jogo, o jogador realiza ações como correr, pular e interagir com o ambiente por meio de comandos vocais, o que proporciona uma experiência interativa única e desafiadora. Super Voice Bros busca unir a nostalgia dos jogos clássicos com a inovação tecnológica atual, oferecendo uma releitura moderna de uma fórmula consagrada.

### Acessibilidade e Inclusão
Super Voice Bros não é apenas uma releitura moderna de um clássico; ele também representa um avanço em acessibilidade nos jogos eletrônicos. O controle por voz pode beneficiar jogadores com limitações motoras, além de tornar a experiência mais inclusiva e interativa. O jogo busca se adaptar a diferentes tons de voz e ambientes, proporcionando jogabilidade estável para uma ampla gama de usuários.

### O que é o Super Voice Bros?

Super Voice Bros é um jogo de plataforma onde o personagem é controlado unicamente pela voz. Utilizando bibliotecas de reconhecimento de fala, o jogo responde a comandos vocais como "pular", "correr", "parar" e outros, oferecendo uma experiência imersiva e acessível.
#### 2.1 Funcionalidades Principais

* **Comandos de voz para controle total:**
  * “Pular” – salto simples
  * “Correr” – acelera o personagem
  * “Agachar” – abaixa o personagem
  * “Parar” – congela o personagem
  * “Super salto” – salto maior e mais longo
  * “Ataque” – ataque giratório contra inimigos
    
* **Tecnologia de reconhecimento de voz ajustável**
  * Reconhecimento por entonação (ex: gritar = salto maior)
  * Configurações sensíveis para diferentes ambientes
    
* **Desafios por fase:**
  * Obstáculos, inimigos e plataformas móveis
  * Detecção de comandos rápidos e claros
  * Fases com níveis de dificuldade progressivos

### 2.2 Personagens sugeridos
Os personagens de Super Voice Bros foram criados com base em arquétipos clássicos de jogos de plataforma, especialmente do universo Super Mario Bros, mas adaptados à proposta vocal do jogo. Cada personagem tem um nome marcante, fácil de lembrar e relacionado ao conceito de som, fala ou interferência. A seguir, apresentamos os personagens principais:

**Voko – O Herói**
 * Função: Protagonista controlado por comandos de voz
 * Inspiração: Mario
 * Design sugerido:
 * Corpo simples (retângulo ou oval)
 * Cabeça com boné e fone de ouvido
 * Olhos e boca expressivos
 * Paleta: vermelho, azul e branco

**Glitchy – Inimigo Comum**
 * Função: Obstáculo básico nas fases
 * Inspiração: Goomba
 * Design sugerido:
 * Forma: quadrado ou retângulo distorcido
 * Textura: efeito de “pixels quebrados” ou estática
 * Cores: cinza, preto e vermelho
 * Animação: tremores ou piscada

**Buzzik – Inimigo Voador**
 * Função: Inimigo aéreo que interfere com comandos
 * Inspiração: Koopa voador
 * Design sugerido:
 * Forma: oval com asas triangulares
 * Detalhes: linhas de som saindo da boca
 * Cores: amarelo, laranja e branco
 * Movimento: voa em padrão de onda
  

**Mutez – Vilão Principal**
 * Função: Chefe final que tenta silenciar todos os mundos
 * Inspiração: Bowser
 * Design sugerido:
 * Corpo: grande retângulo ou quadrado com expressão intimidadora
 * Boca: símbolo de "mute" (um X ou risco sobre os lábios)
 * Cores: preto, roxo escuro, vermelho
 * Animação: pode lançar “ondas de silêncio” (efeitos visuais simples)
   
_**Importante: Mutez aparece na fase bônus final do jogo, tornando essa fase o grande desafio final. A fase bônus é o "chefão" oculto do jogo: complexa, imprevisível e repleta de obstáculos sonoros que testam tudo o que o jogador aprendeu. Ela representa o verdadeiro clímax da jornada vocal.**_
   
#### 2.3 Arquitetura do Código

```plaintext
super_voice_bros/
│
├── main.py               # Arquivo principal
├── voice_control.py      # Padrões de reconhecimento de voz
├── player.py             # Lógica do personagem e movimentos
├── enemies.py            # Gerenciamento dos inimigos
├── levels/               # Estrutura e dados das fases
├── assets/               # Imagens, sons e fontes
│   ├── images/
│   ├── sounds/
│   └── fonts/
└── utils.py              # Funções auxiliares e ferramentas
```

---

### 3. Etapas de Entrega (Cronograma Detalhado)

#### Etapa 1: Protótipo Básico (Semanas 1-2)

* Configuração do ambiente Pygame + reconhecimento de voz
* Implementação do personagem e comandos básicos
* Criação de uma fase de teste simples
  
#### Etapa 2: Lógica do Jogo (Semanas 3-4)
* Adição de obstáculos, inimigos e colisões
* Lógica de entonação vocal (saltos com intensidade)
* Sistema de detecção de comandos simultâneos
  
#### Etapa 3: Polimento (Semana 5)
* Melhorias nos gráficos e sons
* Ajustes na sensibilidade de voz
* Fases com aumento de dificuldade

---
  
#### Etapa 4: Testes e Entrega Final (Semana 6)
* Correção de bugs
* Testes com diferentes microfones e ambientes
* Geração dos arquivos finais do projeto
### 4. Requisitos Técnicos
#### 4.1 Exemplo de dependências (`requirements.txt`)

```txt
pygame==2.5.2
SpeechRecognition==3.10.0
pyaudio==0.2.13
```
