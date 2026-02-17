from random import random

from src.domain.entity.CartaEntity import CartaEntity
from src.infra.dao.CartaDAO import CartaDAO


class CartaService:
    _instance = None

    personagem = [[1, "Mago"], [1, "Arqueiro"], [1, "Guerreiro"]]
    fundo = [[1, "Planície"], [1, "Montanha"], [1, "Floresta"]]
    borda = [[1, "Perfeito"], [2, "Top"], [3, "Ótimo"], [4, "Bom"], [5, "Comum"]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # -----------------------------
    # CREATE
    # -----------------------------
    def carta_aleatoria(self, dono, fator_n) -> CartaEntity:
        n = (random() + fator_n) % 1
        return self.gerar_carta(dono, n)

    def gerar_carta(self, dono, n) -> CartaEntity:
        n, personagem = self.selecione(n, CartaService.personagem)
        n, fundo = self.selecione(n, CartaService.fundo)
        n, borda = self.selecione(n, CartaService.borda)

        if borda == "Perfeito": bonus = 5
        elif borda == "Top": bonus = 4
        elif borda == "Ótimo": bonus = 3
        elif borda == "Bom": bonus = 2
        else: bonus = 1  # borda == "Comum"

        base = self.estatus_base(personagem)
        stats = {
            "for": [base[0], round(random()*5, 2)-3],
            "des": [base[1], round(random()*5, 2)-3],
            "con": [base[2], round(random()*5, 2)-3],
            "int": [base[3], round(random()*5, 2)-3],
            "sab": [base[4], round(random()*5, 2)-3],
            "car": [base[5], round(random()*5, 2)-3]
        }

        return CartaEntity(None, fundo, personagem, borda, stats, bonus, dono)

    @staticmethod
    def selecione(n, lista):
        n *= sum([c for c, _ in lista])
        escolha = lista[-1]
        for item in lista:
            if item[0] < n:
                n -= item[0]
            else:
                escolha = item[1]
                n /= item[0]
                break
        return n % 1, escolha

    @staticmethod
    def estatus_base(personagem):
        stats = [0, 0, 0, 0, 0, 0]
        match personagem:
            case "Mago":
                stats = [8, 13, 14, 15, 12, 10]
            case "Guerreiro":
                stats = [15, 13, 14, 8, 12, 10]
            case "Arqueiro":
                stats = [8, 15, 14, 12, 13, 10]
        return stats

    # -----------------------------
    # REFORJA
    # -----------------------------
    def reforjar(self, v1, card1: CartaEntity) -> CartaEntity:
        card2 = self.carta_aleatoria(card1.get_dono(), v1)
        while card2.get_nome() != card1.get_nome():
            card2 = self.carta_aleatoria(card1.get_dono(), v1)

        for atr in ["for", "des", "con", "int", "sab", "car"]:
            card1.set_atributo(atr, [card1.get_stats()[atr][0],
                                     max(card1.get_stats()[atr][1], card2.get_stats()[atr][1])])

        CartaDAO().atualizar(card1)
        return card1

    # -----------------------------
    # FUNDIR
    # -----------------------------
    def fundir(self, card1: CartaEntity, card2: CartaEntity) -> CartaEntity:
        stats1 = self.estatus_base(card1.get_personagem())
        stats2 = self.estatus_base(card2.get_personagem())

        stats3 = {}
        atributos = ["For", "Des", "Con", "Int", "Sab", "Car"]

        for n_atr, atr in enumerate(atributos):
            atr_c1 = card1.get_atributo(atr) - (
                    stats1[n_atr] + 2 - CartaService.borda.index(card1.get_borda())
            )
            atr_c2 = card2.get_atributo(atr) - (
                    stats2[n_atr] + 2 - CartaService.borda.index(card2.get_borda())
            )
            stats3[atr] = max(atr_c1, atr_c2) + stats1[n_atr] - 1

        raridade = card1.get_borda()
        if CartaService.borda.index(card2.get_borda()) < CartaService.borda.index(card1.get_borda()):
            index = CartaService.borda.index(card1.get_borda()) - 1
            raridade = CartaService.borda[index]
            for c1 in stats3:
                stats3[c1] = stats3[c1] + 1

        nome = f"{card1.get_personagem()} da {card1.get_fundo()} {raridade}"

        return CartaEntity(
            nome,
            card1.get_personagem(),
            card1.get_fundo(),
            raridade,
            stats3
        )

    # -----------------------------
    # CARTA APRESENTAVEL AO CLIENT
    # -----------------------------
    @staticmethod
    def para_client(card: CartaEntity):
        dict_carta = card.to_dict()
        for c, v in dict_carta["stats"].items():
            dict_carta["stats"][c] = [f"{(sum(v) + dict_carta["bonus"]):.2f}", f"{int(100 * (v[1] + 3) / 5):02d}"]
        return dict_carta
