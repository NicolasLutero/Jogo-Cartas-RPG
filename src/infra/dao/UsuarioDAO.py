import os

from src.domain.entity.UsuarioEntity import UsuarioEntity
from src.infra.database.FactoryConnection import FactoryConnection

from src.infra.exception.InfraException import *


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
    def criar(self, usuario: UsuarioEntity) -> int:
        sql = """
            INSERT INTO usuario (
                nome,
                senha,
                fator_n,
                data_reforjar,
                data_cartas_diarias,
                data_fundir
            )
            VALUES (
                %s,
                %s,
                %s,
                CURRENT_DATE - INTERVAL '1 day',
                CURRENT_DATE - INTERVAL '1 day',
                CURRENT_DATE - INTERVAL '1 day'
            )
            RETURNING id;
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (
                usuario.get_nome(),
                usuario.get_senha(),
                usuario.get_fator_n()
            ))
            usuario_id = cur.fetchone()[0]

        self._conn.commit()
        usuario.set_id(usuario_id)
        return usuario_id

    # -----------------------------
    # READ ONE
    # -----------------------------
    def buscar_por_nome(self, nome: str) -> UsuarioEntity | None:
        sql = """
            SELECT 
                id,
                nome,
                senha,
                fator_n,
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
            raise UsuarioNaoEncontradoException()

        return UsuarioEntity(
            cod=row[0],
            nome=row[1],
            senha_hash=row[2],
            fator_n=float(row[3]),
            data_reforjar=str(row[4]) if row[4] is not None else row[4],
            data_cartas_diarias=str(row[5]) if row[5] is not None else row[5],
            data_fundir=str(row[6]) if row[6] is not None else row[6]
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
    def atualizar(self, usuario: UsuarioEntity) -> bool:
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

