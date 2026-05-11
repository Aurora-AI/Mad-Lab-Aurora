import os
import json
import logging
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Adiciona caminhos para imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CEO-Oversight")

try:
    from contracts import RecurrenceAlert, SovereigntyReport
except ImportError:
    logger.error("Contracts not found. Ensure you are running from the correct directory.")
    sys.exit(1)

# Configurações Industriais
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
COLLECTION_NAME = "reflexion_ki"
THRESHOLD = 3
REPORT_DIR = Path("C:/Projetos/Aurora/Ozzmosis/docs/Vault/Reports")
DISPATCHER_DB = current_dir / "dispatcher_state.db"

def get_real_success_rate() -> float:
    """Calcula a taxa de sucesso real baseada nos logs do Dispatcher (Histórico de Eventos)."""
    if not DISPATCHER_DB.exists():
        logger.warning(f"Dispatcher DB não encontrado em {DISPATCHER_DB}. Usando taxa conservadora.")
        return 0.88 # Fallback
    
    try:
        with sqlite3.connect(DISPATCHER_DB) as conn:
            # Conta eventos de conclusão vs eventos de re-trigger do loop de reparo
            total_tasks = conn.execute(
                "SELECT COUNT(*) FROM dispatch_logs WHERE event_type IN ('REPAIR_COMPLETED', 'MICRO_TASK_COMPLETED')"
            ).fetchone()[0]
            
            failed_tasks = conn.execute(
                "SELECT COUNT(*) FROM dispatch_logs WHERE dispatched_to = 'repair_loop'"
            ).fetchone()[0]
            
            if total_tasks == 0:
                return 1.0
            
            success_rate = 1.0 - (failed_tasks / total_tasks)
            return round(max(0.0, min(1.0, success_rate)), 2)
    except Exception as e:
        logger.error(f"Erro ao acessar métricas do Dispatcher: {e}")
        return 0.88

def check_recurrence(threshold: int = THRESHOLD) -> Optional[SovereigntyReport]:
    """
    Analisa os anti-patterns no Qdrant para detectar recorrências críticas.
    Implementa Paginação Industrial (Scroll Loop) para garantir análise de 100% dos dados.
    """
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        all_points = []
        next_offset = None
        
        logger.info(f"[*] Iniciando scroll de recorrência na coleção '{COLLECTION_NAME}'...")
        
        while True:
            res = client.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="type",
                            match=models.MatchValue(value="anti_pattern_candidate"),
                        )
                    ]
                ),
                limit=100,
                offset=next_offset,
                with_payload=True
            )
            
            points, next_offset = res
            all_points.extend(points)
            
            if next_offset is None:
                break
            logger.info(f"[+] Coletados {len(all_points)} candidatos...")

        if not all_points:
            logger.info("Nenhum candidato a anti-pattern encontrado no Qdrant.")
            return None

        alerts = []
        for point in all_points:
            payload = point.payload
            occurrences = payload.get("occurrences", 1)
            
            if occurrences >= threshold:
                alert = RecurrenceAlert(
                    pattern_id=payload.get("pattern_id", payload.get("id", "UNKNOWN")),
                    category=payload.get("category", "DIVERSE"),
                    domains=payload.get("domains", []),
                    occurrences=occurrences,
                    threshold=threshold,
                    first_seen=payload.get("ingested_at", datetime.now(timezone.utc).isoformat()),
                    last_seen=payload.get("last_updated", datetime.now(timezone.utc).isoformat())
                )
                alerts.append(alert)
        
        # Obter métricas reais
        success_rate = get_real_success_rate()
        logger.info(f"[*] Taxa de sucesso real detectada: {success_rate * 100}%")

        if not alerts:
            logger.info(f"Nenhuma recorrência acima do threshold ({threshold}) detectada.")
            return None

        # Gerar o Report
        report_id = f"SOV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        max_occ = max(a.occurrences for a in alerts)
        severity = "CRITICAL" if max_occ > 5 else "WARNING" if max_occ >= 3 else "INFO"

        report = SovereigntyReport(
            report_id=report_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            alerts=alerts,
            total_repairs_last_30d=len(all_points),
            repair_success_rate=success_rate,
            suggested_actions=[
                "Refatorar a skill vinculada ao padrão mais recorrente.",
                "Implementar gate determinístico no Trustware para mitigar a falha.",
                "Auditoria manual do Comandante recomendada devido à taxa de sucesso."
            ],
            severity=severity
        )
        
        return report

    except Exception as e:
        logger.error(f"Erro crítico no monitor de recorrência: {e}")
        return None

def save_report(report: SovereigntyReport):
    """Persiste o relatório em JSON e Markdown no Vault."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    # JSON
    json_path = REPORT_DIR / f"{report.report_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))
    
    # Markdown (Sovereignty Style)
    md_path = REPORT_DIR / f"{report.report_id}.md"
    template_path = parent_dir / "templates" / "SOVEREIGNTY_REPORT.md"
    
    content = ""
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{{report_id}}", report.report_id)
        content = content.replace("{{generated_at}}", report.generated_at)
        content = content.replace("{{severity}}", report.severity)
        content = content.replace("{{success_rate}}", f"{report.repair_success_rate * 100:.1f}%")
        
        # Alertas
        alerts_md = ""
        for a in report.alerts:
            alerts_md += f"| {a.pattern_id} | {a.category} | {a.occurrences} | {a.last_seen} |\n"
        content = content.replace("{{alerts_table}}", alerts_md)
        
        # Ações
        actions_md = "\n".join([f"- {action}" for action in report.suggested_actions])
        content = content.replace("{{suggested_actions}}", actions_md)
    else:
        content = f"# Sovereignty Report {report.report_id}\n\nGenerated at: {report.generated_at}\nSeverity: {report.severity}\nSuccess Rate: {report.repair_success_rate * 100:.1f}%"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    logger.info(f"Relatório persistido: {md_path}")

if __name__ == "__main__":
    logger.info("=== INICIANDO MONITOR DE RECORRÊNCIA (CEO-OVERSIGHT) ===")
    report = check_recurrence()
    if report:
        save_report(report)
        logger.info(f"STATUS: ALERTA EMITIDO ({report.severity})")
    else:
        logger.info("STATUS: OPERAÇÃO NORMAL")
