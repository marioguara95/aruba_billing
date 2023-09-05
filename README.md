# Domanda 1
**Al candidato viene richiesto di definire l’architettura software, la struttura db di massima e i principali flussi
di lavoro di un sistema che integra il servizio di Fatturazione Elettronica di Aruba con sistemi esterni senza
usare l’interfaccia web. La soluzione deve essere in grado di gestire sia la fatturazione attiva sia quella
passiva.**

## Architettura Software:

L'architettura del sistema deve essere basata su un'architettura a microservizi, che permette di separare le diverse
funzionalità in moduli indipendenti. 

Ogni microservizio può essere sviluppato, testato e scalato autonomamente. Questo deve essere così composto:

### Servizio di Integrazione: 
Questo microservizio funge da punto di ingresso per la comunicazione con il servizio di Fatturazione Elettronica di Aruba. Gestisce le richieste in arrivo e distribuisce i compiti ai servizi appropriati.

### Servizio di Fatturazione: 
Questo microservizio gestisce la logica di creazione e gestione delle fatture, sia attive che passive. 
Si interfaccia con il servizio di Fatturazione Elettronica utilizzando delle API.

### Servizio di Database: 
Questo microservizio gestisce la persistenza dei dati. Utilizza Django con il database MySQL per archiviare le 
informazioni relative alle fatture, ai clienti, ai prodotti, ecc.

### Servizi Esterni: 
In base ai sistemi esterni con cui devi integrarti, potresti avere servizi dedicati che gestiscono la comunicazione con 
questi sistemi. Ad esempio, un servizio per l'integrazione con il sistema contabile, un altro per la gestione delle scorte, ecc.

## Struttura del Database:
Utilizzando Django e MySQL, puoi definire i modelli del database in Django e lasciare che il framework si occupi della 
creazione delle tabelle. Ecco alcuni esempi di modelli:

### Modello Cliente: 
Con campi come nome, indirizzo, codice fiscale, partita IVA, ecc.

### Modello Prodotto: 
Con campi come nome, descrizione, prezzo, quantità in magazzino, ecc.

### Modello Fattura: 
Con campi come numero di fattura, data di emissione, importo totale, cliente associato, ecc.

## Principali Flussi di Lavoro:

### Creazione Fattura Attiva:

Il servizio di Fatturazione riceve una richiesta per creare una nuova fattura attiva.
Recupera le informazioni del cliente e dei prodotti dal servizio di database.
Genera la fattura, calcolando l'importo totale e altri dettagli.
Comunica con il servizio di Fatturazione Elettronica di Aruba per inviare la fattura.

### Creazione Fattura Passiva:

Il servizio di Fatturazione riceve una notifica di ricezione di una nuova fattura passiva.
Estrae le informazioni dalla notifica e le registra nel servizio di database.

### Integrazione con Sistemi Esterni:

Il servizio di Integrazione riceve richieste o notifiche da sistemi esterni.
In base alla natura della richiesta, inoltra il lavoro al servizio appropriato (contabilità, gestione scorte, ecc.).


# Domanda 2 
Si richiede inoltre di implementare un modulo per gestire l’API Rest che acceda al db e permetta di
gestire le seguenti operazioni: 

1. invio fattura, 

2. richiedere stato fattura, _(NB: non è stato impostato uno stato quindi ritorna l'importo totale della fattura, 
lo stato è simulato)_
   - Teoria:  http://localhost:8000/api/invoices/{id_fattura}/invoice_status/
   - Esempio: http://localhost:8000/api/invoices/1/invoice_status/

4. recupero fattura, 
   - Teoria:  http://localhost:8000/api/invoices/{id_fattura}/
   - Esempio: http://localhost:8000/api/invoices/1/

5. elenco fatture attive/passive ricevute in un certo intervallo.
   - Teoria:  http://localhost:8000/api/invoices/invoices_in_interval/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
   - Esempio: http://localhost:8000/api/invoices/invoices_in_interval/?start_date=2023-01-25&end_date=2023-08-26

##


## Test inserimento fattura 1. Cliente esistente



````
{
  "products": [
      {
          "name": "Acqua",
          "description": "bottiglia 33cl",
          "price": "1.50",
          "quantity_in_stock": "11",
          "quantity": "3" 
      }

  ],
  "client": {
      "name": "mario",
      "address": "via bari 123",
      "fiscal_code": "grgmra95h26a662x",
      "vat_number": "00000000000"
  },
  "invoice_number": "123",
  "issuance_date": "2023-08-24"
}
````
## Test inserimento fattura 2. Cliente NON esistente
````
{
  "products": [
    {
      "name": "Prodotto 1",
      "description": "Descrizione Prodotto 1",
      "price": "2.50",
      "quantity_in_stock": 10,
      "quantity": 2
    }
  ],
  "client": {
    "name": "Giovanni",
    "address": "via Roma 456",
    "fiscal_code": "giov345h76a123x",
    "vat_number": "12345678901"
  },
  "invoice_number": "456",
  "issuance_date": "2023-08-25"
}
````
## Test inserimento fattura 3. Cliente NON esistente

````
{
  "products": [
    {
      "name": "Caffè",
      "description": "Pacco da 250g",
      "price": "4.50",
      "quantity_in_stock": 20,
      "quantity": 1
    },
    {
      "name": "Penne",
      "description": "Confezione da 500g",
      "price": "1.20",
      "quantity_in_stock": 15,
      "quantity": 2
    }
  ],
  "client": {
    "name": "Laura",
    "address": "via Milano 789",
    "fiscal_code": "laur567g89b456y",
    "vat_number": "98765432101"
  },
  "invoice_number": "789",
  "issuance_date": "2023-08-26"
}
````