from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.codice}: {self.tipo} {self.marca} ({self.anno_acquisto}), {self.valore:.2f} euro"

class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"{self.codice}: {self.id_strumento} {self.cognome_allievo}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.__responsabile = responsabile

        self.strumenti = {}
        self.prestiti = {}
        self.contatore_prestiti = 0

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self.__responsabile = responsabile



    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                righe = f.readlines()
            for riga in righe:
                riga = riga.strip()
                if riga == "":
                    continue
                codice, tipo, marca, anno, valore = riga.split(",")
                strumento = Strumento(codice, tipo, marca, int(anno), float(valore))
                self.strumenti[codice] = strumento

        except FileNotFoundError:
            print(f"Errore: il file '{file_path}' non esiste.")
            return None



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        massimo = 0
        for codice in self.strumenti:
            numero = int(codice[1:])
            if numero > massimo:
                massimo = numero

        nuovo_codice = "S" + str(massimo + 1)
        strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_codice] = strumento
        return strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti.values(), key=attrgetter("marca"))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"{id_strumento} non esiste.")

        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"{id_strumento} già in prestito.")

        self.contatore_prestiti += 1
        codice = "P" + str(self.contatore_prestiti);
        prestito = Prestito(codice, data, id_strumento, cognome_allievo)
        self.prestiti[codice] = prestito
        return prestito


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"{id_prestito} non esiste.")

        self.prestiti.pop(id_prestito)
