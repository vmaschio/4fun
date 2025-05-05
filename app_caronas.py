import streamlit as st
import json
import os
from datetime import datetime

ARQUIVO_CARONAS = 'caronas.json'
DATA_EVENTO = '30/05/2025'
DESTINO = 'Campos do Jordão - SP'

# Configuração do tema e estilo
st.set_page_config(
    page_title="Caronas para Campos do Jordão",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def carregar_caronas():
    if os.path.exists(ARQUIVO_CARONAS):
        with open(ARQUIVO_CARONAS, 'r') as f:
            return json.load(f)
    return []

def salvar_caronas(caronas):
    with open(ARQUIVO_CARONAS, 'w') as f:
        json.dump(caronas, f, indent=4)

def exibir_carona_card(carona, index):
    vagas_disponiveis = carona["vagas"] - len(carona["ocupantes"])
    st.markdown(f"""
        <div class="card">
            <h3>Carona #{index+1}</h3>
            <p><strong>🧍‍♂️ Motorista:</strong> {carona['motorista']}</p>
            <p><strong>🕒 Horário:</strong> {carona['hora_saida']}</p>
            <p><strong>📍 Origem:</strong> {carona['origem']}</p>
            <p><strong>🚘 Vagas:</strong> {vagas_disponiveis}/{carona['vagas']}</p>
            <p><strong>👥 Ocupantes:</strong> {", ".join(carona['ocupantes']) if carona['ocupantes'] else "Nenhum ainda"}</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown(f"""
        <div class="header">
            <h1>🚗 Caronas para Campos do Jordão</h1>
            <h3>📅 {DATA_EVENTO}</h3>
        </div>
    """, unsafe_allow_html=True)

    caronas = carregar_caronas()

    # Sidebar para navegação
    with st.sidebar:
        st.markdown("### 📱 Menu")
        menu = st.radio("", [
            "Ver caronas disponíveis",
            "Entrar em uma carona",
            "Oferecer carona",
            "Excluir minha carona"
        ])

    # Conteúdo principal
    if menu == "Ver caronas disponíveis":
        st.markdown("### 🧾 Caronas Disponíveis")
        if not caronas:
            st.info("Ainda não há caronas cadastradas.")
        else:
            for i, carona in enumerate(caronas):
                exibir_carona_card(carona, i)

    elif menu == "Entrar em uma carona":
        st.markdown("### 🙋‍♂️ Entrar em uma Carona")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            nome = st.text_input("Seu nome")
        
        if not caronas:
            st.info("Ainda não há caronas disponíveis.")
        else:
            opcoes = []
            for i, carona in enumerate(caronas):
                vagas_disponiveis = carona["vagas"] - len(carona["ocupantes"])
                if vagas_disponiveis > 0:
                    descricao = f"{carona['motorista']} - {carona['hora_saida']} - {carona['origem']} ({vagas_disponiveis} vagas)"
                    opcoes.append((i, descricao))

            if opcoes:
                escolha = st.selectbox("Escolha uma carona disponível", [desc for _, desc in opcoes])
                if st.button("Entrar na carona"):
                    index = [i for i, desc in opcoes if desc == escolha][0]
                    if nome and nome not in caronas[index]['ocupantes']:
                        caronas[index]['ocupantes'].append(nome)
                        salvar_caronas(caronas)
                        st.markdown('<div class="success-message">✅ Você entrou na carona com sucesso!</div>', unsafe_allow_html=True)
                    elif nome in caronas[index]['ocupantes']:
                        st.markdown('<div class="error-message">⚠️ Você já está nesta carona.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Por favor, insira seu nome.</div>', unsafe_allow_html=True)
            else:
                st.info("Todas as caronas estão completas.")

    elif menu == "Oferecer carona":
        st.markdown("### 🚘 Oferecer Carona")
        col1, col2 = st.columns(2)
        
        with col1:
            motorista = st.text_input("Seu nome (motorista)")
            hora_saida = st.time_input("Horário de saída")
        
        with col2:
            origem = st.text_input("De onde você sairá?")
            vagas = st.slider("Quantas vagas deseja oferecer?", 1, 4, 1)

        if st.button("Cadastrar carona"):
            if motorista and origem:
                nova_carona = {
                    "motorista": motorista,
                    "hora_saida": hora_saida.strftime("%H:%M"),
                    "origem": origem,
                    "vagas": vagas,
                    "ocupantes": []
                }
                caronas.append(nova_carona)
                salvar_caronas(caronas)
                st.markdown('<div class="success-message">✅ Carona cadastrada com sucesso!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-message">❌ Por favor, preencha todos os campos obrigatórios.</div>', unsafe_allow_html=True)

    elif menu == "Excluir minha carona":
        st.markdown("### ❌ Excluir Minha Carona")
        nome_motorista = st.text_input("Digite seu nome (motorista)")
        caronas_usuario = [(i, carona) for i, carona in enumerate(caronas) if carona['motorista'] == nome_motorista]

        if nome_motorista:
            if not caronas_usuario:
                st.info("Você não possui caronas cadastradas.")
            else:
                opcoes = [f"{c['hora_saida']} - {c['origem']} ({len(c['ocupantes'])}/{c['vagas']} ocupantes)" for _, c in caronas_usuario]
                escolha = st.selectbox("Selecione a carona para excluir", opcoes)
                if st.button("Excluir carona"):
                    index = caronas_usuario[opcoes.index(escolha)][0]
                    caronas.pop(index)
                    salvar_caronas(caronas)
                    st.markdown('<div class="success-message">✅ Carona excluída com sucesso!</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
