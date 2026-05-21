<!--
Sync Impact Report
==================
Version change: (template/unratified) → 1.0.0
Modified principles: N/A (initial ratification)
Added sections:
  - Core Principles (SOLID, YAGNI, DRY)
  - Development Lifecycle (4-phase pipeline)
  - LangChain Architecture and Corporate Context
  - Context Management and Security
  - Governance
Removed sections: Template placeholder principles (Library-First, CLI Interface, etc.)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/checklist-template.md ⚠ no changes required (generic)
  - .specify/templates/commands/*.md ⚠ not present in repository
  - README.md ⚠ not present in repository
Follow-up TODOs: none
-->

# PDV-AI Constitution

## Core Principles

### SOLID

Todo o design de classes e módulos MUST respeitar os cinco princípios SOLID. Priorize
injeção de dependências e interfaces bem definidas para isolar completamente as regras
de negócios da orquestração do LangChain.

**Rationale**: Isolamento de domínio corporativo permite evolução independente da camada
de IA e facilita testes sem acoplamento a provedores ou frameworks.

### YAGNI (You Aren't Gonna Need It)

Desenvolva apenas o que foi estritamente especificado para a feature atual. A antecipação
de cenários hipotéticos futuros e a criação de abstrações desnecessárias são proibidas.

**Rationale**: Escopo controlado reduz dívida técnica e mantém entregas alinhadas ao
valor de negócio imediato.

### DRY (Don't Repeat Yourself)

A duplicação de lógica ou de configuração (incluindo templates de prompts de IA) é
inaceitável. Extraia comportamentos comuns para utilitários ou serviços modulares.

**Rationale**: Uma única fonte de verdade para regras e prompts evita divergência silenciosa
e simplifica manutenção.

## Development Lifecycle

Pipeline rigoroso de quatro fases. Nenhuma fase pode ser ignorada ou reordenada.

### Phase 1 — Documentation and UML

Antes de escrever qualquer linha de código de aplicação, o agente MUST gerar um documento
técnico descrevendo a feature. Este documento MUST incluir diagramação em sintaxe UML
(Diagrama de Classes para estrutura estática e/ou Diagrama de Sequência para fluxos de
dados do LLM/VectorDB).

**Rationale**: Design explícito reduz retrabalho e estabelece contrato verificável antes
da implementação.

### Phase 2 — Validation Gate

O agente MUST pausar o fluxo e solicitar aprovação humana da especificação técnica e da
UML gerada. É proibido iniciar a codificação sem validação arquitetural explícita.

**Rationale**: Gate humano previne implementação de designs incorretos ou incompletos.

### Phase 3 — Guided Implementation

O código gerado MUST refletir exatamente o contrato estabelecido na UML validada, aderindo
estritamente aos princípios desta constituição. Type hinting é obrigatório em todo código
Python de aplicação.

**Rationale**: Implementação fiel ao design aprovado garante rastreabilidade e qualidade.

### Phase 4 — Validation and Tests

Toda implementação MUST ser finalizada com testes (unitários e/ou integração). Chamadas de
rede para APIs de IA no LangChain MUST ser alvo de mocking durante as baterias de testes
padrão.

**Rationale**: Testes automatizados com mocks de rede garantem CI confiável e regressão
detectável sem custo de API.

## LangChain Architecture and Corporate Context

### Separation of Concerns (SoC)

A lógica corporativa da aplicação (ex.: validações B2B/SaaS, integrações de banco) MUST
NOT estar emaranhada com a construção de chains ou invocações de agentes.

**Rationale**: Domínio corporativo e orquestração de IA evoluem em ritmos diferentes;
acoplamento direto impede ambos.

### Model Agnosticism

O sistema MUST operar com as interfaces genéricas do framework (`BaseChatModel`). A troca
do provedor do LLM MUST ser um ajuste de configuração, não uma refatoração de código.

**Rationale**: Vendor lock-in em código de aplicação aumenta custo de migração e testes.

### Prompt Management

Prompts são infraestrutura crítica. MUST ser mantidos em módulos isolados. É estritamente
proibido o uso de strings chumbadas diretamente nas funções de execução.

**Rationale**: Prompts centralizados permitem versionamento, revisão e reutilização sem
caça a strings espalhadas no código.

## Context Management and Security

### Memory Isolation (Multi-tenant)

O contexto de conversação e o armazenamento de embeddings MUST ser sempre particionados
por locatário ou identificador de usuário. Vazamento de dados contextuais entre entidades
é uma falha arquitetural grave.

**Rationale**: Isolamento por tenant é requisito mínimo de segurança e conformidade em
aplicações B2B/SaaS.

### Secrets Management

Chaves de API MUST NOT transitar em texto claro nem ser definidas no código. A configuração
MUST exigir injeção via variáveis de ambiente ou mecanismo equivalente de secrets.

**Rationale**: Segredos em código ou logs expõem credenciais e violam práticas básicas de
segurança operacional.

## Governance

Esta constituição supersede práticas ad hoc e guia todos os artefatos Spec Kit (spec,
plan, tasks, implementação).

**Amendment procedure**: Alterações MUST ser propostas via `/speckit-constitution`, documentadas
no Sync Impact Report, e refletidas nos templates dependentes antes de entrar em vigor.

**Versioning policy**:
- MAJOR: remoção ou redefinição incompatível de princípios ou gates
- MINOR: novo princípio, seção ou gate materialmente expandido
- PATCH: clarificações, correções de redação, refinamentos não semânticos

**Compliance review**: Todo plan.md MUST incluir Constitution Check com gates verificáveis.
Implementações MUST ser revisadas contra os princípios SOLID/YAGNI/DRY, isolamento LangChain,
multi-tenant, gestão de prompts e testes com mocking de API de IA. Violações MUST ser
documentadas na tabela Complexity Tracking do plano ou corrigidas antes do merge.

**Runtime guidance**: Consulte `.cursor/rules/specify-rules.mdc` e o plan.md da feature
ativa para contexto tecnológico e estrutural.

**Version**: 1.0.0 | **Ratified**: 2026-05-20 | **Last Amended**: 2026-05-20
