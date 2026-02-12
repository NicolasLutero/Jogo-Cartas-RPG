from PIL import Image
from math import sqrt
from pathlib import Path


class ImagemCartaGenerator:
    _instance = None
    ROOT = Path(__file__).resolve().parents[3]  # ajuste níveis se necessário


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def img_path(self, rel_path: str):
        return self.ROOT / rel_path

    @staticmethod
    def scale_image(img, scale: float):
        w, h = img.size
        new_w = int(w * scale)
        new_h = int(h * scale)
        return img.resize((new_w, new_h), Image.LANCZOS)

    @staticmethod
    def paste_center(base, overlay, offset_x=0, offset_y=0):
        bw, bh = base.size
        ow, oh = overlay.size
        x = (bw - ow) // 2 + offset_x
        y = (bh - oh) // 2 + offset_y
        base.paste(overlay, (x, y), overlay)
        return base

    @staticmethod
    def crop_center(img, target_w, target_h):
        w, h = img.size
        left = (w - target_w) // 2
        top = (h - target_h) // 2
        right = left + target_w
        bottom = top + target_h
        return img.crop((left, top, right, bottom))

    @staticmethod
    def aplicar_borda_transparente(img, radius_px):
        """Recorte com cantos arredondados (border-radius style)"""
        if radius_px <= 0:
            return img

        img = img.convert("RGBA")
        w, h = img.size
        pixels = img.load()

        r = radius_px

        # Função distância
        def dist(x1, y1, x2, y2):
            return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # --- Canto superior esquerdo ---
        cx, cy = r, r
        for x in range(r):
            for y in range(r):
                if dist(x, y, cx, cy) > r:
                    pixels[x, y] = (0, 0, 0, 0)

        # --- Canto superior direito ---
        cx, cy = w - r - 1, r
        for x in range(w - r, w):
            for y in range(r):
                if dist(x, y, cx, cy) > r:
                    pixels[x, y] = (0, 0, 0, 0)

        # --- Canto inferior esquerdo ---
        cx, cy = r, h - r - 1
        for x in range(r):
            for y in range(h - r, h):
                if dist(x, y, cx, cy) > r:
                    pixels[x, y] = (0, 0, 0, 0)

        # --- Canto inferior direito ---
        cx, cy = w - r - 1, h - r - 1
        for x in range(w - r, w):
            for y in range(h - r, h):
                if dist(x, y, cx, cy) > r:
                    pixels[x, y] = (0, 0, 0, 0)

        return img

    def gerar_carta(
        self,
        fundo: str,
        personagem: str,
        borda: str
    ):
        escala_fundo = 1.0
        escala_personagem = 1.15
        escala_borda = 2.4
        offset_y_personagem = 80
        offset_y_borda = -36
        borda_transparente_px = 65
        tamanho_final = (505, 620)

        # --- Carregamento ---
        fundo_img = Image.open(self.img_path(f"img/fundo/{fundo.lower()}.jpg")).convert("RGBA")
        personagem_img = Image.open(self.img_path(f"img/personagem/{personagem}.png")).convert("RGBA")
        borda_img = Image.open(self.img_path(f"img/borda/{borda}.png")).convert("RGBA")

        # --- Escalas ---
        fundo_img = self.scale_image(fundo_img, escala_fundo)
        personagem_img = self.scale_image(personagem_img, escala_personagem)
        borda_img = self.scale_image(borda_img, escala_borda)

        # --- Base ---
        base = fundo_img.copy()

        # --- Sobreposição ---
        base = self.paste_center(base, personagem_img, offset_y=offset_y_personagem)
        base = self.paste_center(base, borda_img, offset_y=offset_y_borda)

        # --- Crop central ---
        final = self.crop_center(base, tamanho_final[0], tamanho_final[1])

        # --- Borda transparente (CSS-like border) ---
        final = self.aplicar_borda_transparente(final, borda_transparente_px)

        return final
