
import flet as ft
import sqlite3
import random
import urllib.request
import json
from datetime import datetime
def init_db():
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, val TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, cat TEXT, sender TEXT, content TEXT, stamp TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS diplomacy (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, rel TEXT, author TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, chan TEXT, sender TEXT, msg TEXT, stamp TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS market (id INTEGER PRIMARY KEY AUTOINCREMENT, cat TEXT, title TEXT, price TEXT, broker TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS cw_ops (id INTEGER PRIMARY KEY AUTOINCREMENT, tm TEXT, rules TEXT, positions TEXT)")
conn.commit()
conn.close()
def main(page: ft.Page):
page.title = "DPSP LEGACY COMMAND"
page.theme_mode = ft.ThemeMode.DARK
page.bgcolor = "#070a13"
page.padding = 10
init_db()
active_user = ft.Refft.Dropdown
webhook_input = ft.Refft.TextField
chat_input = ft.Refft.TextField
news_input = ft.Refft.TextField
intel_name = ft.Refft.TextField
market_title = ft.Refft.TextField
market_price = ft.Refft.TextField
cw_time = ft.Refft.TextField
cw_rules = ft.Refft.TextField
cw_pos = ft.Refft.TextField
soldier_lbl = ft.Refft.Text
asset_lbl = ft.Refft.Text
threat_lbl = ft.Refft.Text
threat_progress = ft.Refft.ProgressBar
def get_webhook():
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT val FROM config WHERE key='webhook'")
row = c.fetchone()
conn.close()
return row[0] if row else ""
def save_webhook(url):
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("INSERT OR REPLACE INTO config (key, val) VALUES ('webhook', ?)", (url,))
conn.commit()
conn.close()
def dispatch_discord_embed(title, description, hex_color=5814783):
hook_url = get_webhook().strip()
if not hook_url:
return
payload = {
"embeds": [{
"title": f"[DPSP NETWORK] {title}",
"description": description,
"color": hex_color,
"footer": {"text": "Architect Framework: Pruthviraj / pruthviraj_gowda"}
}]
}
try:
req = urllib.request.Request(
hook_url,
data=json.dumps(payload).encode('utf-8'),
headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)
urllib.request.urlopen(req)
except Exception as err:
print("Webhook transmission bypass:", err)
def update_dominance_matrix():
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT COUNT(DISTINCT sender) FROM chat")
soldiers = c.fetchone()[0] or 0
c.execute("SELECT COUNT() FROM market")
assets = c.fetchone()[0] or 0
c.execute("SELECT COUNT() FROM diplomacy WHERE rel='🤝 ALLIANCE-FAMILY'")
allies = c.fetchone()[0] or 0
c.execute("SELECT COUNT(*) FROM cw_ops")
wars = c.fetchone()[0] or 0
conn.close()
score = (soldiers * 8) + (assets * 4) + (allies * 12) + (wars * 15)
score = min(max(int(score), 5), 100)
soldier_lbl.current.value = str(soldiers + 4)
asset_lbl.current.value = str(assets)
threat_progress.current.value = score / 100
if score < 35:
threat_lbl.current.value = f"STATUS: SECURE SECTOR RECON ({score}%)"
threat_lbl.current.value_color = "#94a3b8"
elif score < 75:
threat_lbl.current.value = f"STATUS: SECTOR GRIND DOMINANCE ({score}%)"
threat_lbl.current.value_color = "#3b82f6"
else:
threat_lbl.current.value = f"STATUS: CRITICAL FACTION OVERLORD ({score}%)"
threat_lbl.current.value_color = "#ef4444"
page.update()
def render_news(container):
container.controls.clear()
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT cat, sender, content, stamp FROM news ORDER BY id DESC LIMIT 15")
for row in c.fetchall():
cat, sender, body, stamp = row
badge_color = {"📢 ANNOUNCEMENT": "#fbbf24", "📰 DPSP-NEWSPAPER": "#3b82f6", "🎉 SERVER-NEWS": "#10b981", "🔥 MAIN-EVENT": "#ef4444"}.get(cat, "#a855f7")
container.controls.append(
ft.Container(
content=ft.Column([
ft.Row([
ft.Container(content=ft.Text(cat, size=10, color="#ffffff", weight=ft.FontWeight.BOLD), bgcolor=badge_color, padding=4, border_radius=4),
ft.Text(f"By {sender} • {stamp}", size=11, color="#94a3b8")
], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
ft.Text(body, size=14, color="#e2e8f0"),
], spacing=6),
padding=12, bgcolor="#0f1322", border_radius=8, border=ft.border.all(1, "#24324d"), margin=ft.margin.only(bottom=8)
)
)
conn.close()
update_dominance_matrix()
def render_chat(container, channel):
container.controls.clear()
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT sender, msg, stamp FROM chat WHERE chan=? ORDER BY id DESC LIMIT 25", (channel,))
for row in c.fetchall():
sender, msg, stamp = row
is_bot = sender == "🤖 OwO Bot"
container.controls.append(
ft.Container(
content=ft.Column([
ft.Text(f"{sender} [{stamp}]", size=11, color="#f472b6" if is_bot else "#5865f2", weight=ft.FontWeight.BOLD),
ft.Text(msg, size=14, color="#ffffff"),
], spacing=2),
padding=8, border_radius=8, bgcolor="#181330" if is_bot else "#0b0f19", margin=ft.margin.only(bottom=6)
)
)
conn.close()
page.update()
def render_intel(container):
container.controls.clear()
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT name, rel, author FROM diplomacy ORDER BY id DESC")
for row in c.fetchall():
name, rel, author = row
is_allied = rel == "🤝 ALLIANCE-FAMILY"
container.controls.append(
ft.ListTile(
leading=ft.Icon(ft.icons.SHIELD if is_allied else ft.icons.GPP_BAD, color="#10b981" if is_allied else "#ef4444"),
title=ft.Text(name, weight=ft.FontWeight.BOLD, color="#ffffff"),
subtitle=ft.Text(f"Standing: {rel} | Logged by: {author}", color="#94a3b8", size=12),
bgcolor="#0f1322", shape=ft.RoundedRectangleBorder(radius=8)
)
)
conn.close()
update_dominance_matrix()
def render_market(container):
container.controls.clear()
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT cat, title, price, broker FROM market ORDER BY id DESC")
for row in c.fetchall():
cat, title, price, broker = row
container.controls.append(
ft.ListTile(
leading=ft.Icon(ft.icons.STOREFRONT, color="#fbbf24"),
title=ft.Text(title, weight=ft.FontWeight.BOLD, color="#ffffff"),
subtitle=ft.Text(f"Section: {cat} | Merchant: {broker}", color="#94a3b8"),
trailing=ft.Text(price, color="#fbbf24", weight=ft.FontWeight.BOLD, size=14),
bgcolor="#0f1322", shape=ft.RoundedRectangleBorder(radius=8)
)
)
conn.close()
update_dominance_matrix()
def render_cw(container):
container.controls.clear()
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("SELECT tm, rules, positions FROM cw_ops ORDER BY id DESC LIMIT 5")
for row in c.fetchall():
tm, rules, pos = row
container.controls.append(
ft.Container(
content=ft.Column([
ft.Text(f"⏰ COORDINATED ACTION TIME: {tm}", size=13, color="#ef4444", weight=ft.FontWeight.BOLD),
ft.Text(f"📜 LOADOUT COMPLIANCE RULES:\n{rules}", size=12, color="#fbbf24"),
ft.Text(f"🗺️ BOUNDARY DROP POSITION GRID:\n{pos}", size=12, color="#ffffff"),
], spacing=6),
padding=12, bgcolor="#0f1322", border_radius=8, border=ft.border.all(1, "#ef4444"), margin=ft.margin.only(bottom=10)
)
)
conn.close()
update_dominance_matrix()
def push_announcement(e, cat_select, container):
txt = news_input.current.value.strip()
if not txt: return
user = active_user.current.value
stamp = datetime.now().strftime("%I:%M %p")
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("INSERT INTO news (cat, sender, content, stamp) VALUES (?, ?, ?, ?)", (cat_select.value, user, txt, stamp))
conn.commit()
conn.close()
dispatch_discord_embed(f"NEW BROADCAST: {cat_select.value}", f"Operator: {user}\nTransmission: {txt}", 16759844)
news_input.current.value = ""
render_news(container)
def push_chat(e, chan_select, container):
msg = chat_input.current.value.strip()
if not msg: return
user = active_user.current.value
stamp = datetime.now().strftime("%I:%M %p")
chan = chan_select.value
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("INSERT INTO chat (chan, sender, msg, stamp) VALUES (?, ?, ?, ?)", (chan, user, msg, stamp))
low = msg.lower()
if low == "owo":
c.execute("INSERT INTO chat (chan, sender, msg, stamp) VALUES (?, ?, ?, ?)",
(chan, "🤖 OwO Bot", f"Hello {user}! (uwu)", stamp))
elif low in ["owo hunt", "owo h"]:
loots = ["Legendary Phoenix 🦅", "Shadow Stalker Wolf 🐺", "Common Fox 🦊"]
c.execute("INSERT INTO chat (chan, sender, msg, stamp) VALUES (?, ?, ?, ?)",
(chan, "🤖 OwO Bot", f"🔍 {user} captured a {random.choice(loots)}!", stamp))
elif low in ["owo cash", "owo bal"]:
c.execute("INSERT INTO chat (chan, sender, msg, stamp) VALUES (?, ?, ?, ?)",
(chan, "🤖 OwO Bot", f"💰 {user}, balance is {random.randint(4000, 50000):,} Cowoncy!", stamp))
conn.commit()
conn.close()
chat_input.current.value = ""
render_chat(container, chan)
def push_intel(e, rel_select, container):
nm = intel_name.current.value.strip()
if not nm: return
user = active_user.current.value
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("INSERT INTO diplomacy (name, rel, author) VALUES (?, ?, ?)", (nm, rel_select.value, user))
conn.commit()
conn.close()
dispatch_discord_embed("DIPLOMATIC UPDATE", f"Faction: {nm}\nStanding Alignment: {rel_select.value}\nLogged by: {user}", 1095811)
intel_name.current.value = ""
render_intel(container)
def push_market(e, cat_select, container):
tl = market_title.current.value.strip()
pr = market_price.current.value.strip()
if not tl or not pr: return
user = active_user.current.value
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("INSERT INTO market (cat, title, price, broker) VALUES (?, ?, ?, ?)", (cat_select.value, tl, pr, user))
conn.commit()
conn.close()
dispatch_discord_embed("NEW MARKETPLACE LISTING", f"Asset: {tl}\nCategory: {cat_select.value}\nValuation Price: {pr}\nContact Broker: {user}", 16500483)
market_title.current.value = ""
market_price.current.value = ""
render_market(container)
def push_cw(e, container):
t = cw_time.current.value.strip()
r = cw_rules.current.value.strip()
p = cw_pos.current.value.strip()
if not t: return
conn = sqlite3.connect("dpsp_premium_matrix.db")
c = conn.cursor()
c.execute("INSERT INTO cw_ops (tm, rules, positions) VALUES (?, ?, ?)", (t, r, p))
conn.commit()
conn.close()
page.run_javascript("window.speechSynthesis.speak(new SpeechSynthesisUtterance('Tactical Capital War orders deployed. Check communications node immediately.'));")
dispatch_discord_embed("⚠️ TACTICAL CW DISPATCH BROADCASTED ⚠️", f"Target Coordination Time: {t}\nRules Details: {r}\nBoundary Positions: {p}", 15672356)
cw_time.current.value = ""
cw_rules.current.value = ""
cw_pos.current.value = ""
render_cw(container)
news_lv = ft.ListView(expand=True, spacing=4)
news_cat = ft.Dropdown(value="📢 ANNOUNCEMENT", options=[
ft.dropdown.Option("📢 ANNOUNCEMENT"), ft.dropdown.Option("📰 DPSP-NEWSPAPER"), ft.dropdown.Option("🎉 SERVER-NEWS"), ft.dropdown.Option("🔥 MAIN-EVENT")
], bgcolor="#0f1322")
news_view = ft.Column([
ft.Text("📢 Family Stream Categories", size=15, weight=ft.FontWeight.BOLD),
news_cat, ft.TextField(ref=news_input, hint_text="Type broadcast context...", bgcolor="#0f1322"),
ft.ElevatedButton("Publish Announcement", color="#ffffff", bgcolor="#5865f2", on_click=lambda e: push_announcement(e, news_cat, news_lv)),
ft.Divider(color="#24324d"), ft.Container(content=news_lv, expand=True)
], expand=True, visible=True)
chat_lv = ft.ListView(expand=True, spacing=4)
chat_chan = ft.Dropdown(value="# GENERAL-CHAT", options=[
ft.dropdown.Option("# GENERAL-CHAT"), ft.dropdown.Option("# UNIVERSAL-CHAT"), ft.dropdown.Option("# MEDIA"), ft.dropdown.Option("# owo")
], bgcolor="#0f1322", on_change=lambda e: render_chat(chat_lv, e.control.value))
chat_view = ft.Column([
ft.Text("💬 Discord Stream Simulation Channels", size=15, weight=ft.FontWeight.BOLD),
chat_chan, ft.Container(content=chat_lv, expand=True, bgcolor="#03050a", padding=6, border_radius=8),
ft.Row([
ft.TextField(ref=chat_input, hint_text="Send message or type owo tools...", expand=True, bgcolor="#0f1322"),
ft.IconButton(icon=ft.icons.SEND, icon_color="#5865f2", on_click=lambda e: push_chat(e, chat_chan, chat_lv))
])
], expand=True, visible=False)
intel_lv = ft.ListView(expand=True, spacing=6)
intel_rel = ft.Dropdown(value="🤝 ALLIANCE-FAMILY", options=[
ft.dropdown.Option("🤝 ALLIANCE-FAMILY"), ft.dropdown.Option("🏴 ENEMY-FAMILY-NAME"), ft.dropdown.Option("👽 OCG-ALLIANCE-NAME")
], bgcolor="#0f1322")
intel_view = ft.Column([
ft.Text("🛡️ Faction Diplomatic Standings Ledger", size=15, weight=ft.FontWeight.BOLD),
ft.TextField(ref=intel_name, hint_text="Target Clan Designation", bgcolor="#0f1322"), intel_rel,
ft.ElevatedButton("Log Diplomacy Entry", color="#ffffff", bgcolor="#10b981", on_click=lambda e: push_intel(e, intel_rel, intel_lv)),
ft.Divider(color="#24324d"), ft.Container(content=intel_lv, expand=True)
], expand=True, visible=False)
market_lv = ft.ListView(expand=True, spacing=6)
market_cat = ft.Dropdown(value="🚗 VEHICLE-DEALING", options=[
ft.dropdown.Option("🏢 PROPERTY-DEALING"), ft.dropdown.Option("🚗 VEHICLE-DEALING"), ft.dropdown.Option("🎒 ACCESSORIES-DEALING"), ft.dropdown.Option("👕 SKIN-DEALING")
], bgcolor="#0f1322")
market_view = ft.Column([
ft.Text("💰 DPSP Active Commercial Trading Floor", size=15, weight=ft.FontWeight.BOLD),
market_cat, ft.TextField(ref=market_title, hint_text="Asset Name / Skin Label", bgcolor="#0f1322"),
ft.TextField(ref=market_price, hint_text="Trade Pricing demands", bgcolor="#0f1322"),
ft.ElevatedButton("Publish Asset Contract", color="#ffffff", bgcolor="#fbbf24", on_click=lambda e: push_market(e, market_cat, market_lv)),
ft.Divider(color="#24324d"), ft.Container(content=market_lv, expand=True)
], expand=True, visible=False)
cw_lv = ft.ListView(expand=True, spacing=6)
cw_view = ft.Column([
ft.Text("⚔️ Capital War Dispatch Terminal", size=15, weight=ft.FontWeight.BOLD),
ft.TextField(ref=cw_time, hint_text="Target Drop Time...", bgcolor="#0f1322"),
ft.TextField(ref=cw_rules, hint_text="Weapon loadout details", bgcolor="#0f1322"),
ft.TextField(ref=cw_pos, hint_text="Vehicle coordinates parameters", bgcolor="#0f1322"),
ft.ElevatedButton("Broadcast CW War Orders", color="#ffffff", bgcolor="#ef4444", on_click=lambda e: push_cw(cw_lv)),
ft.Divider(color="#24324d"),
ft.Text("⚙️ LIVE DISCORD SYNC WEBHOOK OVERLAY (OPTIONAL)", size=12, color="#94a3b8", weight=ft.FontWeight.BOLD),
ft.Row([
ft.TextField(ref=webhook_input, value=get_webhook(), hint_text="Paste Discord Webhook URL...", expand=True, password=True, bgcolor="#0f1322"),
ft.IconButton(icon=ft.icons.SAVE, icon_color="#10b981", on_click=lambda e: [save_webhook(webhook_input.current.value), ft.SnackBar(ft.Text("Matrix Synced!"))])
]),
ft.Divider(color="#24324d"), ft.Container(content=cw_lv, expand=True)
], expand=True, visible=False)
def nav_toggle(e):
idx = e.control.selected_index
news_view.visible = (idx == 0)
chat_view.visible = (idx == 1)
intel_view.visible = (idx == 2)
market_view.visible = (idx == 3)
cw_view.visible = (idx == 4)
if idx == 0: render_news(news_lv)
if idx == 1: render_chat(chat_lv, chat_chan.value)
if idx == 2: render_intel(intel_lv)
if idx == 3: render_market(market_lv)
if idx == 4: render_cw(cw_lv)
page.update()
page.navigation_bar = ft.NavigationBar(
destinations=[
ft.NavigationDestination(icon=ft.icons.CHAT, label="NEWS"),
ft.NavigationDestination(icon=ft.icons.FORUM, label="CHAT"),
ft.NavigationDestination(icon=ft.icons.SHIELD_ROUNDS, label="INTEL"),
ft.NavigationDestination(icon=ft.icons.STOREFRONT, label="MARKET"),
ft.NavigationDestination(icon=ft.icons.CROSSSWORDS, label="WAR ROOM")
],
selected_index=0, on_change=nav_toggle, bgcolor="#0f1322"
)
metrics_panel = ft.Container(
content=ft.Column([
ft.Text("DPSP LEGACY MASTER APP", size=18, weight=ft.FontWeight.BOLD, color="#ffffff"),
ft.Text("System Architect: Pruthviraj / pruthviraj_gowda", size=10, color="#fbbf24"),
ft.Dropdown(
ref=active_user, value="Founder / Boss",
options=[ft.dropdown.Option("Founder / Boss"), ft.dropdown.Option("Co-Founder"), ft.dropdown.Option("Chief Administrator"), ft.dropdown.Option("senior curator of Capital War"), ft.dropdown.Option("Supreme Lead")],
bgcolor="#070a13"
),
ft.Divider(color="#24324d"),
ft.Row([
ft.Column([ft.Text("0", ref=soldier_lbl, size=16, weight=ft.FontWeight.BOLD, color="#06b6d4"), ft.Text("SOLDIERS", size=8, color="#94a3b8")], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
ft.Column([ft.Text("0", ref=asset_lbl, size=16, weight=ft.FontWeight.BOLD, color="#fbbf24"), ft.Text("ASSETS", size=8, color="#94a3b8")], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
ft.Column([ft.Text("STATUS: CALCULATING...", ref=threat_lbl, size=10, weight=ft.FontWeight.BOLD), ft.ProgressBar(ref=threat_progress, value=0.1, width=120, color="#5865f2", bgcolor="#24324d")], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
padding=12, border=ft.border.all(1, "#24324d"), border_radius=16, bgcolor="#0f1322"
)
page.add(metrics_panel, ft.Divider(color="#24324d"), news_view, chat_view, intel_view, market_view, cw_view)
render_news(news_lv)
ft.app(target=main)
