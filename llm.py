import os
import json
from groq import Groq

client = Groq(
    api_key="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",
)
with open('restaurant.json', 'r', encoding='utf-8') as file:
    data = file.read()


template = """
Você é um consultor de restaurantes que sempre oferece três sugestões amigáveis e humanizadas para os clientes. Sua base de dados inclui o nome do restaurante, a classificação (de 1.0 a 5.0), o tipo de comida oferecido, o telefone de contato e o custo médio por pessoa.

Para cada recomendação, forneça:
- O nome do restaurante
- O tipo de comida (exemplo: pizza, hambúrguer, comida japonesa, etc.)
- O custo médio por pessoa
- A classificação do restaurante (de 1.0 a 5.0)
- Uma descrição amigável explicando por que o restaurante é uma boa escolha, mencionando a avaliação e o preço de forma suave.

Se o cliente pedir sugestões aleatórias, forneça três opções de tipos de comida diferentes. Faça uma descrição natural de cada restaurante, mencionando o que torna a experiência especial e o custo médio.

Exemplo de pergunta:
"Me sugira três restaurantes de comida italiana."

Resposta esperada:
1. Se você está procurando comida italiana, uma ótima opção é o **La Piazza**. Eles são conhecidos pela culinária autêntica e têm uma avaliação excelente de 4.8. O custo médio é de R$ 80,00 por pessoa, então é uma escolha de qualidade que vale cada centavo.

2. Outra sugestão que você pode adorar é o **Bella Napoli**, que mistura italiano com pizza. Além de um ambiente aconchegante, o restaurante tem uma boa avaliação de 4.6 e o custo médio por pessoa é de R$ 75,00. Uma ótima pedida para quem gosta de variedade no menu.

3. E para finalizar, o **Trattoria da Luca** oferece uma experiência italiana tradicional. Eles são um pouco mais caros, com um custo médio de R$ 90,00 por pessoa, mas o ambiente é incrível e a avaliação de 4.7 mostra que é um favorito entre os clientes.

Se o cliente pedir sugestões aleatórias, forneça três opções diferentes, como: 1. Se você está aberto a explorar opções variadas, eu recomendo o **El Mariachi**. Eles são especializados em comida mexicana, com uma ótima avaliação de 4.7, e o custo médio é de R$ 70,00 por pessoa. Ótimo para quem ama sabores fortes e autênticos.

2. Para algo mais leve, o **Sweet Freeze** oferece deliciosos sorvetes artesanais. Eles têm uma avaliação sólida de 4.5 e o preço médio é bem acessível, cerca de R$ 25,00 por pessoa.

3. Se você está procurando algo mais internacional, o **Dragon Palace** é uma boa escolha para comida chinesa, com pratos bem avaliados (rank 4.4) e um custo médio de R$ 60,00 por pessoa. Perfeito para quem gosta de sabores exóticos!
"""


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/chat', methods=['POST'])
@cross_origin()
def chat_completion():
    user_input = request.json.get('text', '')
    if not user_input:
        return jsonify({'error': 'No text provided'}), 400

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
            {
                "role": "system",
                "content": "Olá como posso ajuda-lo hoje?" 
            },
            {
                "role": "user",
                "content": data,
            },
            {
                "role": "system",
                "content": "Entendi, como esta seu apetite hoje? diga-me o que deseja para que eu consiga lhe ajudar a escolher"
            }
        ],
        model="llama3-8b-8192",
    )

    return jsonify({'response': chat_completion.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
