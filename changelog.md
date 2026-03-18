# 📜 Changelog
Todas as mudanças importantes deste projeto serão documentadas aqui.

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