# Wolfin no GitHub Pages — notícias que se atualizam sozinhas

Com este pacote, o site fica num endereço próprio (`https://SEU-USUARIO.github.io/wallstreet/`) e o GitHub
busca as notícias sozinho a cada 3 horas, de graça. Você só faz isso uma vez.

## Arquivos
| Arquivo | Para quê |
|---|---|
| `index.html` | O site Wolfin (já lê o `noticias.json`) |
| `manifest.webmanifest`, `sw.js` | Fazem o site ser instalável como app e abrir sem internet |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png` | Ícone do app / atalho na tela inicial |
| `noticias.json` | Notícias (começa com a coleta de 05/11/2026; depois o robô atualiza) |
| `scripts/atualizar_noticias.py` | Busca os feeds RSS e gera o `noticias.json` |
| `.github/workflows/noticias.yml` | Manda o GitHub rodar o script a cada 3 horas |

## ⚠️ ANTES de começar: faça backup
Os dados do Wolfin ficam guardados **por endereço**. Ao abrir o site no endereço novo, ele começa vazio.
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
- Na primeira abertura aparece "Proteger o Wolfin": crie usuário e senha. Os dados passam a ficar **criptografados (AES-256)** no aparelho e só abrem com a senha.
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

## Escolha do mascote no cadastro (versão 4.4)
Em "Criar minha conta" há uma etapa nova depois do nome: "Escolha seu mascote". Mostra os 11 estilos (Executivo, Jazz, Piloto, Rei, Detetive, Hacker, Chefão, Preso, Bêbado, Magnata e Férias) em grade com miniatura e nome; o lobo do topo muda na hora ao tocar. A escolha é salva na conta (junto com as preferências, criptografadas quando há senha) e espelhada para a tela de login, então aparece nos próximos acessos. Quem toca só em Continuar fica com o Executivo. "Usar sem senha" e "Já tenho uma conta" não têm a etapa (o estilo muda em Ajustes → Mascote).

## Tutorial do primeiro acesso (versão 4.5)
Depois de CRIAR uma conta nova ("Criar minha conta" ou "Usar sem senha"), o app mostra um passeio rápido de 8 passos (Seu painel, Lançamentos rápidos, Receitas, Despesas, Dívidas e Caixinhas, Relatórios, Ajustes e um final) com destaque na própria tela e um balão explicativo. "Pular" fica disponível o tempo todo (a tecla Esc também pula). Ao concluir ou pular, o app grava na conta (S.flags.tour) que o tutorial já foi visto e não o mostra de novo. Contas que já existem e backups importados NÃO veem o tutorial (o gatilho é só a criação de conta). Em Ajustes → Sobre há "Ver o tutorial" para rever quando quiser.

## Detetive corrigido (versão 4.6)
O estilo Detetive do mascote usa agora o PNG transparente enviado (chapéu, rosto, terno, distintivo, mão com o cigarro e a fumaça), embutido em WebP (~42 KB) na proporção do palco (1024×880), inteiro e sem cortes (só um esmaecido suave na cintura, onde a imagem original termina). Pálpebras e orelhas foram realinhadas ao novo desenho; a fumaça sai da ponta do cigarro (3 baforadas) e a brasa pulsa. O quadro do Detetive na Home e no login mostra o desenho completo; a miniatura em Ajustes e no cadastro é centrada no rosto.

## Tema Pérola e escolha de cor no cadastro (versão 4.7)
Nova paleta **Pérola** (#E8EDF5: fundo perolado com acento azul-ardósia legível; versão escura própria), primeira da lista em Ajustes → Aparência e padrão do site (aplicado já na primeira visita, sem piscar azul). O **Azul** e as demais cores continuam disponíveis. Em "Criar minha conta" há uma nova etapa depois do mascote: "Escolha a cor do seu tema" (9 cores + Claro/Escuro, com pré-visualização ao vivo, Pérola selecionada por padrão). A escolha é salva na conta e espelhada para a tela de login. Quem já usa o app mantém a cor que tem; "Usar sem senha" e "Já tenho uma conta" não passam pela etapa (troca em Ajustes).

## Situação financeira com cartões (versão 4.8)
A "Minha situação financeira" (Relatórios) agora considera os cartões de crédito, pela mesma lógica da tela Cartões (função `ccFin`, só leitura): faturas que vencem no mês entram nos compromissos e nas despesas do mês (pagas e pendentes); o saldo devedor dos cartões (faturas pendentes + parcelas futuras no cartão) entra em "Parcelas e faturas a pagar" e na capacidade de pagamento; fatura vencida e não paga conta como atraso. Pagamentos parciais reduzem o pendente e o saldo na mesma medida (sem contar duas vezes); pagar a mais nunca deixa pendente negativo. Sem cartões, o resultado e a tela são idênticos aos da versão anterior (verificado em 300 cenários). O saldo disponível, Home, Dívidas e Relatórios de fluxo (caixa) não mudaram.

## Validação dos pagamentos de fatura (versão 4.9)
Em Cartões → Pagar fatura: o valor não pode passar do que falta pagar (total da fatura − pagamentos anteriores); o formulário mostra o máximo e já vem preenchido com ele, e o limite é conferido de novo no momento de salvar. Valor acima, zero, negativo ou inválido mostram uma mensagem clara e nada é gravado. Fatura quitada não aceita novos pagamentos (o botão não aparece e a ação é bloqueada mesmo se acionada). Envios repetidos (clique duplo, Enter) gravam um único pagamento (trava de ~1 s e limite recalculado). Saldo, despesas pagas do mês, Situação financeira e histórico atualizam na mesma operação; desfazer um pagamento devolve o valor ao pendente. Dados antigos com pagamento acima da fatura são preservados (a fatura aparece como "Paga" e o pendente nunca fica negativo). O auxiliar de formulários passou a ignorar com segurança um segundo envio que chega depois de o formulário fechar.

## Salvamento seguro (versão 5.0)
No modo protegido, a gravação passou a ser uma fila única que sempre leva o estado mais recente: criptografa (chave capturada no momento de salvar), grava e confere lendo de volta. O aviso "Salvo ✓" (e os demais avisos emitidos durante a gravação) só aparece depois que isso termina com sucesso; se falhar, aparece "Não foi possível salvar os dados protegidos…" e o armazenamento continua com a versão anterior íntegra (a próxima gravação leva o estado completo). Fechar a página durante a gravação dispara o aviso do navegador. Quando outra janela/aba do app grava dados diferentes, esta página pede para recarregar e fica só leitura, para nunca sobrescrever dados novos com antigos; a tela de login usa sempre o cadastro protegido mais recente. Abrir o app não regrava dados que não mudaram. Criptografia e formato guardado inalterados. Limite: fechar de verdade no meio da gravação pode perder a última alteração (o armazenamento nunca fica corrompido).

## Cache do app (versão 5.1)
O `sw.js` agora identifica os caches como `wallstreet::<escopo>::v<versão>` (ex.: `wallstreet::/wallstreet/::v3`) e só cria, lê e apaga caches com essa identificação (mais o nome antigo `wallstreet-vN`). Caches de outros projetos do mesmo domínio (como o github.io, que é compartilhado) nunca são tocados, e o app só responde por arquivos da própria pasta. Instalação: o `index.html` é obrigatório (se falhar, a versão atual continua valendo e não sobra cache pela metade); ícones e manifesto são "melhor esforço". Ativação: só limpa as versões antigas se o cache novo está íntegro, e limpa de novo na primeira requisição (caso um worker antigo recrie algo). Rede primeiro revalidando sempre (não aparece arquivo velho nem do cache HTTP do navegador); se a rede falhar ou levar mais de 6 s, usa a cópia guardada. O botão "Atualizar agora" agora desregistra só o Service Worker deste app e apaga só os caches dele. Para trocar de versão do cache, mude `VERSAO` no `sw.js`. Dados financeiros (localStorage), criptografia e login não são tocados.

## Importação protegida de backups (versão 5.2)
Antes de importar, o arquivo é validado por inteiro numa cópia (estrutura, listas obrigatórias, tipos, valores em centavos, datas, cartões, versão dos dados, campos suspeitos, tamanho). Arquivos vazios, cortados, corrompidos, de outro app ou de versão mais nova são recusados com mensagem clara e os dados atuais não são tocados. O backup comum novo traz um selo de integridade (`__backup`, SHA-256): se o arquivo for alterado depois de exportado, a importação é recusada; backups antigos (sem selo) continuam aceitos, assim como os criptografados (criptografia inalterada). Antes de substituir, a confirmação mostra o resumo do backup e dos dados atuais e avisa de: menos registros que os atuais, mais antigo que o último backup, mesmo backup já importado, versão antiga. Backup igual aos dados atuais não é reimportado. Cliques repetidos e importações simultâneas são impedidos. A troca é atômica: se a gravação falhar (armazenamento cheio, criptografia, conferência, janela desatualizada), tudo volta como estava. A tela "Já tenho uma conta" usa a mesma validação. Não há cópia automática dos dados atuais antes de substituir: exporte um backup antes se quiser guardá-los.

## Segurança de acesso reforçada (versão 5.3)
Controle de tentativas de senha e de código de recuperação: a tentativa é contada ANTES de verificar (fechar a aba no meio não escapa; envios simultâneos não multiplicam palpites; tentativas com menos de ~1 s de intervalo são recusadas sem contar). Espera progressiva a partir da 3ª falha seguida: 15 s, 30 s, 1 min, 2 min, 5 min, 10 min, 15 min e depois sempre 30 min (teto: nunca bloqueia para sempre). Sem tentativas por 2 h a contagem cai; por 24 h volta a um nível leve; valor absurdo no controle vira no máximo 30 min; relógio voltado para trás também não passa de 30 min. O estado fica em 3 lugares independentes (localStorage, IndexedDB e Cache, usa-se o mais restritivo): apagar um não zera, e o apagado é restaurado. Durante a espera até a senha certa é recusada com a mesma resposta; as mensagens são genéricas. A recuperação por código tem contador próprio (não é travada pela espera da senha) e funciona como antes; qualquer acesso correto zera tudo. Criptografia (AES-256-GCM, PBKDF2), senhas, chaves e códigos de recuperação não foram alterados. Limites: quem apaga os 3 lugares ou adianta o relógio do aparelho pula a espera; e a espera não protege contra quem copia o arquivo criptografado e testa senhas fora do app (aí só valem a senha forte e o PBKDF2).

## Relatórios financeiros completos (versão 5.4)
A tela Relatórios ganhou 7 cartões novos abaixo da "Minha situação financeira" (os que já existiam continuam): Resumo do mês (recebido, pago, dívidas pagas, guardado, saldo inicial, resultado e saldo final), Indicadores do mês (positivo / atenção / crítico, com as mesmas regras da Situação financeira), Comprometimento da renda (contas, parcelas e faturas de cartão em % da renda prevista; pago, a pagar e vencido; dívidas pagas à parte), Despesas por categoria (participação em %), Despesas recorrentes (contas fixas, parcelamentos e compras parceladas no cartão), Evolução das dívidas (inicial, pago, restante e saldo devedor por mês) e Comparação mensal (dois meses à escolha). Tudo é calculado dos lançamentos reais, sem estimativas; no mês atual o total comprometido é igual ao da Situação financeira e o saldo final é igual ao saldo principal. Atenção: marcar uma parcela como paga NÃO reduz o saldo disponível (comportamento já existente); o resumo mostra "Parcelas deste mês já pagas" à parte. Backups que só diferem em tema/cor agora mostram a confirmação de importação.

## Acessibilidade e navegação (versão 5.5)
Janelas (formulários, confirmações, avatar, limites) agora são diálogos modais: título falado, foco entra e fica preso nelas, Esc fecha, o fundo fica inerte e o foco volta ao botão que abriu (ou ao título da tela). A calculadora flutuante abre por teclado/leitor de tela (antes só por toque de ponteiro). Anel de foco visível nos dois temas, link "Pular para o conteúdo", avisos (toast) e erros lidos sozinhos, 32 gráficos com descrição falada (valores escondidos também ficam escondidos), barras decorativas fora da leitura, botões de tema/cor com estado (aria-pressed), aba atual marcada (aria-current), cada tela anuncia o nome no título da página e leva o foco ao título, foco preservado ao redesenhar a tela. Áreas de toque de no mínimo 44 px (inclusive a barra inferior em telas de 320 px) e quatro textos pequenos com contraste ajustado. Redução de movimento do aparelho continua respeitada. Cálculos, dados, criptografia e login não foram alterados. Testado em emulação do Chromium (tamanhos de tela, Pixel 5, Galaxy S9+) e com teclado; não foi testado em aparelho físico nem com TalkBack. Um backup que só difere em tema, cor, mascote ou avatar agora mostra a confirmação de importação.

## Testes automatizados
A pasta `tests/` tem a estrutura de testes (veja `tests/README.md`) e `.github/workflows/tests.yml` roda tudo no GitHub a cada envio, com um job por área. Localmente: `pip install -r tests/requirements.txt`, `python -m playwright install chromium` e `python tests/run_all.py`. Usa só dados fictícios; não depende de nada do app em produção. Um envio com teste vermelho não deve ser publicado.

## Nova identidade: Wolfin (versão 6.0)
O aplicativo agora se chama **Wolfin** (título: "Wolfin – Controle Financeiro"; slogan: "Domine seu dinheiro."). O nome e o slogan aparecem nas telas de boas-vindas e login, no cartão principal da Home, na página Sobre, no título das abas, no tutorial, nos avisos e nos arquivos gerados (`wolfin-backup-AAAA-MM-DD.json`, `lembrete-wolfin.ics`). O manifesto PWA passa a ter nome "Wolfin – Controle Financeiro" e nome na tela inicial "Wolfin"; o `id`, o `start_url` e o `scope` não mudaram, então o app instalado continua o mesmo (o Android pode levar um tempo para atualizar o nome e o ícone na tela inicial).

**O que NÃO mudou, de propósito (compatibilidade):** o endereço do site e do repositório (`/wallstreet/`), as chaves de armazenamento no navegador (`wallstreet.*`), o prefixo dos caches do Service Worker (`wallstreet::`) e o marcador interno dos backups (`wallstreet-backup`). Por isso quem já usa o app **não perde dados, não precisa refazer a senha** e continua importando backups antigos. A logo (lobo) foi preservada.

**Marca:** a disponibilidade jurídica do nome "Wolfin" (registro de marca, domínio, Play Store) **não** foi verificada por esta mudança e deve ser validada à parte antes de qualquer publicação comercial.

## Intro animada (versão 6.3: vídeo com som, uma vez por sessão)
A intro em vídeo (cerca de 6 s, vertical) criada pelo dono do app aparece **uma vez por sessão**: na primeira abertura do site/app e de novo só quando se abre em outra aba/janela ou se fecha e reabre o app. **Recarregar não repete** (nem o recarregamento automático do app ao bloquear ou atualizar). Isso usa `sessionStorage` ("wolfin.intro"); não dá para detectar "saiu e voltou ao navegador" com precisão: se o navegador mantiver/restaurar a aba, a intro não reaparece. Sem `sessionStorage` (modo restrito) ela toca normalmente.

**Som:** o vídeo tem o áudio original (MP4: AAC; WebM: Opus). O app tenta tocar com som; navegadores costumam bloquear som automático (o Chrome tende a permitir em app instalado). Se bloquear, o vídeo toca **mudo** e aparece o botão "Toque para ativar o som" (liga o áudio sem pular a intro). Confirme que você tem os direitos de uso da música/efeitos do vídeo.

Arquivos: `intro-wolfin.mp4` (H.264+AAC, ~0,7 MB) e `intro-wolfin.webm` (VP9+Opus, ~0,8 MB), convertidos do original (1440×2560, 60 fps, 19,9 MB) para 720×1280, 30 fps. O navegador baixa só o formato que consegue tocar; o Service Worker guarda o MP4 já na instalação e serve os trechos (Range/206), então a intro em vídeo toca offline. Um toque (ou tecla) pula; em tela larga, com "reduzir movimento", ou se o vídeo não carregar em ~3 s, usa a **intro em CSS** (logo com reflexo e orelhas, nome e slogan, ~1,5 s; com movimento reduzido, estática por ~0,6 s). Para trocar o vídeo, gere os dois arquivos com os mesmos nomes (ou mude os nomes no script da intro e use nomes novos a cada versão para o cache não servir o antigo). Os testes (`tests/suites/intro_wolfin.py`) conferem formato, tamanho, áudio, margens do texto, som permitido/bloqueado, sessão e offline.

## Cor padrão e mascote (versão 6.3)
- **Cor padrão: Azul** (para combinar com a intro). As 9 cores continuam disponíveis em Ajustes → Aparência (Azul agora é a primeira; a Pérola continua como opção). Quem já escolheu uma cor mantém a escolha; o padrão vale para contas novas e primeiras visitas.
- **Troca automática de roupa do mascote: removida.** A roupa fica sempre a escolhida em Ajustes → Mascote. Dados/backups antigos com a troca ligada são aceitos: ela passa a desligada e a roupa atual é mantida (o campo `ma` continua nos backups só por compatibilidade).

## Mascotes oficiais (versão 7.0): mascote = avatar
O app tem **10 mascotes oficiais**, e o escolhido é também o **avatar** em todo o app (cabeçalho da Home, cartão do mascote, Ajustes, tela de login): Wolfin (Lobo, CEO, mascote principal), Leônidas (Leão, Rei), Don Vito (Raposa, Magnata), Oráculo (Coruja, Analista), Brutus (Touro, Investidor), Mako (Tubarão, Negociador), Bento (Castor, Planejador), Penny (Esquilo, Poupador), Nyx (Pantera, Hacker) e Elliot (Guaxinim, Detetive). Não existe mais seleção separada de avatar, nem as roupas do lobo, nem a troca automática de roupa.
- **Onde escolher:** na criação da conta (lista com imagem, nome, animal · função e descrição curta; o Wolfin aparece primeiro como "Principal", mas não é obrigatório) e em **Ajustes → Meu mascote** (ou tocando no avatar do cabeçalho).
- **Imagens:** PNG enviados pelo dono do app, convertidos para WebP (544 px, ≈ 406 KB no total) e **embutidos** no `index.html` (funcionam offline). O avatar é um recorte do rosto da mesma imagem. O script que gera os dados está em `tests/tools/gerar_mascotes.py` (precisa dos PNG originais).
- **Animações (só CSS, individuais por personagem):** piscar com pálpebras sobre o rosto (olhos fecham ao digitar a senha no login), movimento de cabeça e respiração próprios, orelhas (Wolfin, Don Vito, Brutus, Penny, Nyx, Elliot), brilhos (joias, correntes, moeda, abotoaduras), reflexo em óculos e lupa (Oráculo, Bento, Elliot), fumaça discreta (Brutus) e pulsação neon (Nyx). Com "reduzir movimento" tudo fica estático. Não foram implementados: movimento do chapéu/sobrancelhas do Don Vito, ajuste dos óculos do Oráculo, movimento da moeda da Penny e ajuste da lupa do Elliot.
- **Dados e migração:** o mascote fica em `pref.mc` (e em `wallstreet.look`, para a tela de login). Contas e backups antigos são migrados ao abrir/importar, **sem apagar nada** (os campos antigos `av` e `ms` continuam nos dados): avatar escolhido → lobo=Wolfin, gato preto=Nyx, tigre=Leônidas, raposa=Don Vito, coruja=Oráculo, panda-vermelho=Elliot; senão a roupa antiga → Rei=Leônidas, Detetive=Elliot, Hacker=Nyx, Magnata=Don Vito; sem correspondência → Wolfin. A conquista "Cara própria" agora é "escolha o seu mascote".

## Correções da auditoria final (versão 7.1)
- **Parcela paga desconta do saldo.** Marcar uma parcela como paga agora reduz o saldo disponível. O mês do caixa é a data do pagamento (`paidOn`); sem ela, o vencimento; sem ele, o mês da parcela. Antes, parcelas pagas eram "registradas à parte" e não alteravam o saldo (o saldo podia ficar superestimado). **Quem já tinha parcelas pagas vê o saldo diminuir uma vez**, com um aviso único mostrando o valor (marcador `flags.pqv`). Relatórios mostra "Inclui R$ X de parcelas pagas neste mês".
- **Rótulos:** Home "Receitas / Despesas / Diferença" (diferença = receitas − despesas do mês, sem caixinhas e dívidas); Despesas "Pagas (sem faturas de cartão)"; Relatórios "Resultado do mês (após dívidas e caixinhas)".
- **Desempenho:** os cálculos repetidos dentro de um único desenho de tela são reaproveitados (nada fica guardado depois). Home ≈ 31–49% mais rápida e Relatórios ≈ 17–24% (medido com dados fictícios). O cartão "Minha situação financeira" continua sendo o mais pesado (recomendação em aberto).
- **Senha mais forte** (criação da conta, troca de senha, recuperação e backup criptografado): mínimo de 10 caracteres; recusa senhas comuns, repetidas, em sequência e só numéricas com menos de 12 dígitos; indicador de força na criação. Contas existentes **não** são afetadas (o login não usa essa regra).
- **Política de conteúdo (CSP) e `referrer`:** o app só fala com o próprio site, sem plugins, sem `<base>`, formulários só para o próprio site, sem referrer. Vale só em http/https e nunca no modo de testes. Limites: os scripts do app continuam permitidos inline e o bloqueio de `eval` não foi confirmado.
- **Armazenamento persistente:** o app pede ao navegador, uma vez e em silêncio, para não apagar os dados.
- **Workflows:** ações do GitHub atualizadas para versões com Node 24 (checkout v6, setup-python v6, setup-node v6, upload-artifact v7, escolhidas por pesquisa, **confirme na primeira execução**). O workflow de notícias roda uma por vez, em servidor fixo, reconcilia com seus envios (`git pull --rebase`) e tenta o envio até 4 vezes.

### Privacidade: origem compartilhada no GitHub Pages (importante)
Todos os sites de `pauldavilafnc.github.io` compartilham o mesmo armazenamento do navegador. **Não publique outros projetos nesta conta**, porque eles poderiam ler os dados do Wolfin (especialmente no modo "sem senha"). Para isolar de verdade, use uma conta/organização ou domínio próprio para o Wolfin (o endereço muda e os dados do navegador são por endereço: restaure por backup exportado). No modo sem senha os dados ficam em texto simples no navegador e o backup comum também; prefira proteger com senha e exportar backup criptografado.

## Intro: som automático, sem botão (versão 7.2)
O botão "Toque para ativar o som" foi removido. A intro **tenta tocar com som sozinha**; se o navegador bloquear o som automático (a regra da maioria), ela toca **muda**, sem botão nem aviso. Um toque ainda pula a intro. **Nenhum site consegue forçar som automático**: quem decide é o navegador. O som costuma tocar automaticamente quando o Wolfin está **instalado como app** (tela inicial) e, em alguns navegadores, depois de permitir som/autoplay para o site nas configurações do navegador.

## Nova entrada: som da intro, 3 etapas, ENTRAR e senhas (versão 7.3)
- **Intro com controle de som.** Voltou um botão **discreto** (canto superior direito, só na intro em vídeo). A intro continua **tentando** tocar com som, mas **só se o navegador permitir**; se bloquear, toca muda e o botão mostra "som desligado" (tocar nele liga). Tocar no botão **não** pula a intro (tocar em qualquer outro lugar pula). Desligar o som fica lembrado em `wolfin.introsnd` (única chave nova; não é dado financeiro). Em movimento reduzido ou tela larga, a intro é em CSS, sem som e sem botão.
- **Quem ainda não tem conta vê 3 etapas** (cada uma com "Etapa N de 3"): **1. Escolha seu mascote** (os 10, com imagem, nome, animal · função e descrição; o Wolfin primeiro, "Principal"; é preciso escolher um para continuar) → **2. Escolha sua aparência** (claro/escuro + 9 cores, com prévia que muda na hora; Azul continua o padrão) → **3. Boas-vindas** (o mascote escolhido se apresenta e explica o app em frases curtas) → **nome** → **criar usuário e senha**. Nada é gravado até concluir a conta; ao concluir, mascote, cor, tema e nome vão para a conta e o mascote vira o avatar.
- **ENTRAR** aparece, pequeno, no centro embaixo, em **todas as 3 etapas**. Ele leva à tela de entrada (**Entrar na sua conta**). Como os dados ficam só no aparelho (sem servidor), em um aparelho novo "entrar" significa **importar o backup** da conta. Quem já tem conta neste aparelho **nunca vê as etapas**: cai direto no login.
- **"Usar sem senha por enquanto"** saiu da primeira tela e fica na tela de criar acesso.
- **Senhas:** "Senha" e "Repita a senha" (e, na recuperação, "Nova senha" e "Repita a nova senha") têm **cada uma o seu olho**, independentes, com nomes diferentes para leitores de tela.
- **Não mudou:** cálculos, relatórios, backups, armazenamento financeiro, criptografia, chaves `wallstreet.*`.
