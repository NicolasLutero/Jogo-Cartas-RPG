from random import random

from src.domain.GeradorImagemCarta import GeradorImagemCarta


class OperadorCarta:
    _instance = None
    personagem = ["Mago", "Arqueiro", "Guerreiro"]
    cenario = ["Planície", "Montanha", "Floresta"]

    raridades = ["Perfeito", "Top", "Ótimo", "Bom", "Comum"]
    raridade = []
    for i, rari in enumerate(raridades):
        for _ in range(i + 1):
            raridade.append(rari)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # -----------------------------
    # CREATE
    # -----------------------------
    def carta_aleatorio(self, v1):
        n = (random() + v1)%1
        return self.gerar_carta(n)

    def gerar_carta(self, n):
        n, personagem = self.selecione(n, OperadorCarta.personagem)
        n, cenario = self.selecione(n, OperadorCarta.cenario)
        n, raridade = self.selecione(n, OperadorCarta.raridade)

        bonus = len(OperadorCarta.raridades)-OperadorCarta.raridades.index(raridade)-1 - 2

        stats = self.estatus_base(personagem)
        stats = {
            "For": round(stats[0] + bonus + random()*5, 2),
            "Des": round(stats[1] + bonus + random()*5, 2),
            "Con": round(stats[2] + bonus + random()*5, 2),
            "Int": round(stats[3] + bonus + random()*5, 2),
            "Sab": round(stats[4] + bonus + random()*5, 2),
            "Car": round(stats[5] + bonus + random()*5, 2)
        }

        return {"nome":f"{personagem} da {cenario} {raridade}",
                "personagem": personagem,
                "cenario": cenario,
                "raridade": raridade,
                "stats":stats}

    @staticmethod
    def selecione(n, lista):
        n *= len(lista)
        escolha = lista[int(n)]
        return n % 1, escolha

    @staticmethod
    def estatus_base(personagem):
        stats = [0, 0, 0, 0, 0, 0]
        match personagem:
            case "Mago":
                stats = [8, 13, 14, 15, 12, 10]
            case "Arqueiro":
                stats = [8, 15, 14, 12, 13, 10]
            case "Guerreiro":
                stats = [15, 13, 14, 8, 12, 10]
        return stats

    # -----------------------------
    # REFORJA
    # -----------------------------
    def reforjar(self, v1, card1):
        card2 = self.carta_aleatorio(v1)
        while card2["nome"] != card1["nome"]:
            card2 = self.carta_aleatorio(v1)

        stats = {
            "For": max(card1["stats"]["For"], card2["stats"]["For"]),
            "Des": max(card1["stats"]["Des"], card2["stats"]["Des"]),
            "Con": max(card1["stats"]["Con"], card2["stats"]["Con"]),
            "Int": max(card1["stats"]["Int"], card2["stats"]["Int"]),
            "Sab": max(card1["stats"]["Sab"], card2["stats"]["Sab"]),
            "Car": max(card1["stats"]["Car"], card2["stats"]["Car"])
        }
        card2["stats"] = stats

        return card2

    # -----------------------------
    # FUNDIR
    # -----------------------------
    def fundir(self, card1, card2):
        stats1 = self.estatus_base(card1["personagem"])
        stats2 = self.estatus_base(card2["personagem"])

        stats3 = {}
        atributos = ["For", "Des", "Con", "Int", "Sab", "Car"]
        for n_atr, atr in enumerate(atributos):
            atr_c1 = card1["stats"][atr] - (stats1[n_atr]+2-OperadorCarta.raridades.index(card1["raridade"]))
            atr_c2 = card2["stats"][atr] - (stats2[n_atr]+2-OperadorCarta.raridades.index(card2["raridade"]))
            stats3[atr] = max(atr_c1, atr_c2) + stats1[n_atr]-1

        raridade = card1["raridade"]
        if OperadorCarta.raridades.index(card2["raridade"]) < OperadorCarta.raridades.index(card1["raridade"]):
            index = OperadorCarta.raridades.index(card1["raridade"]) - 1
            raridade = OperadorCarta.raridades[index]
            for c1, v1 in stats3.items():
                stats3[c1] = v1 + 1

        return {"nome": f"{card1["personagem"]} da {card1["cenario"]} {raridade}",
                "personagem": card1["personagem"],
                "cenario": card1["cenario"],
                "raridade": raridade,
                "stats": stats3}

    # -----------------------------
    # IMAGEM DA CARTA
    # -----------------------------
    @staticmethod
    def get_image(card):
        return GeradorImagemCarta().gerar_carta(card["cenario"], card["personagem"], card["raridade"])



# Remover #

def apresentar(card):
    print(card["nome"])
    print("estatística")
    for chave, valor in card["stats"].items():
        print(f" - {chave}: {valor}")
    OperadorCarta().get_image(card).show()
    print("\n")


carta = OperadorCarta().carta_aleatorio(0)
for i in range(10):
    print(i)
    carta = OperadorCarta().reforjar(0, carta)
apresentar(carta)

# Remover #
