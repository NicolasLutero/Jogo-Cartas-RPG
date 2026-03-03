# CartaService.py
from random import random

# Domain Class
from src.domain.entity.CartaEntity import CartaEntity
from src.domain.entity.UsuarioEntity import UsuarioEntity

# Infra Class
from src.infra.dao.CartaDAO import CartaDAO


class CartaService:
    _instance = None

    personagem = [[1, "Mago"], [1, "Arqueiro"], [1, "Guerreiro"],
                  [1, "Barbaro"], [1, "Barbaro Gelo"], [1, "Druida"],
                  [1, "Guerreiro Githyanki"], [1, "Ladino Lua"], [1, "Monge Eclipse"],
                  [1, "Piromancer"]]
    fundo = [[1, "Planície"], [1, "Montanha"], [1, "Floresta"],
             [1, "Floresta Noturna"], [1, "Vulcao"]]
    borda = [[1, "Perfeito"], [2, "Top"], [3, "Ótimo"], [4, "Bom"], [5, "Comum"]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.carta_dao = CartaDAO()
        return cls._instance


    # -----------------------------
    # CREATE
    # -----------------------------
    def gerar_n_cartas(self, n, usuario):
        cartas = [self.carta_aleatoria(usuario.get_id(), usuario.get_fator_n()) for _ in range(n)]
        for carta in cartas:
            self.carta_dao.criar(carta)
        return cartas

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
            case "Barbaro":
                stats = [15, 12, 14, 8, 10, 13]
            case "Barbaro Gelo":
                stats = [14, 10, 15, 12, 13, 8]
            case "Druida":
                stats = [10, 12, 13, 8, 15, 14]
            case "Guerreiro Githyanki":
                stats = [14, 15, 13, 10, 8, 12]
            case "Ladino Lua":
                stats = [10, 15, 12, 13, 14, 8]
            case "Monge Eclipse":
                stats = [12, 14, 13, 10, 15, 8]
            case "Piromancer":
                stats = [8, 12, 10, 15, 13, 14]
        return stats


    # -------------------------------------------
    # BUSCAR CARTA POR ID
    # -------------------------------------------
    def buscar_carta(self, id_carta):
        return self.carta_dao.buscar_por_id(id_carta)


    # -----------------------------
    # REFORJA
    # -----------------------------
    def reforjar(self, usuario: UsuarioEntity, card1: CartaEntity) -> CartaEntity:
        fator_n = usuario.get_fator_n()
        dono_id = usuario.get_id()

        card2 = self.carta_aleatoria(dono_id, fator_n)
        while card2.get_nome() != card1.get_nome():
            card2 = self.carta_aleatoria(dono_id, fator_n)

        for atr in ["for", "des", "con", "int", "sab", "car"]:
            card1.set_atributo(atr, [card1.get_stats()[atr][0],
                                     max(card1.get_stats()[atr][1], card2.get_stats()[atr][1])])

        self.carta_dao.atualizar(card1)
        return card1


    # -----------------------------
    # FUNDIR
    # -----------------------------
    def fundir(self, card1: CartaEntity, card2: CartaEntity) -> CartaEntity:
        for atr in ["for", "des", "con", "int", "sab", "car"]:
            card1.set_atributo(atr, [card1.get_stats()[atr][0],
                                     max(card1.get_stats()[atr][1], card2.get_stats()[atr][1])])

        if card1.get_bonus() < card2.get_bonus():
            bonus = card1.get_bonus()+1
            card1.set_bonus(bonus)
            card1.set_borda(self.borda[len(self.borda)-bonus][1])

        self.carta_dao.atualizar(card1)
        self.carta_dao.deletar(card2.get_id())
        return card1


    # -----------------------------
    # CARTA APRESENTAVEL AO CLIENT
    # -----------------------------
    @staticmethod
    def para_client(card: CartaEntity):
        dict_carta = card.to_dict()
        for c, v in dict_carta["stats"].items():
            dict_carta["stats"][c] = [f"{(sum(v) + dict_carta["bonus"]):.2f}", f"{int(100 * (v[1] + 3) / 5):02d}"]
        return dict_carta
