# Revisión del lote 1 (situaciones 1–10), coreano

**Veredicto: GO**

Cambios: 27 (en 10 partes). Validador: `unir_partes.py ko 1` → 10 situaciones, 0 errores.

## Por tipo

- **Traducción errónea (2):** s1-o1 y s2-o1 traían el coreano en el campo `es`; ahora «¿Hay mesa para dos?» y «Un café pequeño, por favor.».
- **Léxico no natural o calco (9):**
  - 일 플러스 일 → 원 플러스 원 (s3-i-v4, con metaRom «won peulleoseu won»);
  - 시차 피로 → 시차증 (s8-i-v9);
  - s5-o1 «중간 사이즈» → 엠 사이즈 (con fraseRom);
  - «호의의 표시로» → 서비스 차원에서 (s10-a-f3);
  - 보증 서비스로 처리돼요 → 보증이 적용돼요 (s4-i-f2);
  - 환승 비행기 → 환승 항공편 (s7-i1);
  - «이 모델 중에» → 이 모델로 (s6-i1);
  - «날짜가 지났어요» → 유통기한이 지났어요 (s3-i-f4);
  - s6-a1 «뜯어졌어요» de calzado → 밑창이 떨어졌어요.
- **Adaptación a Corea (3):** 국경 (s9-b-v4) → 입국장 con sus traducciones y romanización; s9-i-v9 ya no usa «국경»; s2-a-v10 «거스름돈은 괜찮아요» (propina inusual) → 거스름돈이 모자란 것 같아요.
- **Registro (2):** s9-a1 y s10-a3 mezclaban 합쇼체 y 해요체 en la misma intervención; unificados en 해요체.
- **Ejemplos (6):** sin 그/그녀 (s5-a-v1, s9-i-v10, s9-a-v1); ejemplo inverosímil «작은 밀가루» (s3-b-v10); redundancia «다 떨어지고 없어요» (s3-i-v9); anuncio de aterrizaje mal usado (s8-a-v5); 닳다 con «헌» redundante (s6-i-v10); 방문하다 con ejemploRom actualizado (s9-b-v9).
- **Traducciones es/en (5):** «260 (milímetros)» → «260 mm» (s6-o1); 소비기한 → «la fecha límite de consumo / consume-by date» (s3-i-v2); «¿Cree que llegue a tiempo?» → «¿Cree que alcance a llegar?» (s7-i1); en de 부담스럽다 (s6-a-v9); en de 시차증.

## Observaciones

- No se encontraron discrepancias de romanización con `rr_ko.py`; no hay casos léxicos que discutir.
- Progresión básico → intermedio → avanzado correcta en las 10 situaciones; sin menciones de Ecuador.
- Pendiente menor (no bloquea): el vocabulario cita verbos solo en -다, tal como pide ENCARGO.md (la ficha pedía también la forma -요 entre paréntesis; prevalece el encargo).
