# 📜 Changelog
Todas as mudanças importantes deste projeto serão documentadas aqui.

> ⚠️ Versões antigas podem conter descrições mais técnicas.
> A partir da V0.2.2, o changelog foi simplificado para melhor entendimento dos usuários.

## V0.3.1 - 20/03/2026

### Correções
- Corrigido avatar exibido no comando `$rankroleta`
- Agora o embed mostra corretamente o avatar do usuário consultado



## V0.3.0 - 20/03/2026

### Novidades
- Novo sistema de estatísticas da roleta (dados agora são salvos permanentemente)
- Novo comando `$rankroleta` para visualizar suas estatísticas
- Agora é possível visualizar estatísticas de outros usuários usando menção

### Sistema de roleta aprimorado
- O bot agora registra:
  - Número de partidas
  - Número de mortes
  - Número de sobrevivências
  - Streak atual (quantas vezes sobreviveu seguidas)
  - Melhor streak já alcançada
- Dados são mantidos mesmo após reiniciar o bot

### Melhorias nos comandos
- `$rankroleta` exibe informações de forma visual e organizada
- Avatar exibido corretamente para o usuário consultado
- Respostas mais consistentes com o padrão visual do bot

### Sistema anti-spam
- Adicionado cooldown no comando `$roleta`
- Evita uso excessivo em curto período de tempo

### Melhorias internas
- Integração com banco de dados SQLite
- Estrutura de código preparada para futuras funcionalidades (ranking global, conquistas, etc.)
- Melhor organização da lógica da roleta



## V0.2.2 - 18/03/2026

### Novidades
- Melhor organização interna do bot (mais estabilidade e base para futuras melhorias)
- Mensagens mais bonitas e padronizadas em vários comandos
- Novo estilo de resposta para erros e confirmações

### Melhorias nos comandos
- `$quem` agora mostra o resultado de forma mais visual e com avatar do usuário sorteado
- `$8ball` agora exibe sua pergunta junto com a resposta
- `$cor` agora mostra erros e cores disponíveis de forma mais clara

### Correções
- Corrigido prefixo incorreto do bot (restaurado para `$`)

### Melhorias gerais
- Respostas mais claras ao usar comandos incorretamente
- Melhor consistência visual entre todos os comandos
- Melhor base para futuras atualizações do bot



## V0.2.1 - 17/03/2026



### Added
- Validação dinâmica de cores com base nos cargos do servidor
- Suporte a múltiplos idiomas no comando `$cor` (PT, EN, ES)
- Sistema de logs estruturados para os principais comandos (`$cor`, `$roleta`, `$avatar`, `$8ball`)
- Validação de entrada no comando `$8ball` (exige pergunta do usuário)

### Changed
- Estilizado o comando `$8ball`
- Estilizado o comando `$ajuda`
- Estilizado o comando `$ping`
- Estilizado o comando `$avatar`
- Melhorada a experiência de uso no comando `$cor`
- Comando `$update` agora exibe a última versão do changelog
- Padronização dos logs no formato `key=value` para facilitar leitura e futura análise
- Melhorias internas de desempenho e monitoramento de erros
- Melhor tratamento de entradas inválidas nos comandos

### Fixed
- Comandos faltantes adicionados ao `$ajuda`
- Corrigido erro ao usar `$cor` sem permissão
- Corrigido erro ao usar `$avatar` com usuário inválido



## V0.2.0 - 13/03/2026

### Added
- Comando `$8ball`
- Comando `$update`
- Comando `$roleta` (Roleta Russa)

### Changed
- Estilizado o comando `$roleta` com embed

### Fixed
- Comando `$avatar` não exige mais menção (@)

### Improved
- Bot agora aceita comandos em maiúsculas ou minúsculas

### Planned
- Estilização de outros comandos



## V0.1.0 - 12/03/2026

### Added
- Comando `$ping` (teste de latência do bot)
- Comando `$avatar` (exibe o avatar de um usuário)
- Comandos de tradução:
  - `$en` (inglês)
  - `$es` (espanhol)
  - `$pt` (português)
- Integração com API de tradução (GoogleTranslator)
- Sistema básico de comandos com prefixo `$`
- Configuração de intents (message_content)

### Deploy
- Bot hospedado no Railway (24/7)