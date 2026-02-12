from random import random

from src.domain.service.ImagemCartaGenerator import ImagemCartaGenerator
from src.domain.entity.CartaEntity import CartaEntity


class CartaService:
    _instance = None

    personagem = ["Mago", "Arqueiro", "Guerreiro"]
    fundo = ["Planície", "Montanha", "Floresta"]

    raridades = ["Perfeito", "Top", "Ótimo", "Bom", "Comum"]
    borda = []
    for i, rari in enumerate(raridades):
        for _ in range(i + 1):
            borda.append(rari)

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

        bonus = len(CartaService.raridades) - CartaService.raridades.index(borda) - 1 - 2

        base = self.estatus_base(personagem)
        stats = {
            "for": round(base[0] + bonus + random() * 5, 2),
            "des": round(base[1] + bonus + random() * 5, 2),
            "con": round(base[2] + bonus + random() * 5, 2),
            "int": round(base[3] + bonus + random() * 5, 2),
            "sab": round(base[4] + bonus + random() * 5, 2),
            "car": round(base[5] + bonus + random() * 5, 2)
        }

        return CartaEntity(None, fundo, personagem, borda, stats, dono)

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
            case "Guerreiro":
                stats = [15, 13, 14, 8, 12, 10]
            case "Arqueiro":
                stats = [8, 15, 14, 12, 13, 10]
        return stats

    # -----------------------------
    # REFORJA
    # -----------------------------
    def reforjar(self, v1, card1: CartaEntity) -> CartaEntity:
        card2 = self.carta_aleatoria(v1)

        while card2.get_nome() != card1.get_nome():
            card2 = self.carta_aleatoria(v1)

        stats = {
            "For": max(card1.get_atributo("For"), card2.get_atributo("For")),
            "Des": max(card1.get_atributo("Des"), card2.get_atributo("Des")),
            "Con": max(card1.get_atributo("Con"), card2.get_atributo("Con")),
            "Int": max(card1.get_atributo("Int"), card2.get_atributo("Int")),
            "Sab": max(card1.get_atributo("Sab"), card2.get_atributo("Sab")),
            "Car": max(card1.get_atributo("Car"), card2.get_atributo("Car"))
        }

        card2.set_stats(stats)
        return card2

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
                    stats1[n_atr] + 2 - CartaService.raridades.index(card1.get_borda())
            )
            atr_c2 = card2.get_atributo(atr) - (
                    stats2[n_atr] + 2 - CartaService.raridades.index(card2.get_borda())
            )
            stats3[atr] = max(atr_c1, atr_c2) + stats1[n_atr] - 1

        raridade = card1.get_borda()
        if CartaService.raridades.index(card2.get_borda()) < CartaService.raridades.index(card1.get_borda()):
            index = CartaService.raridades.index(card1.get_borda()) - 1
            raridade = CartaService.raridades[index]
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
    # IMAGEM DA CARTA
    # -----------------------------
    @staticmethod
    def get_image(card: CartaEntity):
        return ImagemCartaGenerator().gerar_carta(
            card.get_fundo(),
            card.get_personagem(),
            card.get_borda()
        )
