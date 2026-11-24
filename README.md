# 🤖 Automatizador de Códigos Anónimos - SIGA UNI

Este script automatiza la asignación de **Códigos Anónimos** en el sistema SIGA. Lee el acta en PDF descargada del sistema, extrae los códigos de los alumnos y los cruza con el código anónimo para ingresarlos automáticamente en el formulario web. Ahorra tiempo y evita errores de tipeo.

---

## 🛠️ Requisitos Previos (Instalación en una máquina nueva)

Para que el script funcione, necesitas tener instalado lo siguiente:

1. **Python (3.10 o superior)**: Descárgalo de [python.org](https://www.python.org/downloads/). 
   * *IMPORTANTE: Durante la instalación, marca la casilla que dice "Add Python to PATH" antes de darle a instalar.*
2. **Google Chrome**: Navegador web (asegúrate de tenerlo actualizado).
3. **Visual Studio Code (VS Code)**: Recomendado para ejecutar el script fácilmente.

### 📦 Instalación de Librerías
Abre la terminal de VS Code (`Ctrl + ñ` en Windows) y ejecuta este comando para instalar las herramientas necesarias:
```bash
pip install selenium webdriver-manager pdfplumber
---
📁 sistema_codigo_anonimos/
 ┣ 📁 Actas_PDF/               <-- Aquí guardarás los PDFs
 ┣ 📄 automatizar_pdf_final.py <-- El script principal
 ┣ 📄 AbrirChromeSIGA.bat      <-- El lanzador (lo crearás en el paso 2)
 ┗ 📄 README.md                <-- Este archivo
