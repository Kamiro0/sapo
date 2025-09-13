Proyecto Courier - LEON ROLDAN (Ficha 3147246) - Versión completa
---------------------------------------------------------------
- Dominio: Courier
- Entidad: Envío
- Prefijos: courier_*, test_courier_* (en nombres de archivos y tests)

Comandos:
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  pytest --cov=app --cov-report=term-missing
