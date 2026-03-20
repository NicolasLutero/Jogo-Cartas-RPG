# Cartinhas RPG – Plataforma de Cartas Digitais Estratégicas

## 📖 Visão Geral

**Cartas de RPG** é uma plataforma web de cartas digitais com temática de RPG que combina **colecionismo, progressão diária e decisões estratégicas**.

A versão atual do sistema contempla exclusivamente a **administração de cartas**, incluindo geração, evolução e controle de ações diárias.  
**Não há sistema de partidas, combate ou modo jogável nesta versão.**

O objetivo desta etapa é consolidar regras de domínio, persistência e organização arquitetural antes da implementação de mecânicas de jogo.

[Galeria de Fotos do Gerador de Cartinhas](https://drive.google.com/drive/folders/1PvTlhDMctvWQEE73xk7idqshj2U1Vygx?usp=sharing)

---

## 🎯 Objetivo do Projeto

- Permitir que cada jogador possua e administre sua própria coleção.
- Controlar progressão por meio de ações limitadas diariamente.
- Garantir regras claras, determinísticas e testáveis.
- Manter uma arquitetura organizada e escalável.

---

## 👥 Público-Alvo

- Jogadores de RPG.
- Colecionadores digitais.
- Usuários que apreciam progressão controlada.
- Desenvolvedores interessados em organização arquitetural aplicada a jogos.

---

## 🃏 Estrutura das Cartas

Cada carta possui:

### 🔹 Classe
- Mago
- Arqueiro
- Guerreiro

### 🔹 Cenário
- Planície
- Floresta
- Montanha

### 🔹 Raridade Visual
- Comum
- Bom
- Ótimo
- Top
- Perfeito

### 🔹 Atributos (Inspirados em D&D)

- Constituição  
- Força  
- Destreza  
- Inteligência  
- Sabedoria  
- Carisma  

---

## ⚙️ Funcionalidades Implementadas

### ✅ Sistema de Usuários
- Cadastro
- Login
- Controle de sessão
- Persistência individual de coleção

### ✅ Geração Inicial
- Cada usuário recebe 45 cartas ao criar conta.

### ✅ Cartas Diárias
- 5 novas cartas únicas por dia.
- Controle de disponibilidade diária.

### ✅ Reforjar
- Combina duas cartas semelhantes.
- Gera uma nova carta com os melhores atributos entre ambas.
- Limitado a 1 vez por dia.

### ✅ Fundir
- Combina duas cartas diferentes.
- Produz uma carta de raridade superior.
- Redistribui atributos de forma otimizada.
- Limitado a 1 vez por dia.

---

## 🏗 Arquitetura

O projeto utiliza **Python com Flask**, estruturado segundo princípios de organização em camadas:

- **Presentation** – Blueprints separados (Site, Login/Cadastro, Mecânicas).
- **Application** – Casos de uso que orquestram regras de negócio.
- **Domain** – Entidades centrais e regras de evolução.
- **Infra** – Persistência e integração com banco de dados.

Essa separação facilita manutenção, testes e futura expansão.

---

## 🛠 Tecnologias

- **Back-end:** Python + Flask
- **Banco de Dados:** PostgreSQL
- **Front-end:** HTML, CSS, JavaScript

---

## 📌 Estado Atual

A aplicação está funcional como **plataforma de administração e evolução de cartas**.  
Ainda não existe sistema de combate ou modo jogável.

---

## OBS: Configuração do Banco de Dados

Este projeto requer um banco PostgreSQL com as seguintes credenciais padrão:

- Banco: GeradorCartasRPG
- Usuário: GenCartas
- Senha: SenhaGenCartas

1. Crie o banco:
   CREATE DATABASE GeradorCartasRPG;

2. Crie o usuário:
   CREATE USER GenCartas WITH PASSWORD 'SenhaGenCartas';

3. Conceda permissões:
   GRANT ALL PRIVILEGES ON DATABASE GeradorCartasRPG TO GenCartas;
