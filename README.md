# MarIA - Asistente de Navegación Web Inteligente



## Descripción

MarIA es un asistente de navegación web inteligente construido con Python que combina reconocimiento de voz, síntesis de voz y modelos de lenguaje de gran escala (LLM) para proporcionar una experiencia de navegación web controlada por voz. Permite a los usuarios interactuar con Microsoft Edge mediante comandos de voz o texto, navegar por páginas web, realizar búsquedas, y automatizar interacciones con elementos de las páginas.

## Características principales

- 🗣️ **Interacción por voz**: Control completo del navegador mediante comandos de voz en español
- 🌐 **Control del navegador**: Abrir/cerrar Edge, gestionar pestañas, navegación básica
- 🔍 **Búsqueda web**: Realizar búsquedas y seleccionar resultados específicos
- 🤖 **Automatización**: Interacción con elementos de páginas web (botones, enlaces, formularios)
- 📝 **Resumen de contenido**: Generación de resúmenes de páginas web
- 📊 **Historial de acciones**: Registro de todas las acciones realizadas

## Componentes del proyecto

- **MarIA.py**: Núcleo principal que coordina el reconocimiento de voz, la toma de decisiones y la ejecución de acciones
- **metodosMarIA.py**: Implementación de los métodos de automatización del navegador usando Selenium
- **HablarMarIA.py**: Interfaz gráfica para interactuar con MarIA mediante texto o voz
- **hablarModeloHistorial.py**: Utilidad para mantener conversaciones con el modelo con historial

## Requisitos previos

### Software
- Python 3.8+
- Microsoft Edge
- [Ollama](https://ollama.ai/) con los siguientes modelos:
  - `deepseek-r1:14b`
  - `llama3.1:8b`
  - `MarIA` (modelo personalizado o configurado en Ollama)

### Dependencias de Python
```
selenium
beautifulsoup4
pyttsx3
speech_recognition
transformers
pydantic
tkinter
pillow
ollama
```

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tuusuario/MarIA.git
cd MarIA
```

2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

3. Asegúrate de tener instalados los modelos necesarios en Ollama:
```bash
ollama pull deepseek-r1:14b
ollama pull llama3.1:8b
# Configura tu modelo MarIA personalizado
```

4. Descargar el driver de Edge correspondiente a tu versión del navegador y colocarlo en la carpeta `Drivers/Edge/`

## Estructura de archivos

```
MarIA/
├── Drivers/
│   └── Edge/
│       └── msedgedriver.exe
├── Fotos/
│   └── MarIA_Logo.png
├── MarIA.py
├── metodosMarIA.py
├── HablarMarIA.py
├── hablarModeloHistorial.py
├── .gitignore
└── README.md
```

## Uso

### Interfaz gráfica

Para iniciar la interfaz gráfica:

```bash
python HablarMarIA.py
```

Esto abrirá una ventana donde podrás interactuar con MarIA mediante texto o voz.

### Mediante línea de comandos

Para usar directamente la versión de línea de comandos:

```bash
python MarIA.py
```

## Comandos de ejemplo

MarIA puede entender y ejecutar una variedad de comandos, como:

- "Abre el navegador"
- "Busca información sobre inteligencia artificial"
- "Resume esta página"
- "Abre una nueva pestaña y ve a wikipedia.org"
- "Haz clic en el tercer resultado"
- "Cierra esta pestaña"
- "Haz clic en el botón de inicio de sesión"

## Contribución

Las contribuciones son bienvenidas. Por favor, considera seguir estos pasos:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añade nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia

[MIT](LICENSE)

## Contacto

[Pablo Lanero] - [pablolaneroperez@gmail.com]

---

**Nota**: Este proyecto se encuentra en desarrollo activo. Algunas características pueden no estar completamente implementadas o contener errores.
