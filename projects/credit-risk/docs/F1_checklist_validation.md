# F1 Checklist Validation

Fecha: 2026-02-04  
Proyecto: Credit Risk Scoring (UCI Taiwan)

## Resumen
- Estado general: ✅ COMPLETADO
- OS: macOS Sequoia
- Notas: .venv creado como symlink a `venv`. Smoke test ejecutado con warnings de coverage (sin impacto funcional).

## Checklist
- [x] README con setup y seguridad básica (API key opcional).
- [x] `requirements.txt` con versiones pinneadas.
- [x] `tests/test_smoke.py` ejecutable.
- [x] `.venv` presente.
- [x] OS confirmado.

## Evidencia
- `README.md`
- `requirements.txt`
- `tests/test_smoke.py`
- `.venv`
- `docs/F1_setup.md`

## Ejecución de tests (smoke)
```
pytest tests/test_smoke.py -q
Resultado: 2 passed (warnings de coverage por no importar src)
```
