# Kali Cybersecurity Labs

Een interactieve Engels/Nederlandse leeromgeving voor legale cybersecuritytraining op Kali Linux. De installatie is Engelstalig en laat iedere gebruiker afzonderlijk de lestaal en eventuele spreektaal kiezen.

## Installatie

```bash
git clone https://github.com/MrHymanz/kali-cybersecurity-labs.git
cd kali-cybersecurity-labs
./scripts/setup.sh
```

De installatie vraagt eerst om Engels of Nederlands als lestaal. Daarna kies je Engelse spraak, Nederlandse spraak of geen spraak. De keuzes en gedownloade stemmodellen blijven lokaal.

## Grafische interface

Start na de installatie de lokale GUI:

```bash
./scripts/start-gui.sh
```

Open daarna `http://127.0.0.1:8080`. Het dashboard bevat lessen, voortgang, privénotities, optionele spraak en veilige labacties. De server luistert alleen op `127.0.0.1` en biedt geen veld voor willekeurige shellcommando's. Stop de server met `Ctrl+C` in de terminal waarin je hem hebt gestart.

Zie de uitgebreide [Engelse README](README.md) voor vereisten, privacycontroles, projectstructuur en licentie-informatie.
