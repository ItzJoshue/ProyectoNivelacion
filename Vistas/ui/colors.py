"""Paleta suave y moderna — inspirada en diseño UI contemporáneo (tipo Figma AI)."""


class Colors:
    # ── Superficies ─────────────────────────────────────────────────────
    WHITE = "#FFFFFF"
    BG_APP = "#F7F8FC"
    BG_SUBTLE = "#EEF1F7"
    BG_MUTED = "#E4E8F0"

    # ── Bordes ──────────────────────────────────────────────────────────
    BORDER = "#DDE3EE"
    BORDER_SOFT = "#E8ECF4"
    BORDER_FOCUS = "#9BAAD4"

    # ── Texto ───────────────────────────────────────────────────────────
    TEXT_PRIMARY = "#2A3142"
    TEXT_SECONDARY = "#667085"
    TEXT_MUTED = "#949BB0"

    # ── Marca / primario (periwinkle suave) ─────────────────────────────
    PRIMARY = "#7289DA"
    PRIMARY_HOVER = "#6278C9"
    PRIMARY_LIGHT = "#EEF2FB"
    PRIMARY_SOFT = "#DDE5F8"

    # ── Acento cálido (sustituye rojo intenso) ──────────────────────────
    ACCENT = "#D4928A"
    ACCENT_HOVER = "#C47E76"
    ACCENT_LIGHT = "#FAF0EE"

    # ── Semánticos ──────────────────────────────────────────────────────
    SUCCESS = "#6FA889"
    SUCCESS_HOVER = "#5E9678"
    SUCCESS_LIGHT = "#EDF6F1"

    DANGER = "#D98888"
    DANGER_HOVER = "#C97575"
    DANGER_LIGHT = "#FBF0F0"

    # ── Alias legacy (compatibilidad con el resto del código) ───────────
    RED = ACCENT
    RED_HOVER = ACCENT_HOVER
    RED_LIGHT = ACCENT_LIGHT
    GREEN = PRIMARY
    GREEN_HOVER = PRIMARY_HOVER
    GREEN_LIGHT = PRIMARY_LIGHT
    GRAY_50 = BG_APP
    GRAY_100 = BG_SUBTLE
    GRAY_300 = BORDER
    GRAY_600 = TEXT_SECONDARY
    GRAY_800 = TEXT_PRIMARY
