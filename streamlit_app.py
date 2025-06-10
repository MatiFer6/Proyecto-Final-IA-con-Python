import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi Chatbot",
                   page_icon="🤖",
                   layout= "centered",
                   initial_sidebar_state="expanded")
st.title(body="Mi Chatbot con Streamlit 🤖")

modelos = [
    'llama3-8b-8192', # tiene 8 billones de parámetros
    'llama3-70b-8192', # tiene 70 billones de parámetros
    'mixtral-8x7b-32768' #tiene 7 billones de parámetros x 8
    ]
modelo_elegido = st.sidebar.selectbox("Seleccioná un modelo", modelos)

# Función para crear usuario de Groq
def crear_usuario_groq():
    clave_secreta = st.secrets["Clave_API"]
    return Groq(api_key = clave_secreta)

# Cache e inicio de estado de la sesión
# Para poder recordar los mensajes anteriores usamos los estados de la sesión.
# Ahora vamos a crear una función para inicializar estos estados de la sesión
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# Función que va actualizando el historial a medida que el chat avanza
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

# Función que muestre el historial
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]): st.markdown(mensaje["content"])
            
# Función para determinar un área de chat (espacio en donde se muestra el historial)
def area_chat():
    contenedorChat = st.container(height = 400, border = True)
    with contenedorChat: mostrar_historial()
    
def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribí un mensaje! ")
    if mensaje:
        actualizar_historial("user", mensaje, "🧑🏻")
        with st.chat_message("assistant", avatar = "🤖"):
            mensaje_respuesta = st.empty
            respuesta_completa = ""
        # Posibilidad de usar stream True
        respuesta_stream = clienteUsuario.chat.completions.create(
            model = modelo_elegido,
            messages = [{"role": "user", "content": mensaje}],
            stream = True
        )
        
        for frase in respuesta_stream:
            if frase.choices[0].delta.content:
                respuesta_completa += frase.choices[0].delta.content
        st.markdown(respuesta_completa)
    
        actualizar_historial("assistant", respuesta_completa, "🤖")
        st.rerun()
        
if __name__ == "__main__":
    main()