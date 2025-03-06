from groq import Groq
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa o cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define o prompt para gerar os dados
prompt = """Gere exatamente 10 observações de dados sintéticos no seguinte formato JSON, sem nenhum texto adicional:
{
  "data": [
    {
      "socioeconomic_score": 75.5,
      "study_hours": 6.2,
      "sleep_hours": 7.5,
      "attendance": 85.0,
      "grades": 82.3
    },
    ... mais registros ...
  ]
}

Os valores devem seguir estas regras:
- socioeconomic_score: número entre 0 e 100
- study_hours: número entre 0 e 12
- sleep_hours: número entre 4 e 12
- attendance: número entre 0 e 100
- grades: número entre 0 e 100

IMPORTANTE: Retorne apenas o JSON válido, sem nenhum texto ou explicação."""

def gerar_lote_dados(tamanho=10):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.7,
    )
        
    response = chat_completion.choices[0].message.content
    
    # Remove possíveis caracteres de formatação ou markdown
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    if response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
    
    response = response.strip()
    
    print("Resposta recebida:")
    print(response)
    print("\n---\n")
    
    return json.loads(response)

def combinar_dados(num_total_registros=3000, tamanho_lote=10):
    todos_dados = {"data": []}
    
    lotes_necessarios = num_total_registros // tamanho_lote
    
    for i in range(lotes_necessarios):
        try:
            print(f"Gerando lote {i+1}/{lotes_necessarios}")
            lote = gerar_lote_dados(tamanho_lote)
            todos_dados["data"].extend(lote["data"])
            print(f"Total de registros até agora: {len(todos_dados['data'])}")
        except Exception as e:
            print(f"Erro ao gerar lote {i+1}: {e}")
            continue
            
        # Salva o progresso parcial
        with open('dados_estudantes.json', 'w', encoding='utf-8') as f:
            json.dump(todos_dados, f, ensure_ascii=False, indent=2)
    
    return todos_dados

try:
    # Gera os dados em lotes
    dados_completos = combinar_dados(num_total_registros=3000, tamanho_lote=10)
    
    # Salva os dados finais
    with open('dados_estudantes.json', 'w', encoding='utf-8') as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=2)
    
    print(f"\nProcesso finalizado!")
    print(f"Total de registros gerados: {len(dados_completos['data'])}")
    print("Dados salvos em 'dados_estudantes.json'")

except Exception as e:
    print(f"Erro durante a execução: {e}")