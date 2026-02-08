# 🎮 Skin Discord Bot (Minecraft)

Bot de Discord desenvolvido para **cadastro, validação e comparação de skins de Minecraft (64x64)**, com foco em evitar duplicações e identificar skins **idênticas ou semelhantes** usando análise de imagem.

Projeto pensado para uso em servidores RP / comunidades Minecraft, com controle por permissões e fluxo interativo via botões.

---

## ✨ Funcionalidades

* 📥 Cadastro de skins via comando `/register`
* 🧠 Detecção de skins **100% iguais** (hash)
* 🔍 Detecção de skins **semelhantes (≥ 85%)**
* 🧭 Fluxo interativo com botões (sim / não / cancelar)
* 🧑‍💼 Restrições por **canal configurado**
* 🔐 Comandos administrativos protegidos
* 🖼️ Armazenamento de imagens em nuvem (MonkeyBites)
* 🗄️ Banco de dados PostgreSQL (Neon)
* ⏱️ Registro de data, responsável e dados do personagem
* 🧩 Arquitetura modular e escalável

---

## 🏗️ Arquitetura do Projeto

```
skin-bot/
│
├─ bot.py
├─ requirements.txt
├─ .gitignore
│
├─ cogs/
│   ├─ register.py      # Comando /register
│   ├─ config.py        # Comando /config channel
│
├─ services/
│   ├─ image_analysis.py  # Similaridade e comparação
│   ├─ hash_utils.py      # Hash perceptual
│   ├─ image_render.py    # Render pseudo-3D (opcional)
│
├─ database/
│   ├─ connection.py     # Conexão com Neon
│   ├─ skins_repository.py
│
├─ storage/
│   └─ monkeybites.py    # Upload de imagens
│
├─ utils/
│   ├─ permissions.py    # Checagem de admin
│   └─ constants.py
│
└─ venv/ (ignorado pelo git)
```

---

## ⚙️ Tecnologias Utilizadas

* **Python 3.10+**
* **discord.py (app commands)**
* **PostgreSQL (Neon)**
* **MonkeyBites (armazenamento de imagens)**
* Pillow / OpenCV (análise de imagens)
* Hash perceptual (aHash / pHash)

---

## 📦 Requisitos

* Python 3.10 ou superior
* Conta no Discord Developer Portal
* Conta no Neon
* Conta no MonkeyBites

---

## 🚀 Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/skin-bot.git
cd skin-bot
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
DISCORD_TOKEN=seu_token_do_bot
DATABASE_URL=postgresql://user:password@host/dbname
MONKEY_API_KEY=sua_api_key
MONKEY_BUCKET=nome_do_bucket
```

⚠️ **Nunca versionar o `.env`**

---

## 🗄️ Estrutura do Banco de Dados

### Tabela `skins`

* id (PK)
* user_id (ID do jogador)
* character_name
* race
* image_url
* hash
* created_at
* created_by (ID do admin)

### Tabela `guild_config`

* guild_id (PK)
* channel_id

---

## 🧑‍💼 Comandos do Bot

### 🔧 Administrativos

#### `/config channel <canal>`

Define o canal oficial onde o bot pode ser usado.

✔ Apenas administradores

---

### 🧩 Cadastro

#### `/register`

Campos:

* imagem (PNG 64x64)
* id do usuário
* nome do personagem
* raça

Fluxo:

1. Validação da imagem
2. Geração de hash
3. Busca por skins similares
4. Fluxo interativo de confirmação
5. Salvamento final

---

## 🧠 Similaridade de Skins

* Hash perceptual para igualdade exata
* Comparação pixel a pixel
* Score de similaridade
* Threshold padrão: **85%**

Se similar:

* Exibe prévia
* Pergunta confirmação
* Permite cancelar cadastro

---

## 🖼️ Renderização (Opcional)

* Geração de boneco Minecraft pseudo-3D
* Executado **apenas quando necessário**
* Usado somente para visualização

---

## 🔒 Segurança

* Tokens protegidos por `.env`
* Comandos restritos por permissões
* Canal configurável por servidor

---

## 🧪 Ambiente de Desenvolvimento

Durante o desenvolvimento:

* Banco pode ser local (SQLite)
* Imagens podem ser salvas localmente
* MonkeyBites só é usado em produção

---

## 📈 Roadmap

* [ ] Cache de renders
* [ ] Sistema de edição de skins
* [ ] Histórico de versões
* [ ] Dashboard web

---

## 📄 Licença

Projeto privado / uso interno.
Licenciamento comercial pode ser definido futuramente.

---

## 🤝 Contribuição

Pull requests são bem-vindos.
Para mudanças maiores, abra uma issue primeiro.

---

## ❤️ Autor

Desenvolvido por **Edu GBASE**

> Projeto criado para estudo, prática e uso real em servidores Discord.
