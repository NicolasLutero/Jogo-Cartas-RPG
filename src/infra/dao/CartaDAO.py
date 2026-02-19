# CartaDAO.py
import os

# Domain Class
from src.domain.entity.CartaEntity import CartaEntity

# Infra Class
from src.infra.database.FactoryConnection import FactoryConnection


class CartaDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = FactoryConnection.get_connection()
            cls._instance._init_tables()
        return cls._instance


    # -------------------------------------------
    # CRIA TABELA SE NÃO EXISTIR
    # -------------------------------------------
    def _init_tables(self):
        try:
            sql_check = """
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'carta'
            """

            with self._conn.cursor() as cur:
                cur.execute(sql_check)
                existe = cur.fetchone()

            if not existe:
                self._executar_sql_criacao()

        except Exception:
            self._executar_sql_criacao()

    def _executar_sql_criacao(self):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../infra/database/sql"))
        sql_path = os.path.join(root_path, "TableCarta.sql")

        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()

        with self._conn.cursor() as cur:
            cur.execute(sql)

        self._conn.commit()


    # -------------------------------------------
    # CRIA CARTA
    # -------------------------------------------
    def criar(self, carta: CartaEntity) -> int:
        sql = """
            INSERT INTO carta (
                fundo,
                personagem,
                borda,
                atr_for,
                atr_des,
                atr_con,
                atr_int,
                atr_sab,
                atr_car,
                var_for,
                var_des,
                var_con,
                var_int,
                var_sab,
                var_car,
                bonus,
                dono
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s
            )
            RETURNING id;
        """

        with self._conn.cursor() as cur:
            status = []
            variacoes = []
            atributos = carta.get_stats()
            for c in ["for", "des", "con", "int", "sab", "car"]:
                status.append(atributos[c][0])
                variacoes.append(atributos[c][1])

            cur.execute(sql, (
                carta.get_fundo(),
                carta.get_personagem(),
                carta.get_borda(),
                status[0],
                status[1],
                status[2],
                status[3],
                status[4],
                status[5],
                variacoes[0],
                variacoes[1],
                variacoes[2],
                variacoes[3],
                variacoes[4],
                variacoes[5],
                carta.get_bonus(),
                carta.get_dono()
            ))
            carta_id = cur.fetchone()[0]

        self._conn.commit()
        carta.set_id(carta_id)
        return carta_id


    # -------------------------------------------
    # LÊ CARTA PELO ID
    # -------------------------------------------
    def buscar_por_id(self, cod: int) -> CartaEntity | None:
        sql = """
            SELECT 
                id,
                fundo,
                personagem,
                borda,
                atr_for,
                atr_des,
                atr_con,
                atr_int,
                atr_sab,
                atr_car,
                var_for,
                var_des,
                var_con,
                var_int,
                var_sab,
                var_car,
                bonus,
                dono
            FROM carta
            WHERE id = %s
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (cod,))
            row = cur.fetchone()

        if not row:
            return None

        stats = {
            "for": [int(row[4]), float(row[10])],
            "des": [int(row[5]), float(row[11])],
            "con": [int(row[6]), float(row[12])],
            "int": [int(row[7]), float(row[13])],
            "sab": [int(row[8]), float(row[14])],
            "car": [int(row[9]), float(row[15])],
        }

        return CartaEntity(
            cod=row[0],
            fundo=row[1],
            personagem=row[2],
            borda=row[3],
            stats=stats,
            bonus=int(row[16]),
            dono=row[17]
        )


    # -------------------------------------------
    # LÊ TODAS AS CARTAS POR USUÁRIO
    # -------------------------------------------
    def listar_por_usuario(self, id_usuario: str) -> list[CartaEntity]:
        sql = """
            SELECT 
                id,
                fundo,
                personagem,
                borda,
                atr_for,
                atr_des,
                atr_con,
                atr_int,
                atr_sab,
                atr_car,
                var_for,
                var_des,
                var_con,
                var_int,
                var_sab,
                var_car,
                bonus,
                dono
            FROM carta
            WHERE dono = %s
        """

        cartas = []
        with self._conn.cursor() as cur:
            cur.execute(sql, (id_usuario,))
            rows = cur.fetchall()

        for row in rows:
            stats = {
                "for": [int(row[4]), float(row[10])],
                "des": [int(row[5]), float(row[11])],
                "con": [int(row[6]), float(row[12])],
                "int": [int(row[7]), float(row[13])],
                "sab": [int(row[8]), float(row[14])],
                "car": [int(row[9]), float(row[15])],
            }

            cartas.append(CartaEntity(
                cod=row[0],
                fundo=row[1],
                personagem=row[2],
                borda=row[3],
                stats=stats,
                bonus=int(row[16]),
                dono=row[17]
            ))

        return cartas


    # -------------------------------------------
    # LÊ TODAS AS CARTAS POR USUÁRIO APLICANDO UM FILTRO
    # -------------------------------------------
    def buscar_por_usuario_filtrado(self, id_usuario: str, filtro: dict) -> list[CartaEntity]:
        sql = """
            SELECT 
                id,
                fundo,
                personagem,
                borda,
                atr_for,
                atr_des,
                atr_con,
                atr_int,
                atr_sab,
                atr_car,
                var_for,
                var_des,
                var_con,
                var_int,
                var_sab,
                var_car,
                bonus,
                dono
            FROM carta
            WHERE 
                dono = %s AND
                fundo = ANY(%s) AND
                personagem = ANY(%s) AND
                borda = ANY(%s)
                ORDER BY 
            CASE borda
                WHEN 'Perfeito' THEN 1
                WHEN 'Top'      THEN 2
                WHEN 'Ótimo'    THEN 3
                WHEN 'Bom'      THEN 4
                WHEN 'Comum'    THEN 5
                ELSE 6
            END,
            personagem ASC,
            fundo ASC
        """

        cartas = []
        with self._conn.cursor() as cur:
            cur.execute(sql, (
                id_usuario,
                filtro["fundos"],
                filtro["personagens"],
                filtro["bordas"]
            ))
            rows = cur.fetchall()

        for row in rows:
            stats = {
                "for": [int(row[4]), float(row[10])],
                "des": [int(row[5]), float(row[11])],
                "con": [int(row[6]), float(row[12])],
                "int": [int(row[7]), float(row[13])],
                "sab": [int(row[8]), float(row[14])],
                "car": [int(row[9]), float(row[15])],
            }

            cartas.append(CartaEntity(
                cod=row[0],
                fundo=row[1],
                personagem=row[2],
                borda=row[3],
                stats=stats,
                bonus=int(row[16]),
                dono=row[17]
            ))

        return cartas


    # -------------------------------------------
    # LISTA OS TIPOS DE FUNDO, PERSONAGEM E BORDA DE UM USUÁRIO
    # -------------------------------------------
    def listar_tipos(self, id_dono, campo) -> list[str]:
        sql = """
            SELECT DISTINCT %s
            FROM carta
            WHERE dono = %s
            ORDER BY %s;
        """
        with self._conn.cursor() as cur:
            cur.execute(sql, (campo, id_dono, campo))
            rows = cur.fetchall()
        return [row[0] for row in rows]


    # -------------------------------------------
    # DELETA CARTA
    # -------------------------------------------
    def deletar(self, id_carta: int) -> bool:
        sql = """
            DELETE FROM carta
            WHERE id = %s
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (id_carta,))
            deletado = cur.rowcount > 0

        self._conn.commit()
        return deletado


    # -------------------------------------------
    # ATUALIZA CARTA
    # -------------------------------------------
    def atualizar(self, carta: CartaEntity) -> bool:
        sql = """
            UPDATE carta
            SET 
                fundo = %s,
                personagem = %s,
                borda = %s,
                atr_for = %s,
                atr_des = %s,
                atr_con = %s,
                atr_int = %s,
                atr_sab = %s,
                atr_car = %s,
                var_for = %s,
                var_des = %s,
                var_con = %s,
                var_int = %s,
                var_sab = %s,
                var_car = %s,
                bonus = %s
            WHERE id = %s
        """

        with self._conn.cursor() as cur:
            status = []
            variacoes = []
            atributos = carta.get_stats()
            for c in ["for", "des", "con", "int", "sab", "car"]:
                status.append(atributos[c][0])
                variacoes.append(atributos[c][1])

            cur.execute(sql, (
                carta.get_fundo(),
                carta.get_personagem(),
                carta.get_borda(),
                status[0],
                status[1],
                status[2],
                status[3],
                status[4],
                status[5],
                variacoes[0],
                variacoes[1],
                variacoes[2],
                variacoes[3],
                variacoes[4],
                variacoes[5],
                carta.get_bonus(),
                carta.get_id()
            ))
            atualizado = cur.rowcount > 0

        self._conn.commit()
        return atualizado
