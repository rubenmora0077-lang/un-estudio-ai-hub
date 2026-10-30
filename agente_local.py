import os
from crewai import Agent, Crew, Process, Task

# 1. Tu API Key de Google Gemini
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# 2. Modelo vigente indicado por la API
modelo = "gemini/gemini-3.8-flash"

# 3. Agente Investigador
investigador = Agent(
    role="Investigador",
    goal="Sintetizar 3 puntos clave sobre IA de forma rápida y clara",
    backstory="Eres un analista directo y conciso.",
    verbose=True,
    llm=modelo,
)

# 4. Agente Redactor
redactor = Agent(
    role="Redactor",
    goal="Redactar un correo corto basado en la investigación",
    backstory="Eres un redactor ejecutivo muy directo.",
    verbose=True,
    llm=modelo,
)

# 5. Tareas del equipo
tarea1 = Task(
    description=(
        "Menciona brevemente 3 tendencias clave de la Inteligencia Artificial."
    ),
    expected_output="Una lista corta con 3 tendencias.",
    agent=investigador,
)

tarea2 = Task(
    description=(
        "Toma los puntos anteriores y redacta un correo de saludo profesional de"
        " 3 líneas."
    ),
    expected_output="Un correo corto y profesional.",
    agent=redactor,
)

# 6. Configurar y ejecutar el equipo
equipo = Crew(
    agents=[investigador, redactor],
    tasks=[tarea1, tarea2],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print("\n🚀 Iniciando el equipo con Gemini 3.8 Flash...")
    resultado = equipo.kickoff()
    print("\n\n########################")
    print("RESULTADO FINAL:")
    print(resultado)