# Validacao de Handoff Dashboard (Codex)

## Gates obrigatorios
- [ ] `request_id` preenchido e unico
- [ ] `mode` valido (`autonomo` ou `subordinado`)
- [ ] `task_type` definido
- [ ] `owned_paths` definido e nao vazio
- [ ] `acceptance_criteria` definido
- [ ] `status` dentro de `ready|needs_clarification|blocked|done`

## Anti-colisao
- [ ] Nenhuma alteracao fora de `owned_paths`
- [ ] Sem sobreposicao com ownership backend (`api/**`, `services/**`, `domain/**`, `db/**`, `tests/**`)
- [ ] Em conflito, status `blocked` com justificativa

## Validacao de saida (`done`)
- [ ] `files_changed` preenchido
- [ ] `validation_commands` executados e registrados
- [ ] `validation_result` informado
- [ ] `residual_risk` declarado
