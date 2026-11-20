#!/usr/bin/env python3
"""Build the agent tools reference from the backend's tool catalog.

The catalog (`backend/app/agent_access/catalog.py` in the main repo) is the one
source of the MCP `tools/list`; this page must not drift from it. The script reads
the file as text (no backend import, no dependencies) and writes one snippet per
language to `snippets/agent-tools-<lang>.mdx`, which the reference pages import.

    python3 scripts/gen_agent_tools.py /path/to/tronrental/backend/app/agent_access/catalog.py

A new catalog group or money effect fails the run until its translations are added below.
"""

import ast
import re
import sys
from pathlib import Path

LANGS = ("en", "ru", "es", "pt", "tr", "zh", "hi")

# Scope constants of `app.core.permissions` → the scope string.
SCOPES = {
    "PUBLIC": None,
    "VIEW": "view",
    "DEPOSIT_VIEW": "deposit_view",
    "BUY_ENERGY": "buy_energy",
    "BUY_BANDWIDTH": "buy_bandwidth",
    "SMART_MODE": "smart_mode",
    "TRANSFER_PACKAGES": "transfer_packages",
    "ENERGY_RESALE": "energy_resale",
    "BROADCASTER": "broadcaster",
    "STAKING": "staking",
    "NODE_API_PLAN": "node_api_plan",
    "WITHDRAW": "withdraw",
}

# Effect constants of the catalog → money effect.
EFFECTS = {
    "READ": "none",
    "READ_CHAIN": "none",
    "WRITE": "none",
    "OUTBOUND": "none",
    "STOP": "none",
    "INCOME": "income",
    "DEBIT": "debit",
    "RECURRING_DEBIT": "recurring",
    "WITHDRAWAL": "withdraw",
}

T = {
    "head": {
        "en": ("Tool", "Permissions", "Money", "What it does"),
        "ru": ("Инструмент", "Права", "Деньги", "Что делает"),
        "es": ("Herramienta", "Permisos", "Dinero", "Qué hace"),
        "pt": ("Ferramenta", "Permissões", "Dinheiro", "O que faz"),
        "tr": ("Araç", "İzinler", "Para", "Ne yapar"),
        "zh": ("工具", "权限", "资金", "作用"),
        "hi": ("टूल", "अनुमतियाँ", "पैसा", "क्या करता है"),
    },
    "public": {"en": "none", "ru": "не нужны", "es": "ninguno", "pt": "nenhuma", "tr": "gerekmez", "zh": "无", "hi": "कोई नहीं"},
    "key_only": {
        "en": "API key only",
        "ru": "только API-ключ",
        "es": "solo clave API",
        "pt": "só chave de API",
        "tr": "yalnızca API anahtarı",
        "zh": "仅 API 密钥",
        "hi": "केवल API कुंजी",
    },
    "none": {"en": "—", "ru": "—", "es": "—", "pt": "—", "tr": "—", "zh": "—", "hi": "—"},
    "income": {"en": "to balance", "ru": "на баланс", "es": "al saldo", "pt": "para o saldo", "tr": "bakiyeye", "zh": "回到余额", "hi": "बैलेंस में"},
    "debit": {"en": "spends", "ru": "списывает", "es": "gasta", "pt": "gasta", "tr": "harcar", "zh": "扣款", "hi": "खर्च करता है"},
    "recurring": {
        "en": "recurring",
        "ru": "регулярно",
        "es": "recurrente",
        "pt": "recorrente",
        "tr": "düzenli",
        "zh": "周期性",
        "hi": "आवर्ती",
    },
    "withdraw": {
        "en": "withdrawal",
        "ru": "вывод",
        "es": "retiro",
        "pt": "saque",
        "tr": "çekim",
        "zh": "提现",
        "hi": "निकासी",
    },
}

GROUPS = {
    "Prices and estimates": {"ru": "Цены и расчёт", "es": "Precios y estimaciones", "pt": "Preços e estimativas", "tr": "Fiyatlar ve tahminler", "zh": "价格与估算", "hi": "कीमतें और अनुमान"},
    "Quotes": {"ru": "Котировки", "es": "Cotizaciones", "pt": "Cotações", "tr": "Teklifler", "zh": "报价", "hi": "कोटेशन"},
    "Balance and history": {"ru": "Баланс и история", "es": "Saldo e historial", "pt": "Saldo e histórico", "tr": "Bakiye ve geçmiş", "zh": "余额与历史", "hi": "बैलेंस और इतिहास"},
    "Address": {"ru": "Адрес", "es": "Dirección", "pt": "Endereço", "tr": "Adres", "zh": "地址", "hi": "पता"},
    "Deposits": {"ru": "Пополнение", "es": "Depósitos", "pt": "Depósitos", "tr": "Yatırımlar", "zh": "充值", "hi": "जमा"},
    "Energy": {"ru": "Энергия", "es": "Energía", "pt": "Energia", "tr": "Enerji", "zh": "能量", "hi": "एनर्जी"},
    "Bandwidth": {"ru": "Bandwidth", "es": "Bandwidth", "pt": "Bandwidth", "tr": "Bandwidth", "zh": "带宽", "hi": "बैंडविड्थ"},
    "Auto bandwidth": {"ru": "Авто-bandwidth", "es": "Auto Bandwidth", "pt": "Auto Bandwidth", "tr": "Otomatik Bandwidth", "zh": "自动带宽", "hi": "ऑटो बैंडविड्थ"},
    "Auto-refill": {"ru": "Автопополнение", "es": "Recarga automática", "pt": "Recarga automática", "tr": "Otomatik yenileme", "zh": "自动补充", "hi": "ऑटो रीफ़िल"},
    "Orders": {"ru": "Заказы", "es": "Pedidos", "pt": "Pedidos", "tr": "Siparişler", "zh": "订单", "hi": "ऑर्डर"},
    "Smart Mode": {"ru": "Smart Mode", "es": "Smart Mode", "pt": "Smart Mode", "tr": "Smart Mode", "zh": "Smart Mode", "hi": "Smart Mode"},
    "Transfer packages": {"ru": "Пакеты переводов", "es": "Paquetes de transferencias", "pt": "Pacotes de transferências", "tr": "Transfer paketleri", "zh": "转账套餐", "hi": "ट्रांसफ़र पैकेज"},
    "Invoices": {"ru": "Инвойсы", "es": "Facturas", "pt": "Faturas", "tr": "Faturalar", "zh": "发票", "hi": "इनवॉइस"},
    "Broadcaster": {"ru": "Бродкастер", "es": "Broadcaster", "pt": "Broadcaster", "tr": "Broadcaster", "zh": "广播器", "hi": "ब्रॉडकास्टर"},
    "Energy Resale": {"ru": "Energy Resale", "es": "Energy Resale", "pt": "Energy Resale", "tr": "Energy Resale", "zh": "Energy Resale", "hi": "Energy Resale"},
    "Withdrawal": {"ru": "Вывод", "es": "Retiros", "pt": "Saques", "tr": "Çekimler", "zh": "提现", "hi": "निकासी"},
    "Staking": {"ru": "Стейкинг", "es": "Staking", "pt": "Staking", "tr": "Staking", "zh": "质押", "hi": "स्टेकिंग"},
    "Node API": {"ru": "Node API", "es": "Node API", "pt": "Node API", "tr": "Node API", "zh": "Node API", "hi": "Node API"},
}

HEADER = "{/* Generated by scripts/gen_agent_tools.py from the backend tool catalog. Do not edit by hand. */}\n"


def group_name(comment: str) -> str | None:
    """A group header is a short comment that does not end a sentence; notes end with '.'."""
    text = comment.strip()
    if text.endswith(".") or text.startswith("fmt:") or text.startswith("One row"):
        return None
    return re.split(r"[:(]", text, maxsplit=1)[0].strip()


def parse(source: str) -> list[tuple[str, list[dict]]]:
    groups: list[tuple[str, list[dict]]] = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            name = group_name(stripped[2:])
            if name:
                groups.append((name, []))
            continue
        if not stripped.startswith("Tool("):
            continue
        call = ast.parse(stripped.rstrip(","), mode="eval").body
        name, method, path, scope, effect, title = (
            a.value if isinstance(a, ast.Constant) else a.id for a in call.args
        )
        key_only = any(k.arg == "key_only" and k.value.value for k in call.keywords)
        if not groups:
            sys.exit(f"tool {name} comes before any group comment")
        if scope not in SCOPES or effect not in EFFECTS:
            sys.exit(f"tool {name}: unknown scope {scope} or effect {effect} — add it to the script")
        groups[-1][1].append(
            {
                "name": name,
                "method": method,
                "path": path,
                "scope": SCOPES[scope],
                "money": EFFECTS[effect],
                "title": title,
                "key_only": key_only,
            }
        )
    return [(g, rows) for g, rows in groups if rows]


def render(groups: list[tuple[str, list[dict]]], lang: str) -> str:
    head = T["head"][lang]
    out = [HEADER]
    for group, rows in groups:
        if group not in GROUPS:
            sys.exit(f"group '{group}' has no translations — add it to GROUPS")
        out.append(f"\n#### {group if lang == 'en' else GROUPS[group][lang]}\n")
        out.append(f"| {head[0]} | {head[1]} | {head[2]} | {head[3]} |")
        out.append("|---|---|---|---|")
        for r in rows:
            scopes = [f"`{r['scope']}`"] if r["scope"] else [T["public"][lang]]
            if r["money"] == "recurring":
                scopes.append("`recurring`")
            if r["key_only"]:
                scopes.append(T["key_only"][lang])
            out.append(
                f"| `{r['name']}` | {' + '.join(scopes)} | {T[r['money']][lang]} | "
                f"{r['title']} (`{r['method']} {r['path']}`) |"
            )
    return "\n".join(out) + "\n"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    groups = parse(Path(sys.argv[1]).read_text())
    total = sum(len(rows) for _, rows in groups)
    out_dir = Path(__file__).resolve().parent.parent / "snippets"
    out_dir.mkdir(exist_ok=True)
    for lang in LANGS:
        (out_dir / f"agent-tools-{lang}.mdx").write_text(render(groups, lang))
    print(f"{total} tools in {len(groups)} groups → snippets/agent-tools-*.mdx")


if __name__ == "__main__":
    main()
