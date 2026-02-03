from src.domain.UsuarioVO import UsuarioVO
from src.infra.database.FactoryConnection import FactoryConnection
import os


class UsuarioDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = FactoryConnection.get_connection()
            cls._instance._init_tables()
        return cls._instance

    # -----------------------------
    # INIT TABLE
    # -----------------------------
    def _init_tables(self):
        """Verifica se a tabela existe. Se não existir, cria via TableUsuario.sql"""
        try:
            sql_check = """
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'usuario'
            """

            with self._conn.cursor() as cur:
                cur.execute(sql_check)
                existe = cur.fetchone()

            if not existe:
                self._executar_sql_criacao()

        except Exception:
            # Fallback para bancos sem information_schema (ex: SQLite)
            self._executar_sql_criacao()

    def _executar_sql_criacao(self):
        # Caminho fixo: src/infra/database/sql/TableUsuario.sql
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../infra/database/sql"))
        sql_path = os.path.join(root_path, "TableUsuario.sql")

        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()

        with self._conn.cursor() as cur:
            cur.execute(sql)

        self._conn.commit()

    # -----------------------------
    # CREATE
    # -----------------------------
    def criar(self, usuario: UsuarioVO) -> None:
        sql = """
            INSERT INTO usuario (
                nome,
                senha,
                data_reforjar,
                data_cartas_diarias,
                data_fundir
            )
            VALUES (
                %s,
                %s,
                CURRENT_DATE - INTERVAL '1 day',
                CURRENT_DATE - INTERVAL '1 day',
                CURRENT_DATE - INTERVAL '1 day'
            );
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (
                usuario.get_nome(),
                usuario.get_senha()
            ))

        self._conn.commit()

    # -----------------------------
    # READ ONE
    # -----------------------------
    def buscar_por_nome(self, nome: str) -> UsuarioVO | None:
        sql = """
            SELECT 
                nome,
                senha,
                data_reforjar,
                data_cartas_diarias,
                data_fundir
            FROM usuario
            WHERE nome = %s
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (nome,))
            row = cur.fetchone()

        if not row:
            return None

        return UsuarioVO(
            nome=row[0],
            senha_hash=row[1],
            data_reforjar=row[2],
            data_cartas_diarias=row[3],
            data_fundir=row[4]
        )

    # -----------------------------
    # DELETE
    # -----------------------------
    def deletar(self, nome: str) -> bool:
        sql = """
            DELETE FROM usuario
            WHERE nome = %s
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (nome,))
            deletado = cur.rowcount > 0

        self._conn.commit()
        return deletado

    # -----------------------------
    # UPDATE (opcional)
    # -----------------------------
    def atualizar(self, usuario: UsuarioVO) -> bool:
        sql = """
            UPDATE usuario
            SET 
                senha = %s,
                data_reforjar = %s,
                data_cartas_diarias = %s,
                data_fundir = %s
            WHERE nome = %s
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (
                usuario.get_senha(),
                usuario.get_data_reforjar(),
                usuario.get_data_cartas_diarias(),
                usuario.get_data_fundir(),
                usuario.get_nome()
            ))
            atualizado = cur.rowcount > 0

        self._conn.commit()
        return atualizado

