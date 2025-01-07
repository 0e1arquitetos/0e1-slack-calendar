import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Configuração da API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Obter as credenciais e o ID do calendário do ambiente
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")  # Credenciais como string JSON
CALENDAR_ID = os.getenv("CALENDAR_ID")  # ID do calendário

if not GOOGLE_CREDENTIALS:
    raise ValueError("As credenciais do Google não foram encontradas no ambiente.")
if not CALENDAR_ID:
    raise ValueError("O ID do calendário não foi encontrado no ambiente.")

credentials_info = json.loads(GOOGLE_CREDENTIALS)
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

# Conectar ao serviço do Google Calendar
service = build('calendar', 'v3', credentials=credentials)

# Função para listar eventos
def listar_eventos():
    # Tempo atual e final para busca
    now = datetime.utcnow().isoformat() + 'Z'  # Formato ISO 8601 UTC
    end = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'  # Próximos 30 dias

    print(f"Listando eventos de {CALENDAR_ID} entre {now} e {end}...\n")

    # Solicitação à API
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    # Listar eventos encontrados
    if not events:
        print("Nenhum evento encontrado.")
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start} - {event['summary']}")

# Chamar a função
listar_eventos()
