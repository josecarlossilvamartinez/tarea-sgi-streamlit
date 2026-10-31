import streamlit as st
from modulos.login import login
from modulos.VENTAS import mostrar_venta
from modulos.productos import mostrar_productos

# Inicializar variables de sesión
if "sesion_iniciada" not in st.session_state:
    st.session_state["sesion_iniciada"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

if st.session_state["sesion_iniciada"]:
    st.sidebar.title("Menú")
    st.sidebar.write(f"Usuario: {st.session_state['usuario']}")

    opciones = [
        "Ventas",
        "Productos",
        "Información"
    ]
    seleccion = st.sidebar.selectbox("Seleccione una opción", opciones)

    if seleccion == "Ventas":
        mostrar_venta()
    elif seleccion == "Productos":
        mostrar_productos()
    elif seleccion == "Información":
        st.header("Información del sistema")
        st.write(
            "Aplicación desarrollada durante "
            "el Laboratorio de SGI."
        )

    if st.sidebar.button("Cerrar sesión"):
        st.session_state["sesion_iniciada"] = False
        st.session_state["usuario"] = ""
        st.rerun()
else:
    login()
