# Crawler de dados financeiros

Projeto desenvolvido como desafio na etapa prática de um processo seletivo para **desenvolvedor Python**. O objetivo do desafio é extrair informações.

### Objetivos

A idéia é extrair dados abertos da SUSEP (Superintendência de Seguros Privados). O desafio é dividido nas seguintes etapas:

1. Obter uma massa de dados no formato `JSON` em https://dados.gov.br/dataset/consulta-de-produtos
2. Filtrar apenas os itens onde o campo `tipoproduto` é `"PLANO DE PREVIDÊNCIA"`
3. Baixar o regulamento (PDF) referente a cada processo filtrado em http://www.susep.gov.br/menu/consulta-de-produtos-1
4. Extrair do arquivo PDF uma série de dados, como _Taxa de Juros_, _Taxa de Carregamento_, _Status do processo_, etc.
5. Os dados extraídos devem ser salvos em um novo arquivo `JSON`

### Solução

Para ver a solução, clique [aqui](./projeto).

---
Made with :heart: by [@jjpaulo2](https://github.com/jjpaulo2)