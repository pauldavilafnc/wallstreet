# WALL STREET no GitHub Pages — notícias que se atualizam sozinhas

Com este pacote, o site fica num endereço próprio (`https://SEU-USUARIO.github.io/wallstreet/`) e o GitHub
busca as notícias sozinho a cada 3 horas, de graça. Você só faz isso uma vez.

## Arquivos
| Arquivo | Para quê |
|---|---|
| `index.html` | O site WALL STREET (já lê o `noticias.json`) |
| `manifest.webmanifest`, `sw.js` | Fazem o site ser instalável como app e abrir sem internet |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png` | Ícone do app / atalho na tela inicial |
| `noticias.json` | Notícias (começa com a coleta de 05/11/2026; depois o robô atualiza) |
| `scripts/atualizar_noticias.py` | Busca os feeds RSS e gera o `noticias.json` |
| `.github/workflows/noticias.yml` | Manda o GitHub rodar o script a cada 3 horas |

## ⚠️ ANTES de começar: faça backup
Os dados do WALL STREET ficam guardados **por endereço**. Ao abrir o site no endereço novo, ele começa vazio.
1. No site atual: **Ajustes → Exportar backup** e guarde o arquivo.
2. No site novo: **Ajustes → Importar backup**.

## Passo a passo (pode ser feito pelo navegador do celular; no Chrome, ative "Site para computador" se precisar)
1. Crie uma conta em github.com e toque em **New repository**. Nome: `wallstreet`. Marque **Public**. Toque em **Create repository**.
   (Público é necessário para o Pages gratuito; só o `index.html` e as notícias ficam visíveis — seus dados financeiros ficam apenas no seu aparelho.)
2. Em **Add file → Upload files**, envie `index.html` e `noticias.json`. Toque em **Commit changes**.
3. **Add file → Create new file**. No nome, digite exatamente `scripts/atualizar_noticias.py` (a barra cria a pasta).
   Cole o conteúdo do arquivo `atualizar_noticias.py` e toque em **Commit changes**.
4. **Add file → Create new file**. No nome, digite exatamente `.github/workflows/noticias.yml`.
   Cole o conteúdo do arquivo `noticias.yml` e toque em **Commit changes**.
5. **Settings → Pages**. Em *Build and deployment*, escolha **Deploy from a branch**, branch **main**, pasta **/ (root)**. **Save**.
6. Aba **Actions → Atualizar notícias → Run workflow** para rodar a primeira vez agora.
   (Se aparecer um botão pedindo para habilitar os workflows, aceite.)
7. Espere 1–2 minutos e abra `https://SEU-USUARIO.github.io/wallstreet/`. Em **Notícias** deve aparecer
   "Atualizadas automaticamente em dd/mm/aaaa às hh:mm".

## Como saber se está funcionando
- Aba **Actions**: cada execução verde = deu certo. Abra uma execução para ver o log (`ok Agência Brasil: 10 itens`, etc.).
- Linhas `FALHOU <fonte>` no log significam que **aquele** feed não respondeu ou mudou de endereço. Os outros continuam; o site nunca
  mostra notícia inventada. Se todos falharem, o `noticias.json` não é alterado e o site passa a avisar que está desatualizado.
- Se um endereço de feed mudou, edite a lista `FEEDS` no começo de `scripts/atualizar_noticias.py`.

## O que o site faz
- Abre o `noticias.json` do próprio site (sem chave de API, sem servidor seu).
- Guarda a última versão boa no aparelho: sem internet, mostra essa versão e avisa a data/hora real dela.
- Se a atualização tiver mais de 12 h, avisa que pode estar desatualizada. Se o arquivo vier quebrado ou com link não-https, ignora e avisa.

## Limites que você precisa saber
- **Fontes:** o script usa RSS de Agência Brasil, G1, InfoMoney, Banco Central e BBC News Brasil. **Reuters e Valor Econômico não
  oferecem RSS aberto**, então não entram. Os endereços dos feeds eu não consegui testar de dentro do meu ambiente (sem internet):
  o primeiro log do GitHub mostra quais funcionam.
- **Resumos:** são os que as próprias fontes publicam no feed (cortados em ~230 caracteres), com link para a matéria original.
- **Mundo:** BBC e G1 Mundo são filtrados por palavras de economia (juros, bolsa, dólar, Fed, inflação…), então pode haver dias com poucas notícias.
- **Pausa do GitHub:** o GitHub pode pausar tarefas agendadas após ~60 dias sem atividade no repositório. Se isso acontecer,
  é só entrar em Actions e tocar em *Run workflow* / reativar.
- **Atraso:** a atualização roda de 3 em 3 horas, então o site pode estar até ~3 h atrás da fonte.

## Ícone na tela inicial / instalar como app
Envie para o repositório (Add file → Upload files, na raiz, junto do `index.html`): `index.html`, `manifest.webmanifest`, `sw.js`,
`icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`. Depois de ~1–2 min, abra o site, feche e abra de novo e,
no menu ⋮ do navegador, escolha **Instalar app** (ou **Adicionar à tela inicial**). Se já tinha um atalho antigo com a letra "G", apague-o e crie outro.
Depois de instalado, o app abre em tela cheia e, sem internet, abre com a última versão guardada.

## Segurança (usuário e senha)
- Na primeira abertura aparece "Proteger o WALL STREET": crie usuário e senha. Os dados passam a ficar **criptografados (AES-256)** no aparelho e só abrem com a senha.
- O app mostra **um código de recuperação** (20 caracteres) **uma única vez**. Anote em papel ou guarde fora do celular. É a única forma de recuperar o acesso se esquecer a senha. **Não há recuperação por e-mail** (o site não tem servidor).
- Esqueceu a senha? Na tela de login toque em "Esqueceu a senha?", digite o código e crie uma nova senha (um novo código é gerado).
- Perdeu a senha **e** o código? Os dados não podem ser abertos por ninguém. Só o backup (arquivo exportado em Ajustes) salva. **Backups exportados não são criptografados** — guarde em local seguro.
- Ajustes → Segurança: bloquear agora, bloqueio automático (1, 5 ou 15 min fora do app, ou só ao fechar), alterar senha, gerar novo código, remover proteção.
- Para atualizar o site basta substituir o `index.html` no GitHub; os dados e a senha ficam no aparelho e não são afetados.

## Gastos por categoria e backup criptografado
- **Relatórios → Gastos por categoria:** barras por categoria no mês (escura = já pago, clara = previsto, traço = limite). Toque numa categoria para definir o limite mensal. Avisos: "Perto do limite" (80% do limite pago), "Vai passar do limite" (pago + a pagar ultrapassa) e "Passou do limite". Os avisos aparecem também na central de notificações e nas falas do mascote.
- **Ajustes → Exportar backup criptografado:** gera um arquivo que só abre com a senha que você escolher (diferente da senha de login). Importar funciona pelo mesmo botão "Importar backup". Sem a senha do backup ninguém recupera o arquivo.

## Lembrete semanal de backup
O app guarda a data do último backup exportado (comum ou criptografado). Depois de 7 dias sem backup, avisa na central de notificações, na fala do mascote e em Ajustes → Backup. Dá para mudar para "a cada 2 semanas" ou desligar em Ajustes → Backup → Lembrete de backup. Importar um backup também zera a contagem.

## Zerar dados, app em branco e lembretes
- **Ajustes → Zerar todos os dados:** apaga lançamentos, dívidas, parcelas, caixinhas e limites e deixa o app em branco (é preciso digitar ZERAR). Nome, tema, avatar e senha continuam.
- **O app agora abre em branco** em um aparelho novo (nenhum dado pessoal vem no código). Para trazer seus dados, use Ajustes → Importar backup.
- **Lembrete de backup:** todos os dias, toda semana, a cada 15 dias, todo mês ou desligado.

## Primeira abertura (boas-vindas)
Quem abre o link pela primeira vez vê a tela de boas-vindas: **Criar minha conta** (pergunta o nome, depois usuário e senha, com código de recuperação), **Já tenho uma conta** (importar um backup, comum ou criptografado) ou **Usar sem senha por enquanto**. A "conta" fica só no aparelho: para usar em outro aparelho, é preciso importar o backup.

## Minha situação financeira e Sobre
- **Relatórios → Minha situação financeira:** avalia a saúde financeira (Saudável, Estável, Atenção ou Crítica) com regras claras, usando receitas, despesas, saldo disponível, dívidas, parcelas e atrasos do mês. Mostra o porquê, o que está bem e o que fazer. É orientativa.
- **Ajustes → Sobre:** nome, slogan, criador, finalidade, avisos importantes e direitos autorais.

## Identidade visual (Minimal Glass + lobo)
Visual de vidro fosco nos temas claro e escuro, com o lobo como mascote e símbolo. Em Ajustes → Aparência há o "Efeito de vidro" (Completo ou Leve, mais rápido). Os ícones do app (icon-192.png, icon-512.png, icon-maskable-512.png, apple-touch-icon.png) foram renovados: envie os quatro junto com o index.html.

## Avatar de lobo e calculadora
O avatar agora é um lobo: 7 expressões, acessórios de cabeça (boné, cartola, coroa, gorro, fones) e de rosto (óculos escuros, óculos redondos, tapa-olho, cicatriz), 5 pelagens e 9 cores de fundo (Ajustes → Avatar). O botão flutuante da calculadora usa um ícone simples de calculadora. A voz da assistente foi removida.

## Central de Jogos (etapa 1)
Acesso pelo card "Central de Jogos" na Home. Jogos: Quiz financeiro, Verdadeiro ou falso, Desafio matemático e Decisão financeira (cada rodada tem 4 a 6 perguntas, com explicação a cada resposta). Há XP e níveis, moedas virtuais, desafios diários com baú, sequência de dias com bônus, 14 medalhas e dificuldade que se ajusta ao desempenho. Tudo é virtual (sem dinheiro real) e fica salvo junto com os seus dados (entra no backup). O "Sobreviva ao Mês" (simulador de 4 semanas com salário fictício) já está incluído; a Loja de recompensas (Central de Jogos → Loja) troca moedas virtuais por acessórios, pelagens e fundos novos do lobo e por 3 temas visuais (Ouro, Rosé e Grafite). Itens com cadeado também aparecem no editor de avatar e em Ajustes → Aparência.

## Mascote principal (Lobo 2D)
O mascote é o lobo ilustrado de terno branco, colete, gravata preta e relógio (a imagem de referência), embutido no app como 6 camadas WebP leves (corpo, cabeça, 2 orelhas, 2 olhos; ~43 KB no total). Aparece nas boas-vindas, no login, nas telas com senha e na dica da Home. Animações só com CSS: balanço sutil da cabeça, piscar, orelhas e olhar. Em todas as telas de bloqueio (boas-vindas, nome, login e senha) aparece o mesmo lobo: com a senha oculta ele fecha os olhos, e ao preencher usuário, nome ou senha visível ele olha para baixo. Os 10 avatares continuam independentes.

## Telas de bloqueio (boas-vindas e login)
Têm um botão de sol/lua no canto superior direito para alternar claro/escuro (a escolha fica salva). Dentro do app, o tema só muda em Ajustes. O olho da senha tem design de vidro, fecha com a senha oculta e, aberto, a pupila olha de um lado para o outro. Os 10 avatares são personagens 2D ilustrados (lobo, urso polar, pantera, tigre, raposa, lince, sapo, rinoceronte, coruja e touro).

## Anotações (no lugar da Central de Jogos)
O app não tem mais jogos, moedas, XP nem loja: todos os temas e paletas são livres. No lugar, a seção **Anotações** reúne três ferramentas, tudo salvo só no aparelho (e criptografado quando há senha): **Notas** (título e descrição, salvas automaticamente), **Lembretes** (data e horário, aviso do navegador quando permitido, concluir ou excluir, integrados ao sino de notificações) e **Tarefas** (listas personalizadas com itens marcáveis). Os avisos tocam enquanto o app está aberto; com o app fechado, o navegador não garante o aviso, e os lembretes vencidos aparecem no sino ao abrir.

## Avatares (10 ilustrações no mesmo estilo)
Os 10 avatares são ilustrações no estilo do lobo Alfa, recortadas e otimizadas (WebP, ~10 KB cada, embutidas no app): Alfa (lobo), Ártico (urso polar), Sombra (gato preto), Raio (tigre), Ruivo (raposa), Safira (lobo azul), Esmeralda (sapo), Cobre (cavalo), Névoa (coruja) e Samurai (panda vermelho). Todos no mesmo círculo azul-escuro, com o mesmo enquadramento.

## Versão 4.1: cartões, atalhos, aviso de versão e lembretes na agenda
- **Cartões de crédito** (Despesas → Cartões de crédito): nome, limite, dia de fechamento e vencimento; compras com parcelas; fatura por mês (aberta, fechada, atrasada ou paga); limite disponível. Só o pagamento da fatura entra no saldo. Há avisos de fatura perto do vencimento ou atrasada, e o card aparece na Home.
- **Atalhos do ícone** (segurar o ícone do app instalado): Nova despesa, Nova receita e Anotações (definidos em `manifest.webmanifest`).
- **Aviso de nova versão:** o app compara a versão (BUILD) do site publicado com a do aparelho e oferece "Atualizar agora" (os dados não são apagados). Para isso funcionar, a cada atualização o texto do BUILD no index.html precisa mudar; Ajustes → Sobre tem "Verificar atualização".
- **Lembrar de pagar:** botão ⏰ nas despesas e parcelas pendentes e na fatura do cartão; os lembretes podem ir para o Google Agenda ou para um arquivo .ics (que avisa mesmo com o app fechado).

## Estilos do mascote (versão 4.2)
Em Ajustes → Mascote: o lobo Executivo (terno branco) e 10 roupas (Jazz, Piloto, Rei, Detetive, Hacker, Chefão, Preso, Bêbado, Magnata e Férias). Cada estilo tem animações próprias (piscar, orelhas, balanço de cabeça no ritmo da personalidade e efeitos como notas musicais, fumaça, faíscas e "hic!") e falas próprias sobre dinheiro. A troca automática (a cada 3 horas, nunca repetindo o estilo anterior) vem DESLIGADA por padrão; a escolha manual fica gravada. As telas de login usam o mesmo estilo (com a senha oculta, o lobo fecha os olhos).

## Acabamento visual (versão 4.3)
Transições e animações leves (só transform e opacidade, todas curtas e finitas; paradas quando o Android está com "reduzir movimento"): entrada em sequência nas telas de boas-vindas e login; indicador que desliza sob a aba ativa da navegação; brilho rápido ao tocar nos botões (inclusive nas abas); barras de gráfico que crescem, anéis que entram, linhas de lista que aparecem em sequência, sino que balança ao entrar na Home quando há avisos e aviso rápido (toast) que sobe deslizando.
