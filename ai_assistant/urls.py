from django.urls import path
from ai_assistant.views import *

app_name = "ai_assistant"

urlpatterns = [
    path("", ai_assistant_dashboard, name="dashboard"),
    path("dispute-summary/", dispute_summary_assistant, name="dispute_summary"),
    path("settlement-draft/", settlement_drafting, name="settlement_draft"),
    path("translation/", translation_assistant, name="translation"),
    path("history/", ai_session_history, name="history"),
    path("<int:session_id>/review/", ai_session_review, name="review"),
]
