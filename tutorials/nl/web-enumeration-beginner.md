# Beginnerstutorial web-enumeration

## Scope en leerdoel

- Toegestaan labtarget: `http://127.0.0.1:3000`
- Doel: een onbekende webapplicatie systematisch en eerst passief verkennen.
- Buiten scope: andere lokale services, het LAN en publieke hosts.

## Onderwerpen

- [ ] Verschil tussen passieve inspectie en actieve enumeration
- [ ] Eerste HTTP-response en headers interpreteren
- [ ] Browserweergave, bron en netwerkrequests inspecteren
- [ ] Technologie-indicaties voorzichtig formuleren
- [ ] Bevindingen, onzekerheden en vervolgstappen vastleggen

## Lesverloop

### Stap 1 — Eerste HTTP-response

Vraag met `curl` alleen de responseheaders van de hoofdpagina op:

```bash
curl -I http://127.0.0.1:3000/
```

Belangrijke optie:

- `-I` vraagt om alleen de HTTP-headers en niet om de volledige responsebody.

Let op de statusregel, `Content-Type`, server- of frameworkindicaties en eventuele securityheaders. Een ontbrekende header is een observatie, nog geen bewezen kwetsbaarheid.

## Behandelde onderwerpen
