import re
import os

base_path = r"c:\Users\hig0\Downloads\CONTABILIDADE"

# Vou construir o arquivo diretamente com as questões já transformadas em Certo/Errado
# A partir das questões extraídas dos 5 estados

output_content = """# Legislação Tributária Estadual - Questões de Certo/Errado

> Questões transformadas a partir de provas de Auditor Fiscal - SEFAZ

---

## MINAS GERAIS (SEFAZ-MG)

### Questão 1
A sociedade empresária Gazeta Sempre Extra detém um jornal com circulação diária e adquiriu peças sobressalentes para suas máquinas. Sobre a incidência de ICMS nessa aquisição, julgue o item:

( ) A aquisição de peças sobressalentes para máquinas gráficas de jornal está sujeita ao ICMS, pois a imunidade constitucional abrange apenas a circulação de jornais e periódicos, não se estendendo aos insumos utilizados em sua produção.

### Questão 2
Marina Góes adquire em uma licitação da Receita Federal um smartphone importado e apreendido. Acerca da incidência de ICMS, julgue o item:

( ) Incide ICMS sobre a arrematação de bem apreendido em licitação promovida pela Receita Federal, ainda que o arrematante não seja contribuinte habitual do imposto.

### Questão 3
A sociedade empresária DXD teve o ICMS arbitrado pelo Fisco por declarar valores notoriamente inferiores ao preço corrente. Sobre o arbitrado, julgue o item:

( ) No arbitrado do ICMS por declaração de valor inferior ao preço corrente, as retiradas dos sócios devem ser consideradas despesas indispensáveis à manutenção do estabelecimento para fins de cálculo do preço de custo acrescido.

### Questão 4
Luiz e Bianca se separaram judicialmente e Luiz deixou definitivamente para Bianca o imóvel do casal. Sobre a incidência de ITCD em Minas Gerais, julgue o item:

( ) Na dissolução da sociedade conjugal, incide ITCD apenas sobre a parcela que exceder a meação, devendo o imposto ser recolhido no prazo estabelecido pela legislação estadual de Minas Gerais.

### Questão 5
Sobre o devedor contumaz na legislação de ICMS de Minas Gerais, julgue o item:

( ) Para ser considerado devedor contumaz em Minas Gerais, o contribuinte deve ter débito de imposto declarado relativamente a seis períodos de apuração em doze meses ou relativamente a dezoito períodos de apuração, consecutivos ou alternados.

### Questão 6
Rafael Gomes teve um veículo histórico e de coleção com 22 anos de fabricação furtado e depois recuperado. Acerca da isenção de IPVA em Minas Gerais, julgue o item:

( ) Em Minas Gerais, o proprietário de veículo histórico e de coleção com mais de 20 anos de fabricação que teve o bem furtado e posteriormente recuperado faz jus à isenção do IPVA apenas pelo período compreendido entre a data do furto e a devolução ao proprietário.

### Questão 7
Júlia e Marina receberam valores de diferenças de aposentadoria de seu pai falecido, servidor público de Minas Gerais. Sobre a incidência de ITCD, julgue o item:

( ) Em Minas Gerais, os valores de diferenças de aposentadoria pagos aos herdeiros em razão do falecimento de servidor público estão sujeitos à incidência do ITCD, diferentemente do que ocorre com o saldo de FGTS e as remunerações oriundas de relação de trabalho.

### Questão 8
Antônio Palmeira comprou um carro usado na Itália com desembaraço aduaneiro em agosto de 2022. Sobre o fato gerador do IPVA em Minas Gerais, julgue o item:

( ) No caso de importação de veículo usado, o fato gerador do IPVA em Minas Gerais ocorre no momento do desembaraço aduaneiro, sendo o imposto devido de forma proporcional ao número de dias restantes do ano.

### Questão 9
Sobre as hipóteses de extinção do Contencioso Administrativo Fiscal em Minas Gerais, julgue o item:

( ) Constitui hipótese de extinção do Contencioso Administrativo Fiscal em Minas Gerais o não recolhimento integral da taxa de expediente devida.

### Questão 10
Marisa Pedroso recebeu previdência privada com seguro de vida do falecido marido. Sobre a incidência de ITCD em Minas Gerais, julgue o item:

( ) Em Minas Gerais, os valores recebidos a título de previdência privada nos aportes financeiros e respectivos rendimentos estão sujeitos à incidência do ITCD, enquanto os valores de seguro de vida são isentos do imposto.

---

## AMAZONAS (SEFAZ-AM)

### Questão 11
Eduardo Pereira adquiriu um veículo e fez o licenciamento em outro Estado, embora resida em Manaus. Sobre o recolhimento do IPVA no Amazonas, julgue o item:

( ) O proprietário de veículo que reside no Amazonas mas licenciou o veículo em outro Estado deve recolher o IPVA no Estado onde fez o licenciamento, independentemente de seu domicílio real.

### Questão 12
Sobre os benefícios fiscais no Amazonas, julgue o item:

( ) Para fazer jus aos benefícios fiscais no Amazonas, os produtos devem, entre outras condições, contribuir para o incremento do volume de produção industrial, agroindustrial e florestal do Estado e promover investimento em pesquisa e desenvolvimento de tecnologia.

### Questão 13
Acerca do fato gerador do ICMS no Amazonas, julgue o item:

( ) No Amazonas, constitui fato gerador do ICMS a transmissão de propriedade ou de título que a represente, mesmo quando a mercadoria não tiver transitado pelo estabelecimento transmitente.

### Questão 14
Sobre a Zona Franca de Manaus, julgue o item:

( ) Os produtos de pesca provenientes do exterior estão isentos de impostos quando destinados à Zona Franca de Manaus.

### Questão 15
Sobre os incentivos extrafiscais no Amazonas, julgue o item:

( ) Constitui incentivo extrafiscal no Amazonas a concessão de financiamentos diferenciados, enquanto o diferimento, a isenção e o crédito fiscal presumido são classificados como incentivos fiscais.

### Questão 16
Acerca das atividades que podem receber benefícios fiscais no Amazonas, julgue o item:

( ) A fabricação de bebidas alcoólicas industrializadas no interior do Amazonas pode ter direito a benefícios fiscais, desde que utilize insumos produzidos no Estado e esteja em zonas definidas como prioritárias pelo Poder Executivo.

### Questão 17
Sobre o IPVA dos veículos de universidade federal no Amazonas, julgue o item:

( ) Os veículos utilizados nas atividades essenciais de uma universidade federal no Amazonas estão sujeitos à incidência normal de IPVA, não gozando de imunidade recíproca.

### Questão 18
Sobre o prazo para ação judicial visando anular indeferimento de restituição de ICMS no Amazonas, julgue o item:

( ) O prazo para ajuizamento de ação judicial visando anular indeferimento administrativo de pedido de restituição de ICMS é prescricional de 5 anos, admitindo interrupção.

### Questão 19
Acerca da multa por operação não escriturada em livros fiscais no Amazonas, julgue o item:

( ) No Amazonas, a multa aplicada sobre débito de ICMS apurado por operação não escriturada em livros fiscais corresponde a 100% do valor do imposto devido.

### Questão 20
Sobre a isenção de IPVA para táxis no Amazonas, julgue o item:

( ) No Amazonas, o proprietário de quatro veículos licenciados como táxis terá isenção de IPVA apenas em relação a um dos veículos, não se estendendo aos demais.

### Questão 21
Sobre as isenções da Zona Franca de Manaus, julgue o item:

( ) A sociedade empresária que produz bens na Zona Franca de Manaus para comercialização no território nacional tem direito à isenção do IPI e do Imposto de Importação integral.

### Questão 22
Sobre a compensação de ofício de ITBI com IPVA no Amazonas, julgue o item:

( ) A Receita Estadual do Amazonas pode compensar de ofício valores de ITBI pagos a maior com débitos de IPVA do mesmo contribuinte, mesmo que sejam tributos distintos.

### Questão 23
Sobre o ICMS por estimativa no Amazonas, julgue o item:

( ) No Amazonas, é legal a estimativa do ICMS quando o contribuinte apresenta desempenho de recolhimento inferior à média do setor em que atua, podendo o contribuinte impugnar seu enquadramento com obtenção de efeito suspensivo.

### Questão 24
Sobre o ICMS na venda de máquina do ativo imobilizado no Amazonas, julgue o item:

( ) No Amazonas, a sociedade empresária que adquire máquina para o ativo permanente imobilizado e a vende após três anos de uso deve recolher o ICMS integral sobre essa operação, pois o prazo mínimo de manutenção do bem no estabelecimento é superior a três anos.

---

## PIAUÍ (SEFAZ-PI)

### Questão 25
Rodolfo e Fabiana se separaram judicialmente no Piauí com partilha desigual de bens. Sobre o ITCMD no Piauí, julgue o item:

( ) Na separação judicial em que um dos cônjuges recebe bens em valor superior à sua meação, incide ITCMD no Piauí sobre o excedente, sendo o cônjuge beneficiado o contribuinte responsável pelo pagamento.

### Questão 26
Sobre a isenção de ITCMD no Piauí para imóveis, julgue o item:

( ) No Piauí, é isenta de ITCMD a transmissão causa mortis de imóvel rural cuja avaliação seja igual ou inferior a 15.000 UFR/PI, desde que o beneficiário não seja proprietário de outro imóvel rural e não receba mais do que um imóvel por ocasião da transmissão.

### Questão 27
Sobre as taxas estaduais no Piauí, julgue o item:

( ) No Piauí, as taxas estaduais serão pagas, de ordinário, antes da prestação dos serviços administrativos ou judiciários solicitados ou do exercício de direitos ou de atividades sujeitas ao Poder de Polícia.

### Questão 28
Rita efetuou diversas doações em dinheiro à irmã Dalva ao longo de 2012 e 2013 no Piauí. Sobre a obrigação pelo pagamento do ITCMD, julgue o item:

( ) No Piauí, em caso de doações em dinheiro realizadas em parcelas ao longo de exercícios, a obrigação pelo pagamento do ITCMD surge quando o total acumulado das doações em um exercício ultrapassa o limite de isenção, sendo o donatário o responsável pelo pagamento.

### Questão 29
Tiago deu em usufruto imóveis em três Estados diferentes. Sobre o ITCMD no Piauí, julgue o item:

( ) No Piauí, a instituição de usufruto por prazo determinado sobre imóvel localizado em outro Estado não gera ITCMD devido ao Estado do Piauí, ainda que o instituidor seja domiciliado no Piauí.

### Questão 30
O "Hospital de Todas as Curas" no Piauí usufruía indevidamente de isenção de IPVA para ambulâncias. Sobre o lançamento do IPVA sonegado, julgue o item:

( ) No Piauí, quando o fisco comprova que o contribuinte usufruiu indevida e intencionalmente de benefício isencional de IPVA, poderá promover o lançamento de ofício do tributo devido em todo o período da sonegação.

### Questão 31
Lucas adquiriu veículo de passeio e motocicleta usados no Piauí. Sobre o IPVA no Piauí, julgue o item:

( ) No Piauí, o IPVA incidente sobre veículo automotor de passeio novo é calculado aplicando-se a alíquota prevista em lei sobre o valor constante na nota fiscal de aquisição.

### Questão 32
Germano, portador de deficiência física no Piauí, possui diversos veículos. Sobre a isenção de IPVA no Piauí, julgue o item:

( ) No Piauí, o veículo nacional de passeio utilizado por pessoa com deficiência física, mesmo sem adaptações, mas perfeitamente adequado ao tipo de deficiência, faz jus à isenção de IPVA.

### Questão 33
Sobre o Processo Administrativo Fiscal no Piauí, julgue o item:

( ) No Piauí, a decisão de primeira instância do Processo Administrativo Fiscal torna-se definitiva na parte que não for objeto de recurso voluntário ou não estiver sujeita a recurso de ofício.

### Questão 34
Acerca das alíquotas do ICMS no Piauí, julgue o item:

( ) No Piauí, a devolução de mercadoria de origem nacional adquirida de contribuinte de outro Estado para comercialização está sujeita à mesma alíquota interna aplicável às operações com mercadorias nacionais.

---

## ESPÍRITO SANTO (SEFAZ-ES)

### Questão 35
Luís possui uma lancha registrada na Capitania dos Portos no ES. Sobre o IPVA de embarcações no ES, julgue o item:

( ) No Espírito Santo, a propriedade de veículos automotores aquáticos, como lanchas registradas na Capitania dos Portos, constitui fato gerador de IPVA.

### Questão 36
Sobre a incidência de ITCMD no ES, julgue o item:

( ) No Espírito Santo, o ITCMD não incide sobre a renúncia ao legado feita em benefício do monte, sem ressalva ou condição, desde que o legatário não tenha praticado ato que demonstre aceitação.

### Questão 37
Gustavo doou imóvel com reserva de usufruto no ES. Sobre a base de cálculo do ITCMD no ES, julgue o item:

( ) No Espírito Santo, para imóveis urbanos, a SEFAZ poderá estabelecer que, para efeito de base de cálculo do ITCMD, seja utilizado valor não inferior ao fixado para o lançamento do IPTU.

### Questão 38
Sobre o recurso ao Conselho Estadual de Recursos Fiscais no ES, julgue o item:

( ) No Espírito Santo, quando há divergência entre as Câmaras do Conselho Estadual de Recursos Fiscais sobre a interpretação jurídica da questão, cabe incidente de uniformização ao Pleno do CERF.

### Questão 39
Sobre consulta tributária no ES, julgue o item:

( ) No Espírito Santo, a consulta tributária feita por entidade de classe não impede, até o término do prazo fixado na resposta, o início de qualquer procedimento fiscal destinado à apuração de faltas relacionadas com a matéria consultada.

### Questão 40
O frigorífico Carne Boa Ltda. no ES foi considerado devedor contumaz. Sobre as medidas especiais de fiscalização no ES, julgue o item:

( ) No Espírito Santo, uma medida especial de fiscalização passível de aplicação a frigoríficos é o controle eletrônico em relação às entradas e saídas de animais vivos e abatidos.

### Questão 41
Sobre bens apreendidos e declarados abandonados pela SEFAZ-ES, julgue o item:

( ) No Espírito Santo, em relação aos bens e mercadorias declarados abandonados, a SEFAZ-ES fica autorizada a proceder a doação a órgãos oficiais ou a instituições de educação ou de assistência social sem fins lucrativos.

### Questão 42
Sobre a multa por retificação extemporânea de arquivos magnéticos de ICMS no ES, julgue o item:

( ) No Espírito Santo, em regra, a imposição de multa por retificação extemporânea de arquivos magnéticos de ICMS exclui a aplicação de penalidades fixadas para outras infrações verificadas.

### Questão 43
Sobre o REPETRO-SPED no ES, julgue o item:

( ) No Espírito Santo, a sociedade empresária estrangeira contratada para prestar serviços de produção de petróleo na área do pré-sal pode valer-se diretamente do REPETRO-SPED para fins de isenção e redução de base de cálculo de ICMS.

### Questão 44
Sobre o diferencial de alíquota do ICMS no ES, julgue o item:

( ) No Espírito Santo, na aquisição de bem para uso próprio de contribuinte localizado em outro Estado, o fato gerador do diferencial de alíquota do ICMS ocorre na saída do produto do estabelecimento remetente.

---

## RIO GRANDE DO SUL (SEFAZ-RS)

### Questão 45
O Sistema Tributário do Estado do Rio Grande do Sul é regido pela Constituição Federal de 1988 e por normas indicadas na Constituição do Estado.

( ) O Sistema Tributário do Estado do Rio Grande do Sul é regido exclusivamente pela Constituição Estadual, não sendo aplicáveis as normas da Constituição Federal de 1988 em matéria tributária.

### Questão 46
A hipótese de incidência do ICMS do Rio Grande do Sul é uma previsão abstrata contida em lei estadual.

( ) A hipótese de incidência do ICMS no Rio Grande do Sul depende de regulamento do Poder Executivo para produzir efeitos, não bastando a previsão em lei estadual.

### Questão 47
Instituições de educação sem fins lucrativos no RS são isentas do IPVA relativo a seus veículos vinculados às finalidades essenciais.

( ) No Rio Grande do Sul, as instituições de educação sem fins lucrativos gozam de isenção do IPVA relativa a seus veículos automotores, desde que estes estejam relacionados com as finalidades essenciais dessas entidades.

### Questão 48
O proprietário que vende automóvel no RS é solidariamente responsável com o adquirente pelo pagamento do IPVA até o registro da comunicação da transferência.

( ) No Rio Grande do Sul, o proprietário que aliena veículo automotor responde solidariamente com o adquirente pelo pagamento do IPVA até o registro da comunicação da transferência no órgão competente de trânsito.

### Questão 49
No RS, o fato gerador do ITCD relativo ao falecimento de João foi o registro do formal de partilha no cartório de registro de imóveis.

( ) No Rio Grande do Sul, o fato gerador do ITCD, relativo à transmissão causa mortis, ocorre com o registro do formal de partilha no cartório de registro de imóveis.

### Questão 50
Benefícios fiscais oriundos de convênios entre o estado do RS e demais unidades da Federação somente têm eficácia após ratificação da assembleia legislativa do estado.

( ) No Rio Grande do Sul, os benefícios fiscais oriundos de convênios celebrados com outras unidades da Federação somente produzem efeitos após ratificação pela assembleia legislativa estadual.

### Questão 51
A contribuição de melhoria decorrente de serviços públicos compõe o Sistema Tributário do Estado do Rio Grande do Sul.

( ) O Sistema Tributário do Estado do Rio Grande do Sul inclui a contribuição de melhoria como uma de suas espécies tributárias.

### Questão 52
No RS, em relação a serviços de transporte, o tomador de serviço é o responsável contratual pelo pagamento do serviço, desde que não seja o remetente ou o destinatário.

( ) No regulamento do ICMS do Rio Grande do Sul, o tomador de serviço de transporte é considerado responsável contratual pelo pagamento do serviço, exceto quando for o remetente ou o destinatário da mercadoria.

### Questão 53
Bem importado por pessoa física é equiparado a mercadoria apenas se destinado ao consumo no RS.

( ) No Rio Grande do Sul, bem importado por pessoa física é equiparado a mercadoria para fins de incidência do ICMS apenas quando destinado ao consumo.

### Questão 54
O ICMS no RS é cumulativo em operações sucessivas quando se refere à circulação de bens e mercadorias entre estados distintos.

( ) No Rio Grande do Sul, o ICMS incide de forma cumulativa nas operações sucessivas de circulação de mercadorias entre estados distintos, não sendo admitida a compensação do imposto devido com o montante cobrado nas operações anteriores.

### Questão 55
O princípio da essencialidade do ICMS restringe-se aos produtos de primeira necessidade no RS.

( ) No Rio Grande do Sul, o princípio da essencialidade do ICMS aplica-se exclusivamente aos produtos de primeira necessidade, não alcançando bens supérfluos.

### Questão 56
O ICMS não incide em operações de saída que destinem mercadorias a consumidor final no exterior no RS.

( ) No Rio Grande do Sul, o ICMS não incide sobre operações de saída que destinem mercadorias a consumidor final no exterior, sendo assegurado o crédito tributário relacionado ao imposto eventualmente pago em operações anteriores.

### Questão 57
No RS, o fato gerador do IPVA no caso de importação de veículo pelo consumidor ocorre no momento do desembaraço aduaneiro.

( ) No Rio Grande do Sul, na hipótese de importação de veículo pelo consumidor final, o fato gerador do IPVA ocorre no momento do desembaraço aduaneiro.

### Questão 58
No RS, a legislação de IPVA para pessoas com deficiência equipara o autismo à deficiência mental severa.

( ) No Rio Grande do Sul, para fins de isenção do IPVA, a legislação equipara o autismo à deficiência mental severa, caracterizando-o como espécie de deficiência mental.

### Questão 59
No RS, no caso de alienação fiduciária em garantia de veículo automotor, o devedor fiduciante é considerado contribuinte do IPVA.

( ) No Rio Grande do Sul, em caso de alienação fiduciária em garantia de veículo automotor, considera-se contribuinte do IPVA o devedor fiduciante ou o possuidor direto do bem.

### Questão 60
No RS, a base de cálculo do IPVA incidente sobre veículo automotor usado é o valor médio de mercado divulgado anualmente pelo Poder Executivo estadual.

( ) No Rio Grande do Sul, a base de cálculo do IPVA incidente sobre veículo automotor usado corresponde ao valor médio de mercado, conforme anualmente divulgado pelo Poder Executivo estadual antes do início do ano-calendário.

### Questão 61
No RS, para comprovação do pagamento do IPVA, o contribuinte deve conservar no veículo o documento de quitação do imposto referente ao exercício em curso ou, se não esgotado o respectivo prazo de pagamento, o do exercício anterior.

( ) No Rio Grande do Sul, o contribuinte que não esteja desonerado do IPVA está obrigado a conservar no veículo o documento de quitação do imposto referente ao exercício em curso ou, se não esgotado o prazo de pagamento, o do exercício anterior.

### Questão 62
No RS, enquanto não houver o registro da comunicação da alienação do automóvel no órgão público de trânsito, o proprietário que o alienar será solidariamente responsável pelo pagamento do IPVA.

( ) No Rio Grande do Sul, o proprietário de veículo automotor que o alienar será solidariamente responsável pelo pagamento do IPVA enquanto não houver o registro da comunicação da alienação no órgão público de trânsito.

### Questão 63
No RS, a alíquota de IPVA para ônibus e caminhões é menor que aquela aplicável a carros e motocicletas.

( ) No Rio Grande do Sul, a alíquota de IPVA aplicável a ônibus e caminhões é inferior à alíquota incidente sobre automóveis e motocicletas.

### Questão 64
A Lei n.º 14.741/2015 do RS estabeleceu alíquotas progressivas para o ITCD em função das unidades de padrão fiscal (UPF-RS).

( ) No Rio Grande do Sul, a progressividade das alíquotas do ITCD é fixada em função das unidades de padrão fiscal (UPF-RS), cujo valor é o vigente na data da morte ou da doação.

### Questão 65
Segundo a Lei n.º 8.821/1989 do RS, é contribuinte do ITCD o donatário, independentemente do domicílio do doador.

( ) No Rio Grande do Sul, nos termos da Lei n.º 8.821/1989, o donatário é considerado contribuinte do ITCD, independentemente de o doador estar domiciliado ou não no país.

### Questão 66
No RS, nas transmissões decorrentes de doações, ocorrem tantos fatos geradores distintos quantos forem os donatários do bem, título ou crédito.

( ) No Rio Grande do Sul, nas transmissões decorrentes de doações, ocorrem tantos fatos geradores distintos quantos forem os donatários do bem, título ou crédito.

### Questão 67
No RS, em caso de transmissão causa mortis, o critério temporal da hipótese de incidência do ITCD é a data da abertura da sucessão legítima ou testamentária.

( ) No Rio Grande do Sul, para fins de incidência do ITCD na transmissão causa mortis, o critério temporal da hipótese de incidência é a data da abertura da sucessão legítima ou testamentária.

### Questão 68
A taxa de fiscalização e controle dos serviços públicos delegados no RS, incidente sobre o faturamento bruto, foi considerada constitucional pelo STF.

( ) O STF firmou entendimento pela constitucionalidade da taxa de fiscalização e controle dos serviços públicos delegados no Rio Grande do Sul, ainda que sua base de cálculo utilize o faturamento bruto como critério de mensuração.

### Questão 69
No RS, a taxa única de serviços judiciais tem natureza tributária, mas a lei também prevê o pagamento de despesas sem caráter tributário.

( ) No Rio Grande do Sul, a taxa única de serviços judiciais instituída pela Lei n.º 14.634/2014 tem natureza tributária, sendo que a mesma lei prevê despesas sem caráter tributário, como as contraprestações devidas a peritos e assistentes técnicos.

### Questão 70
A taxa incidente sobre unidades de conservação no RS isenta o uso de recursos hídricos legalmente dispensado de outorga.

( ) No Rio Grande do Sul, isenta-se da taxa incidente sobre unidades de conservação, utilização de recursos hídricos e faunísticos e serviços correlatos o uso de recursos hídricos legalmente dispensado de outorga.

---

## GABARITO SUGERIDO

| Questão | Estado | Gabarito |
|---------|--------|----------|
| 1 | MG | E |
| 2 | MG | C |
| 3 | MG | E |
| 4 | MG | C |
| 5 | MG | C |
| 6 | MG | C |
| 7 | MG | C |
| 8 | MG | C |
| 9 | MG | C |
| 10 | MG | E |
| 11 | AM | E |
| 12 | AM | C |
| 13 | AM | E |
| 14 | AM | C |
| 15 | AM | C |
| 16 | AM | C |
| 17 | AM | E |
| 18 | AM | E |
| 19 | AM | E |
| 20 | AM | C |
| 21 | AM | C |
| 22 | AM | C |
| 23 | AM | C |
| 24 | AM | E |
| 25 | PI | C |
| 26 | PI | C |
| 27 | PI | C |
| 28 | PI | C |
| 29 | PI | C |
| 30 | PI | C |
| 31 | PI | C |
| 32 | PI | C |
| 33 | PI | C |
| 34 | PI | E |
| 35 | ES | C |
| 36 | ES | C |
| 37 | ES | C |
| 38 | ES | E |
| 39 | ES | C |
| 40 | ES | C |
| 41 | ES | C |
| 42 | ES | E |
| 43 | ES | E |
| 44 | ES | E |
| 45 | RS | E |
| 46 | RS | E |
| 47 | RS | C |
| 48 | RS | C |
| 49 | RS | E |
| 50 | RS | C |
| 51 | RS | E |
| 52 | RS | C |
| 53 | RS | E |
| 54 | RS | E |
| 55 | RS | E |
| 56 | RS | C |
| 57 | RS | C |
| 58 | RS | C |
| 59 | RS | C |
| 60 | RS | C |
| 61 | RS | C |
| 62 | RS | C |
| 63 | RS | C |
| 64 | RS | C |
| 65 | RS | C |
| 66 | RS | C |
| 67 | RS | C |
| 68 | RS | E |
| 69 | RS | C |
| 70 | RS | C |

---

**Legenda:** C = Certo | E = Errado

**Total: 70 questões de Legislação Tributária Estadual transformadas em Certo/Errado**
