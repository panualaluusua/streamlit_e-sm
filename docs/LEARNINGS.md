# Learnings from the E-pyöräilyn SM-kisat Results Service Project

## 1. Google Sheets -integraation hyödyntäminen
- Opin, miten Google Sheets voidaan yhdistää Python-sovellukseen `gspread`-kirjaston ja palvelutilin avulla.
- Ymmärsin, kuinka Sheets toimii kevyenä tietovarastona, jota voidaan päivittää ja korjata manuaalisesti ilman monimutkaista backend-palvelua.
- Sheetsin reaaliaikainen päivittyminen mahdollisti lähes live-tulospalvelun toteutuksen.

## 2. Streamlitin käyttö modernin frontin rakentamiseen
- Sain kokemusta Streamlitin käytöstä nopean ja responsiivisen web-käyttöliittymän rakentamisessa.
- Opin hyödyntämään Streamlitin ominaisuuksia, kuten automaattista päivitysintervallia (`streamlit-autorefresh`) ja dynaamisia valintakomponentteja (kilpailu/sarja).
- CSS:n avulla pystyin parantamaan käyttöliittymän ulkoasua ja käytettävyyttä.

## 3. Käytettävyyden ja saavutettavuuden huomiointi
- Käyttöliittymän yksinkertaisuus ja selkeys olivat tärkeitä, jotta käyttäjät löysivät oikeat tulokset helposti.
- Valintatoimintojen (kilpailu, sarja) avulla käyttäjä pystyi suodattamaan tietoa tehokkaasti.

## 4. Joustavuus ja ylläpidettävyys
- Ratkaisu oli helposti muokattavissa tulevia tapahtumia varten: Sheetin ID:n ja rakenteen vaihtaminen riitti.
- Opin, että yksinkertainen arkkitehtuuri (ei erillistä backendia) voi olla tehokas ja helposti ylläpidettävä pienemmissä projekteissa.

## 5. Yleisön tavoittaminen ja vaikutus
- Yli 400 uniikkia kävijää osoitti, että kevytkin ratkaisu voi palvella laajaa käyttäjäkuntaa luotettavasti.

---

## Suurempi kuva – Mihin opit liittyvät?
Tämän projektin opit liittyvät laajemmin digitalisaation ja ohjelmistokehityksen trendeihin:
- Kevyillä, ketterillä ja helposti ylläpidettävillä ratkaisuilla voidaan tuottaa merkittävää hyötyä nopeasti, ilman raskasta IT-infrastruktuuria.
- Low-code/No-code-tyyliset työkalut (kuten Google Sheets ja Streamlit) mahdollistavat nopean kehityksen ja madaltavat digitalisaation kynnystä.
- Reaaliaikaisen tiedon jakaminen ja käyttäjälähtöinen suunnittelu ovat yhä tärkeämpiä monilla aloilla.
- Joustavuus ja helppo muokattavuus tukevat jatkuvaa kehitystä ja DevOps-ajattelua.

Nämä opit ovat sovellettavissa laajasti erilaisissa projekteissa ja organisaatioissa.

---

## Secrets-tiedoston turvallinen käyttö Streamlitissä
Ymmärsin, kuinka tärkeää on säilyttää salaiset avaimet ja tunnistetiedot turvallisesti projektissa. Streamlitin `.streamlit/secrets.toml`-tiedostoa käyttämällä:
- Voin tallentaa esimerkiksi Google Sheets -palvelutilin avaimet pois näkyvistä koodista.
- Secrets-tiedosto lisätään aina `.gitignore`-tiedostoon, jolloin se ei päädy versionhallintaan tai julkisiin repoihin.
- Sovellus voi hakea salaiset tiedot turvallisesti `st.secrets`-rajapinnan kautta ilman, että ne paljastuvat muille käyttäjille tai kehittäjille.

Tämä käytäntö suojaa arkaluontoisia tietoja ja on olennainen osa turvallista ohjelmistokehitystä.
