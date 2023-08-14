# Sistema de Cadastro e Gerenciamento de Usuários

Este é um projeto de um sistema de cadastro e gerenciamento de usuários desenvolvido em Flask, uma estrutura web em Python. O sistema permite que os usuários se cadastrem, forneçam informações pessoais e endereço, e gerenciem sua senha. Além disso, o projeto inclui funcionalidades de geração de PDF com os dados do cadastro e exibição de gráficos estatísticos.

## Funcionalidades

- Cadastro de Usuários: Os usuários podem se cadastrar fornecendo informações como nome, email, telefone, data de nascimento, gênero e CPF.

- Cadastro de Endereço: Após o cadastro inicial, os usuários podem adicionar informações de endereço, incluindo rua, número, cidade e estado.

- Alteração de Senha: Os usuários têm a opção de alterar sua senha a qualquer momento.

- Geração de PDF: Os dados do cadastro dos usuários podem ser exportados para um arquivo PDF.

- Estatísticas: O sistema exibe estatísticas de cadastros por estado em forma de gráfico.

## Requisitos

- Python 3.x
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Mail
- WTForms
- ReportLab
- Matplotlib

## Instalação

1. Clone este repositório para o seu computador.
2. Crie e ative um ambiente virtual (opcional, mas recomendado).
3. Instale as dependências usando o seguinte comando:

    pip install -r requisitos.txt 


4. Execute o aplicativo com o seguinte comando:

python app.py

5. Acesse o aplicativo no seu navegador em http://127.0.0.1:5000/.

## Como Contribuir

Se você gostaria de contribuir para este projeto, siga as etapas abaixo:

1. Faça um fork deste repositório.
2. Crie um novo branch para a sua contribuição:

    git checkout -b minha-contribuicao

3. Faça as alterações desejadas.
4. Faça o commit das suas alterações:

    git commit -m "Minha contribuição: Adicionei recurso XYZ" 


5. Faça o push para o seu repositório fork:

    git push origin minha-contribuicao


6. Abra um Pull Request neste repositório.

## Autor

Icaro Henrique Nunes Viana Silva
icaro_henrique18@hotmail.com

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.





