# GUIA DE ROTEAMENTO E COLETA (FONTE UNICA)

Este arquivo e a fonte unica para triagem, codigo de peca, rito e coleta de dados obrigatorios.

## 1. TRIAGEM DE DOMINIOS

| Dominio | Triggers |
|---|---|
| A - Imobiliario | posse, esbulho, turbacao, reintegracao, interdito, imissao, reivindicatoria, usucapiao, vizinhanca, anulatoria, passagem forcada |
| B - Consumerista/JEC | CDC, consumidor, negativacao, plano de saude, telefonia, overbooking, distrato, corte de energia, vicio de produto, atraso de reparo |
| C - Civel | acidente de transito, aluguel atrasado, despejo, locacao |
| D - Intermediarios | procuracao, substabelecimento, habilitacao, declaracao de hipossuficiencia, acordo |

## 2. TRIAGEM DETALHADA POR TIPO DE PECA

### 2-A - Imobiliario (`minutas-imobiliarias.md`)
| Situacao | Codigo | Rito e notas |
|---|---|---|
| Perda de posse (esbulho) | RPO | < 1 ano e 1 dia: forca nova. >= 1 ano e 1 dia: forca velha |
| Posse perturbada (turbacao) | MPO | Mesma logica de forca nova/velha |
| Ameaca concreta a posse | IPR | Mesma logica de forca nova/velha |
| Proprietario sem posse previa | IPO | Ordinario |
| Reivindicacao de posse | REI | Ordinario |
| Contestacao em usucapiao | CUS | Ordinario |
| Direito de vizinhanca | VIZ | JEC (<=40 SM) ou ordinario |
| Anulatoria de negocio | ANU | Ordinario (decadencia 4 anos) |
| Passagem forcada | PAF | Ordinario |

### 2-B - Consumerista/JEC (`minutas-consumeristas.md`)
| Codigo | Peca | Triggers |
|---|---|---|
| PI | Peticao inicial generica | produto nao entregue, servico nao prestado |
| NEG | Negativacao indevida | SPC, Serasa, fraude |
| PSC | Plano de saude (cancelamento) | cancelamento indevido |
| PSN | Plano de saude (negativa) | cobertura negada |
| TEL | Telefonia | bloqueio, internet, cobranca indevida |
| TRO | Transporte (pane) | atraso por pane |
| TRB | Transporte (overbooking) | pretericao de embarque |
| DIS | Distrato | recusa de cancelamento, multa abusiva |
| CEL | Corte de energia | interrupcao indevida |
| RPR | Demora de reparo | art. 18 CDC, prazo expirado |
| RI | Recurso inominado | prazo recursal JEC |
| CR | Contrarrazoes | resposta a recurso |
| ED | Embargos de declaracao | omissao, contradicao, erro material |

### 2-C - Civel (`minutas-civeis.md`)
| Codigo | Peca | Triggers |
|---|---|---|
| ATR | Acidente de transito | colisao, BO, conserto, lucros cessantes |
| ALU | Locacao/despejo | aluguel atrasado, despejo |

### 2-D - Intermediarios (`minutas-intermediariais.md`)
| Codigo | Documento | Uso padrao |
|---|---|---|
| PRO | Procuracao ad judicia et extra | representacao processual |
| SUB | Substabelecimento | transferir/compartilhar poderes |
| HAB | Habilitacao de advogado | regularizar representacao no processo |
| DHI | Declaracao de hipossuficiencia | gratuidade de justica |
| ACO | Peticao de acordo | homologacao de transacao |

## 3. DADOS OBRIGATORIOS POR CODIGO

| Codigo | Dados adicionais obrigatorios |
|---|---|
| RPO/MPO/IPR | data do fato, historico da posse, atos do reu, prova documental |
| IPO/REI | titulo registrado, matricula, cadeia dominial |
| CUS | numero do processo, area, cadeia possessoria/dominial |
| ANU | documento viciado, data, tipo de vicio, terceiro de boa-fe |
| PAF | imovel serviente, proposta de indenizacao |
| NEG | credor, valor, data de descoberta, impactos |
| CEL | UC, data/hora do corte, adimplencia |
| RPR | produto, data de assistencia, prazo de 30 dias |
| ALU | debitos, fiadores, ocupacao atual do imovel |
| ATR | data/hora/local, BO, danos, orcamentos |
| PRO | qualificacao do outorgante, CPF, poderes especiais, dados dos outorgados |
| SUB | dados do substabelecente/substabelecido, reserva de poderes, processo |
| HAB | numero do processo, dados do novo patrono, pedido de intimacao exclusiva |
| DHI | qualificacao do declarante, fundamento da hipossuficiencia, assinatura |
| ACO | partes, objeto, valor, forma de pagamento, clausulas de quitacao |

## 4. REGRAS GERAIS DE EXECUCAO
- Confirmar rito e codigo antes da redacao final.
- Nao inventar dados; usar `[A PREENCHER]`.
- Valor da causa por algarismos e por extenso quando aplicavel.
- Em possessorias, observar fungibilidade e criterio temporal de forca nova/velha.
- Em documentos intermediarios, permitir modo autonomo do `estagiario` quando nao houver ambiguidade estrategica.

