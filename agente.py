import anthropic
import os
from dotenv import load_dotenv
from tools import (
    menor_custo_por_lead,
    melhor_engajamento,
    analisar_fechamentos,
    calcular_roi,
    resumo_semanal
)

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "menor_custo_por_lead",
        "description": "Analisa qual campanha teve o menor custo por lead em média. Use quando o usuário perguntar sobre eficiência de custo, CPL ou custo por lead.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "melhor_engajamento",
        "description": "Retorna qual campanha teve mais cliques e visualizações no total. Use quando perguntarem sobre alcance, engajamento, cliques ou visualizações.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "analisar_fechamentos",
        "description": "Mostra quantos fechamentos cada campanha gerou no total. Use quando perguntarem sobre conversões, fechamentos ou clientes gerados.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "calcular_roi",
        "description": "Calcula o ROI de cada campanha comparando investimento e receita gerada. Use quando perguntarem sobre ROI, retorno, lucro ou comparação entre campanhas.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "resumo_semanal",
        "description": "Mostra o resumo por semana com investimento, leads, fechamentos e receita. Use quando perguntarem sobre desempenho semanal ou evolução por semana.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }
]
def executar_tool(nome, inputs):
    if nome == "menor_custo_por_lead":
        return menor_custo_por_lead()
    elif nome == "melhor_engajamento":
        return melhor_engajamento()
    elif nome == "analisar_fechamentos":
        return analisar_fechamentos()
    elif nome == "calcular_roi":
        return calcular_roi()
    elif nome == "resumo_semanal":
        return resumo_semanal()
    else:
        return "Tool não encontrada."
def main():
    print("Agente de Marketing iniciado. Digite 'sair' para encerrar.\n")
    historico = []
    while True:
        usuario = input("Você: ").strip()
        
        if usuario.lower() == "sair":
            print("Encerrando agente.")
            break
            
        if not usuario:
            continue

        historico.append({"role": "user", "content": usuario})

        resposta = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system="Você é um assistente especialista em análise de campanhas de marketing digital. Responda sempre em português brasileiro. Quando precisar de dados reais, use as tools disponíveis.",
            tools=tools,
            messages=historico
        )

        if resposta.stop_reason == "tool_use":
            tool_block = next(b for b in resposta.content if b.type == "tool_use")
            nome_tool = tool_block.name
            inputs = tool_block.input
            
            print(f"\n[Agente usando tool: {nome_tool}]\n")
            
            resultado = executar_tool(nome_tool, inputs)

            historico.append({"role": "assistant", "content": resposta.content})
            historico.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": resultado
                }]
            })

            resposta_final = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                system="Você é um assistente especialista em análise de campanhas de marketing digital. Responda sempre em português brasileiro. Quando precisar de dados reais, use as tools disponíveis.",
                tools=tools,
                messages=historico
            )

            assistente_texto = resposta_final.content[0].text
            historico.append({"role": "assistant", "content": assistente_texto})

        else:
            assistente_texto = resposta.content[0].text
            historico.append({"role": "assistant", "content": assistente_texto})

        print(f"Agente: {assistente_texto}\n")

if __name__ == "__main__":
    main()