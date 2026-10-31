import streamlit as st
from config.conexion import obtener_conexion


def mostrar_productos():
    st.header("Productos")
    st.write("Catálogo de productos de las tiendas minoristas.")

    # ---------- Formulario para registrar un producto ----------
    with st.form("form_producto"):
        nombre = st.text_input("Nombre del producto")
        categoria = st.text_input("Categoría")
        precio = st.number_input(
            "Precio (USD)",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )
        guardar = st.form_submit_button("Guardar producto")

        if guardar:
            if nombre.strip() == "":
                st.warning("Debe ingresar el nombre del producto.")
            else:
                conexion = None
                cursor = None
                try:
                    conexion = obtener_conexion()
                    if conexion is None:
                        return
                    cursor = conexion.cursor()
                    consulta = """
                        INSERT INTO PRODUCTO
                        (Nombre, Categoria, Precio)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(
                        consulta,
                        (nombre, categoria, float(precio))
                    )
                    conexion.commit()
                    st.success("Producto registrado correctamente.")
                except Exception as error:
                    if conexion is not None:
                        conexion.rollback()
                    st.error(f"Error al registrar el producto: {error}")
                finally:
                    if cursor is not None:
                        cursor.close()
                    if conexion is not None and conexion.is_connected():
                        conexion.close()

    # ---------- Listado de productos ----------
    st.subheader("Listado de productos")
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT Id_Producto, Nombre, Categoria, Precio "
            "FROM PRODUCTO ORDER BY Id_Producto DESC"
        )
        filas = cursor.fetchall()
        if filas:
            st.dataframe(
                [
                    {
                        "ID": f[0],
                        "Producto": f[1],
                        "Categoría": f[2],
                        "Precio": float(f[3]),
                    }
                    for f in filas
                ],
                use_container_width=True,
            )
        else:
            st.info("Aún no hay productos registrados.")
    except Exception as error:
        st.error(f"Error al consultar los productos: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
