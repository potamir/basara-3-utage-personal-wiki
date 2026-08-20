import base64, os, io
from PIL import Image

wiki_dir = "/Users/rahamirez.ga/basara_icons/wiki_items"
game_dir = "/Users/rahamirez.ga/basara_icons"
out_html = "/Users/rahamirez.ga/basara3_utage_guide.html"

def img_to_base64(path):
    img = Image.open(path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('ascii')

# Load all 182 wiki icons
wiki_icons = {}
for f in os.listdir(wiki_dir):
    name = os.path.splitext(f)[0]  # e.g. "1-1", "28-3"
    fpath = os.path.join(wiki_dir, f)
    try:
        wiki_icons[name] = img_to_base64(fpath)
    except Exception as e:
        print(f"ERROR loading {f}: {e}")
print(f"Loaded {len(wiki_icons)} wiki icons")

# Load game weapon icons
wep_icons = {}
for i in range(30):
    p = os.path.join(game_dir, f"wep_{i:03d}.png")
    if os.path.exists(p):
        wep_icons[i] = img_to_base64(p)

def icon_html(icon_data):
    if icon_data:
        return f'<img src="data:image/png;base64,{icon_data}" alt="icon">'
    return '<div class="icon-placeholder">?</div>'

# Icon filenames per game row
row_icons = {
    r: [f"{r}-{c}" for c in range(1, 7 if r not in [23,24,25,26,27] else 5)]
    for r in range(1, 33)
}

# Item descriptions per game row
row_descs = {
    1: ["Life +2000 (S)","Life +3000 (M)","Life +4000 (L)","Attack +100 (S)","Attack +200 (M)","Attack +300 (L)"],
    2: ["Defence +200 (S)","Defence +250 (M)","Defence +400 (L)","Recovery potency +5%","Recovery potency +10%","Recovery potency +15%"],
    3: ["BASARA Art attack +200 (S)","+300 (M)","+400 (L)","Attack +300/400/500 during Drive","+400/500/600","+500/600/700"],
    4: ["Camp Commanders take more damage (S)","(M)","(L)","Elemental activation +5%","Elemental activation +7%","Elemental activation +9%"],
    5: ["Enemy guard break & dizzy up (S)","(M)","(L)","Stun/guard break/dizzy less often (S)","(M)","(L)"],
    6: ["Attack +70 per base captured","+80 per base","+90 per base","Atk & Def +50 during BASARA Assist","+60","+70"],
    7: ["Atk & Def +200 when near death","+300","+400","Aerial attack +400","+500","+600"],
    8: ["Attack +700 when all 3 gauges full","+800","+900","Attack +500 for first S-string hit","+600","+700"],
    9: ["Parry damage +2000","+2500","+3000","First 10s of stage: +4000 atk","First 20s","First 30s"],
    10: ["Heal while guarding (S)","(M)","(L)","Decreases enemy attack by 5%","Decreases by 10%","Decreases by 15%"],
    11: ["1-hit kills grant 3 zenny","4 zenny","5 zenny","Luck Up (S)","Luck Up (M)","Luck Up (L)"],
    12: ["Allies Fire-proof","Allies Shock-proof","Allies Ice-proof","Allies Wind-proof","Allies Dark-proof","Allies Light-proof"],
    13: ["3x damage to long-range soldiers","3x to shielded (1-hit shield break)","3x to large/heavy soldiers","3x to ninjas","3x to machines (1-hit trap break)","3x to animals"],
    14: ["Higher Critical Hit chance","Final hit of Normal Arts = critical","Deal +50% damage, take +300%","Weapon power = strongest weapon","Hero Time +1s per 5 KOs","Camp fills Hero Gauge 2x faster. Boost at 80 kills"],
    15: ["Hit count +2 when all 3 gauges full","Battle Frenzy +5 seconds","Combo time between hits extended","1 hit = 2 during BASARA Art","Hero Gauge full at battle start","Activate Drive once when gauge not full (red health)"],
    16: ["Movement speed greatly increased","Rice balls temporarily increase speed","Damage taken reduced by 1/4","Taunting fills BASARA Gauge faster","BASARA Gauge full at battle start","BASARA gauge fills faster"],
    17: ["Cannot be stunned by arrows/bullets","Auto-deflect arrows/bullets while blocking","Easier to parry attacks","Recover large health on duel win","Shortens dizzy recovery time","More invincibility frames while dodging"],
    18: ["1 hit = 2 while riding horse","Combo stays active on horse","Attack up on horse","Low HP but EXP multiplier +1","HP decreases but money rate x3","Attack increases per kill"],
    19: ["50% more EXP but HP hidden","Double EXP from stage awards","EXP multiplier +0.2 (+2 if both players)","Same weapon but higher LV (no Challenge mode)","Summons money mallet every 100 kills","Double HP of all enemies"],
    20: ["4x money, halved when hit","Temp boosts last 10s more","Increases blow back distance","No bodyguard assist","Nullifies weapon power-ups","Fugitives marked on map"],
    21: ["Allied soldiers flatter you","Allied soldiers talk crap","Old Japanese radio show in battle","\"The girl and the monkey\" in battle","Strange daughter talk","Chance to revive after death"],
    22: ["UTAGE opening song in battle","Twilight ending song in battle","Character theme song in battle","Ally theme song in battle","Last gallery song in battle","Gray and Gold item effects swapped"],
    23: ["Hatena Box set piece 1","Hatena Box set piece 2","Hatena Box set piece 3","Hatena Box set piece 4"],
    24: ["EXP set piece 1","EXP set piece 2","EXP set piece 3","EXP set piece 4"],
    25: ["Zenny set piece 1","Zenny set piece 2","Zenny set piece 3","Zenny set piece 4"],
    26: ["Golden Armor set piece 1","Piece 2","Piece 3","Piece 4"],
    27: ["Luck set piece 1","Piece 2","Piece 3","Piece 4"],
    28: ["Hisahide PI: Permanent Blaze Border","Kojuro PI: Permanent Moonless Slaughter","Sasuke PI: Shadow clone on dash/jump/evade","Hideaki PI: Triangle=lobster, heal on eat","Tenkai PI: Permanent Ecstasy mode","Yoshiaki PI: Taunt=Play Dead, fills HP & BASARA"],
    29: ["Muneshige PI: Permanent Thunder King, +2 hits chainsaw","Sorin PI: Convert absorbs 5x damage, no 3rd Super time limit","Ieyasu PI: Permanent Hood mode","Mitsunari PI: Max speed for Reverence, Dark +15%, instant skill startup","Yoshitsugu PI: +3 hit & dark element when locked on","Magoichi PI: Pistol shots are rockets"],
    30: ["Kanbei PI: Bomb on dodge, longer skill duration","Tsuruhime PI: Trap enemies in bubble on dash","Masamune PI: Permanent Six Claws mode","Yukimura PI: Permanent Fired Up mode","Keiji PI: Taunt makes enemies dance, fills BASARA","Motochika PI: Net damages enemies, can trap Tadakatsu/Yoshitsugu/Sorin"],
    31: ["Motonari PI: Super armor when setting traps","Yoshihiro PI: All enemies/allies die in one hit","Tadakatsu PI: All Supers no time limit, no health drain","Kotaro PI: All aerial attacks critical, +3 hits","Oichi PI: Revive once during battle","Nobunaga PI: Greatly extend Battle Boost & Drive duration"],
    32: ["Kenshin PI: Extend God Region, +speed, Ice element","Kasuga PI: Release binding wires on moves/skills","Toshiie PI: Permanent Rice Ball mode","Matsu PI: Animal attacks 2x power","Ujimasa PI: Moxibustion & Past Glory 3x longer","Shingen PI: Permanent Fu-Rin-Ka-Zan mode"],
}

set_bonuses = {
    23: "SET BONUS: Grants up to 4 more Hatena Boxes after battle",
    24: "SET BONUS: Full set grants extra 5,000 EXP after battle",
    25: "SET BONUS: Full set grants extra 5,000 zenny after battle",
    26: "SET BONUS: Grants up to 4 golden armors after battle. Disables blocking & dodging",
    27: "SET BONUS: Full set grants incredible luck, but disables all healing",
}

row_categories = {
    1:"Life & Attack (S/M/L)", 2:"Defence & Recovery", 3:"BASARA Art & Drive Attack",
    4:"Camp Commander & Elemental", 5:"Guard Break & Stun Resistance",
    6:"Base Capture & BASARA Assist", 7:"Near Death & Aerial",
    8:"Full Gauge & S-String First Hit", 9:"Parry & Time Attack",
    10:"Guard Heal & Enemy Weaken", 11:"Zenny per Kill & Luck",
    12:"Elemental Proof (Allies)", 13:"Anti-Soldier Types",
    14:"Critical & Special Effects", 15:"Combo & Gauge Management",
    16:"Speed & BASARA Gauge", 17:"Defense & Parry",
    18:"Horse & Risk/Reward", 19:"EXP & Money Strategies",
    20:"Money & Utility", 21:"Cosmetic & Audio",
    22:"Music & Effect Swap",
    23:"Hatena Box Set (4 pieces)", 24:"EXP Bonus Set (4 pieces)",
    25:"Zenny Bonus Set (4 pieces)", 26:"Golden Armor Set (4 pieces)",
    27:"Luck Set (4 pieces, no healing)",
    28:"Personal Items - Row 1", 29:"Personal Items - Row 2",
    30:"Personal Items - Row 3", 31:"Personal Items - Row 4",
    32:"Personal Items - Row 5",
}

# Build HTML
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sengoku Basara 3: Utage - Complete English Guide</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#1a1a2e; color:#e0e0e0; font-family:'Segoe UI','Hiragino Sans','Noto Sans JP',sans-serif; line-height:1.6; padding:20px; }
  .container { max-width:1200px; margin:0 auto; }
  h1 { text-align:center; font-size:2em; color:#ff6b35; text-shadow:0 0 20px rgba(255,107,53,0.3); padding:30px 0; border-bottom:2px solid #ff6b35; margin-bottom:20px; }
  h2 { color:#ff6b35; font-size:1.5em; margin:30px 0 15px; padding-bottom:8px; border-bottom:1px solid #333; }
  h3 { color:#f0a500; margin:20px 0 10px; font-size:1.15em; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:10px; }
  .card { background:#16213e; border:1px solid #333; border-radius:8px; padding:8px 12px; display:flex; align-items:flex-start; gap:10px; transition:transform 0.15s,box-shadow 0.15s; }
  .card:hover { transform:translateY(-2px); box-shadow:0 4px 12px rgba(255,107,53,0.15); }
  .card img { width:48px; height:48px; object-fit:contain; flex-shrink:0; image-rendering:pixelated; background:#0a0a1a; border-radius:4px; border:1px solid #333; }
  .card .info { flex:1; }
  .card .pos { color:#555; font-size:0.7em; }
  .card .desc { color:#ccc; font-size:0.82em; }
  .nav { position:sticky; top:0; background:#1a1a2e; z-index:100; padding:10px 0; margin-bottom:20px; border-bottom:1px solid #333; display:flex; flex-wrap:wrap; gap:6px; justify-content:center; }
  .nav a { color:#ff6b35; text-decoration:none; padding:5px 10px; border:1px solid #333; border-radius:4px; font-size:0.8em; transition:all 0.15s; }
  .nav a:hover { background:#ff6b35; color:#1a1a2e; }
  .section { margin-bottom:40px; }
  table { width:100%; border-collapse:collapse; margin:10px 0; }
  th { background:#16213e; color:#ff6b35; padding:8px 12px; text-align:left; border-bottom:2px solid #333; }
  td { padding:8px 12px; border-bottom:1px solid #222; }
  tr:hover td { background:#16213e; }
  .jp { color:#e94560; font-weight:bold; }
  .romaji { color:#888; font-size:0.85em; }
  .note { background:#16213e; border-left:3px solid #ff6b35; padding:12px 16px; margin:10px 0; border-radius:4px; }
  .footer { text-align:center; color:#555; padding:20px 0; border-top:1px solid #333; margin-top:40px; }
  .set-badge { display:inline-block; padding:1px 6px; background:#f0a50022; color:#f0a500; border:1px solid #f0a500; border-radius:3px; font-size:0.65em; margin-right:4px; }
  .pi-badge { display:inline-block; padding:1px 6px; background:#e94560; color:#fff; border-radius:3px; font-size:0.65em; margin-right:4px; }
  .set-banner { grid-column:1/-1; background:#f0a50015; border:1px solid #f0a500; border-radius:8px; padding:12px 16px; text-align:center; color:#f0a500; font-weight:bold; }
</style>
</head>
<body>
<div class="container">
<h1>Sengoku Basara 3: Utage<br>Complete English Translation Guide</h1>
<p style="text-align:center; color:#888; margin-bottom:20px;">BLJM60389 &middot; All 192 accessory icons from Sengoku BASARA Wiki (Fandom) &middot; Weapon icons from game data</p>

<div class="nav">
  <a href="#main">Main Menu</a>
  <a href="#options">Options</a>
  <a href="#prep">Battle Prep</a>
  <a href="#equipment">Equipment</a>
  <a href="#shop">Shop</a>
  <a href="#hud">Battle HUD</a>
  <a href="#results">Results</a>
  <a href="#weapons">Weapons</a>
  <a href="#accessories">Accessories (192)</a>
  <a href="#items">Items</a>
  <a href="#terms">Terms</a>
  <a href="#utage">Utage Mode</a>
  <a href="#difficulty">Difficulty</a>
  <a href="#system">System Messages</a>
</div>
"""

# ===== MAIN MENU =====
html += """
<div class="section" id="main">
<h2>Main Menu (&#x30E1;&#x30A4;&#x30F3;&#x30E1;&#x30CB;&#x30E5;&#x30FC;)</h2>
<table>
<tr><th>#</th><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td>1</td><td class="jp">&#x5408;&#x6226;</td><td class="romaji">Kassen</td><td>Battle / Campaign</td><td>Story mode - main campaign</td></tr>
<tr><td>2</td><td class="jp">&#x5929;&#x4E0B;&#x7D71;&#x4E00;</td><td class="romaji">Tenka Toitsu</td><td>Unification</td><td>Conquest mode - unify Japan</td></tr>
<tr><td>3</td><td class="jp">&#x5BB4;&#x30E2;&#x30FC;&#x30C9;</td><td class="romaji">Utage Mode</td><td>Utage (Party) Mode</td><td>Party/mini-game mode</td></tr>
<tr><td>4</td><td class="jp">&#x6B66;&#x8005;&#x4FEE;&#x884C;</td><td class="romaji">Musha Shugyo</td><td>Warrior Training</td><td>Free battle / practice</td></tr>
<tr><td>5</td><td class="jp">&#x6B66;&#x5BB6;&#x5C4B;&#x6577;</td><td class="romaji">Buke Yashiki</td><td>Samurai Estate</td><td>Gallery / character viewer</td></tr>
<tr><td>6</td><td class="jp">&#x30AE;&#x30E3;&#x30E9;&#x30EA;&#x30FC;</td><td class="romaji">Gallery</td><td>Gallery</td><td>View unlocked art/sprites</td></tr>
<tr><td>7</td><td class="jp">&#x8A2D;&#x5B9A;</td><td class="romaji">Settei</td><td>Settings / Options</td><td>Game options</td></tr>
<tr><td>8</td><td class="jp">&#x30C7;&#x30FC;&#x30BF;&#x30ED;&#x30FC;&#x30C9;</td><td class="romaji">Data Load</td><td>Load Data</td><td>Load save file</td></tr>
</table>
</div>
"""

# ===== OPTIONS =====
html += """
<div class="section" id="options">
<h2>Options (&#x8A2D;&#x5B9A;)</h2>
<h3>Display Settings</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x753B;&#x9762;&#x30E2;&#x30FC;&#x30C9;</td><td class="romaji">Gamen Mode</td><td>Screen Mode</td></tr>
<tr><td class="jp">&#x30EF;&#x30A4;&#x30C9;&#x30B9;&#x30AF;&#x30EA;&#x30FC;&#x30F3;</td><td class="romaji">Widescreen</td><td>Widescreen (16:9)</td></tr>
<tr><td class="jp">&#x30B9;&#x30BF;&#x30F3;&#x30C0;&#x30FC;&#x30C9;</td><td class="romaji">Standard</td><td>Standard (4:3)</td></tr>
<tr><td class="jp">&#x30D6;&#x30E9;&#x30A4;&#x30C8;&#x30CD;&#x30B9;</td><td class="romaji">Brightness</td><td>Brightness</td></tr>
<tr><td class="jp">&#x5B57;&#x5E55;&#x8868;&#x793A;</td><td class="romaji">Subtitle Display</td><td>Subtitle Display</td></tr>
</table>
<h3>Sound Settings</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">BGM&#x97F3;&#x91CF;</td><td class="romaji">BGM Onryo</td><td>BGM Volume</td></tr>
<tr><td class="jp">SE&#x97F3;&#x91CF;</td><td class="romaji">SE Onryo</td><td>Sound Effects Volume</td></tr>
<tr><td class="jp">&#x30DC;&#x30A4;&#x30B9;&#x97F3;&#x91CF;</td><td class="romaji">Voice Onryo</td><td>Voice Volume</td></tr>
<tr><td class="jp">&#x97F3;&#x58F0;&#x51FA;&#x529B;</td><td class="romaji">Audio Output</td><td>Audio Output</td></tr>
</table>
<h3>Game Settings</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x632F;&#x52D5;</td><td class="romaji">Shindo</td><td>Vibration</td></tr>
<tr><td class="jp">&#x30AB;&#x30E1;&#x30E9;&#x611F;&#x5EA6;</td><td class="romaji">Camera Kando</td><td>Camera Sensitivity</td></tr>
<tr><td class="jp">&#x30AB;&#x30E1;&#x30E9;&#x53CD;&#x8EE2;</td><td class="romaji">Camera Hanten</td><td>Invert Camera</td></tr>
<tr><td class="jp">&#x7E26;&#x65B9;&#x5411;</td><td class="romaji">Vertical</td><td>Vertical (axis)</td></tr>
<tr><td class="jp">&#x6A2A;&#x65B9;&#x5411;</td><td class="romaji">Horizontal</td><td>Horizontal (axis)</td></tr>
<tr><td class="jp">&#x30AA;&#x30FC;&#x30C8;&#x30BB;&#x30FC;&#x30D6;</td><td class="romaji">Auto-Save</td><td>Auto-Save</td></tr>
<tr><td class="jp">&#x96E3;&#x6613;&#x5EA6;</td><td class="romaji">Nan'ido</td><td>Difficulty</td></tr>
<tr><td class="jp">&#x64CD;&#x4F5C;&#x30BF;&#x30A4;&#x30D7;</td><td class="romaji">Control Type</td><td>Control Type</td></tr>
<tr><td class="jp">&#x30BF;&#x30A4;&#x30D7;A</td><td class="romaji">Type A</td><td>Type A (Default)</td></tr>
<tr><td class="jp">&#x30BF;&#x30A4;&#x30D7;B</td><td class="romaji">Type B</td><td>Type B (Alternate)</td></tr>
</table>
</div>
"""

# ===== BATTLE PREP =====
html += """
<div class="section" id="prep">
<h2>Battle Preparation</h2>
<table>
<tr><th>#</th><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td>1</td><td class="jp">&#x51FA;&#x9673;</td><td class="romaji">Shutsujin</td><td>Deploy / Start Battle</td><td>Begin the battle</td></tr>
<tr><td>2</td><td class="jp">&#x6B66;&#x5C06;&#x9078;&#x629E;</td><td class="romaji">Busho Sentaku</td><td>Select Officer</td><td>Choose your character</td></tr>
<tr><td>3</td><td class="jp">&#x88C5;&#x5099;&#x5909;&#x66F4;</td><td class="romaji">Sobi Henko</td><td>Change Equipment</td><td>Weapons, armor, accessories</td></tr>
<tr><td>4</td><td class="jp">&#x6280;&#x80FD;</td><td class="romaji">Gino</td><td>Skills / Arts</td><td>View/change character skills</td></tr>
<tr><td>5</td><td class="jp">&#x30D1;&#x30E9;&#x30E1;&#x30FC;&#x30BF;</td><td class="romaji">Parameters</td><td>Parameters / Stats</td><td>View character stats</td></tr>
<tr><td>6</td><td class="jp">&#x9663;&#x5F62;</td><td class="romaji">Jinkei</td><td>Formation</td><td>Choose troop formation</td></tr>
<tr><td>7</td><td class="jp">&#x6226;&#x6CC1;</td><td class="romaji">Senkyo</td><td>Battle Conditions</td><td>View battle objectives</td></tr>
<tr><td>8</td><td class="jp">&#x6575;&#x60C5;&#x5831;</td><td class="romaji">Teki Joho</td><td>Enemy Info</td><td>View enemy officers</td></tr>
<tr><td>9</td><td class="jp">&#x5408;&#x6226;&#x60C5;&#x5831;</td><td class="romaji">Kassen Joho</td><td>Battle Info</td><td>View stage details</td></tr>
<tr><td>10</td><td class="jp">&#x6B66;&#x5C06;&#x5207;&#x66FF;</td><td class="romaji">Busho Kirikae</td><td>Switch Officer</td><td>Change playable character</td></tr>
<tr><td>11</td><td class="jp">&#x5F15;&#x7C60;&#x308A;</td><td class="romaji">Hikikomori</td><td>Return / Withdraw</td><td>Exit to previous menu</td></tr>
</table>
<h3>Equipment Sub-Menu</h3>
<table>
<tr><th>#</th><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td>1</td><td class="jp">&#x6B66;&#x5668;</td><td class="romaji">Buki</td><td>Weapon</td></tr>
<tr><td>2</td><td class="jp">&#x9632;&#x5177;</td><td class="romaji">Bogu</td><td>Armor</td></tr>
<tr><td>3</td><td class="jp">&#x88C5;&#x98FE;&#x54C1;</td><td class="romaji">Soshokuhin</td><td>Accessory (3 slots)</td></tr>
</table>
<h3>Parameters</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x529B;</td><td class="romaji">Chikara</td><td>Strength</td></tr>
<tr><td class="jp">&#x6280;</td><td class="romaji">Waza</td><td>Technique</td></tr>
<tr><td class="jp">&#x901F;</td><td class="romaji">Hayasa</td><td>Speed</td></tr>
<tr><td class="jp">&#x904B;</td><td class="romaji">Un</td><td>Luck</td></tr>
</table>
</div>
"""

# ===== EQUIPMENT =====
html += """
<div class="section" id="equipment">
<h2>Equipment Details</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x653B;&#x6483;&#x529B;</td><td class="romaji">Kogekiryoku</td><td>Attack Power</td><td>Weapon attack stat</td></tr>
<tr><td class="jp">&#x9632;&#x5FA1;&#x529B;</td><td class="romaji">Bogyoryoku</td><td>Defense Power</td><td>Armor defense stat</td></tr>
<tr><td class="jp">&#x5C5E;&#x6027;</td><td class="romaji">Zokusei</td><td>Element / Attribute</td><td>Fire, Ice, Lightning, etc.</td></tr>
<tr><td class="jp">&#x30EC;&#x30A2;&#x30EA;&#x30C6;&#x30A3;</td><td class="romaji">Rarity</td><td>Rarity</td><td>Item rarity tier</td></tr>
<tr><td class="jp">&#x88C5;&#x5099;&#x6761;&#x4EF6;</td><td class="romaji">Sobi Joken</td><td>Equip Requirement</td><td>Level/stat needed</td></tr>
<tr><td class="jp">&#x88C5;&#x5099;&#x4E2D;</td><td class="romaji">Sobichu</td><td>Equipped</td><td>Currently equipped</td></tr>
<tr><td class="jp">&#x672A;&#x88C5;&#x5099;</td><td class="romaji">Misobi</td><td>Unequipped</td><td>Not equipped</td></tr>
<tr><td class="jp">&#x65B0;&#x898F;</td><td class="romaji">Shinki</td><td>New</td><td>Newly acquired item</td></tr>
<tr><td class="jp">LV</td><td class="romaji">Level</td><td>Level</td><td>Item/weapon level</td></tr>
</table>
<h3>Rarity Tiers</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Color</th></tr>
<tr><td class="jp">&#x4E26;</td><td class="romaji">Nami</td><td>Common</td><td>Gray</td></tr>
<tr><td class="jp">&#x826F;</td><td class="romaji">Yoshi</td><td>Uncommon</td><td>Green</td></tr>
<tr><td class="jp">&#x6975;&#x4E0A;</td><td class="romaji">Gokujo</td><td>Rare</td><td>Blue</td></tr>
<tr><td class="jp">&#x81F3;&#x6975;</td><td class="romaji">Shigoku</td><td>Epic</td><td>Gold</td></tr>
<tr><td class="jp">&#x5929;&#x6674;</td><td class="romaji">Appare</td><td>Legendary</td><td>Red</td></tr>
</table>
</div>
"""

# ===== SHOP =====
html += """
<div class="section" id="shop">
<h2>Shop</h2>
<table>
<tr><th>#</th><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td>1</td><td class="jp">&#x8CFC;&#x5165;</td><td class="romaji">Konyu</td><td>Buy</td><td>Purchase items</td></tr>
<tr><td>2</td><td class="jp">&#x58F2;&#x5374;</td><td class="romaji">Baikyaku</td><td>Sell</td><td>Sell items</td></tr>
<tr><td>3</td><td class="jp">&#x8CB7;&#x53D6;</td><td class="romaji">Kaitori</td><td>Buyback</td><td>Buy back sold items</td></tr>
<tr><td>4</td><td class="jp">&#x5F37;&#x5316;</td><td class="romaji">Kyoka</td><td>Upgrade</td><td>Strengthen equipment</td></tr>
<tr><td>5</td><td class="jp">&#x5408;&#x6210;</td><td class="romaji">Gosei</td><td>Synthesis</td><td>Combine items</td></tr>
<tr><td>6</td><td class="jp">&#x5206;&#x89E3;</td><td class="romaji">Bunkai</td><td>Dismantle</td><td>Break down items</td></tr>
<tr><td>7</td><td class="jp">&#x9451;&#x5B9A;</td><td class="romaji">Kantei</td><td>Appraise</td><td>Identify unknown items</td></tr>
</table>
<h3>Shop Types</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x6B66;&#x5668;&#x5C4B;</td><td class="romaji">Bukiya</td><td>Weapon Shop</td></tr>
<tr><td class="jp">&#x9632;&#x5177;&#x5C4B;</td><td class="romaji">Boguya</td><td>Armor Shop</td></tr>
<tr><td class="jp">&#x96D1;&#x8CA8;&#x5C4B;</td><td class="romaji">Zakkaya</td><td>General Store</td></tr>
<tr><td class="jp">&#x935B;&#x51B6;&#x5C4B;</td><td class="romaji">Kajiya</td><td>Blacksmith</td></tr>
</table>
</div>
"""

# ===== BATTLE HUD =====
html += """
<div class="section" id="hud">
<h2>Battle HUD</h2>
<h3>On-Screen Display</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x4F53;&#x529B;</td><td class="romaji">Tairyoku</td><td>HP / Health</td><td>Green health bar</td></tr>
<tr><td class="jp">&#x30D0;&#x30B5;&#x30E9;&#x30B2;&#x30FC;&#x30B8;</td><td class="romaji">Basara Gauge</td><td>Basara Gauge</td><td>Special attack meter</td></tr>
<tr><td class="jp">&#x9023;&#x6483;&#x6570;</td><td class="romaji">Rengekisu</td><td>Combo Count</td><td>Hit counter</td></tr>
<tr><td class="jp">&#x6483;&#x7834;&#x6570;</td><td class="romaji">Gekibasu</td><td>Kills / Defeated</td><td>Enemies defeated</td></tr>
<tr><td class="jp">&#x6B8B;&#x308A;&#x6642;&#x9593;</td><td class="romaji">Time Remaining</td><td>Time Remaining</td><td>Battle timer</td></tr>
</table>
<h3>Battlefield Elements</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x5236;&#x5727;</td><td class="romaji">Seiatsu</td><td>Capture / Control</td><td>Battlefield capture points</td></tr>
<tr><td class="jp">&#x5473;&#x65B9;</td><td class="romaji">Mikata</td><td>Allies</td><td>Friendly forces</td></tr>
<tr><td class="jp">&#x6575;</td><td class="romaji">Teki</td><td>Enemies</td><td>Hostile forces</td></tr>
<tr><td class="jp">&#x6B66;&#x5C06;</td><td class="romaji">Busho</td><td>Officer</td><td>Named commander</td></tr>
<tr><td class="jp">&#x672C;&#x9663;</td><td class="romaji">Honjin</td><td>Main Camp / HQ</td><td>Destroy to win</td></tr>
<tr><td class="jp">&#x782D;</td><td class="romaji">Toride</td><td>Fort / Stronghold</td><td>Capturable base</td></tr>
</table>
<h3>Soldier Types</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x8DB3;&#x8EFD;</td><td class="romaji">Ashigaru</td><td>Foot Soldiers</td></tr>
<tr><td class="jp">&#x5F13;&#x5175;</td><td class="romaji">Yumihei</td><td>Archers</td></tr>
<tr><td class="jp">&#x9A0E;&#x99AC;&#x5175;</td><td class="romaji">Kibahei</td><td>Cavalry</td></tr>
<tr><td class="jp">&#x5FCD;&#x8005;</td><td class="romaji">Ninja</td><td>Ninja</td></tr>
</table>
<h3>Battle Actions</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x901A;&#x5E38;&#x653B;&#x6483;</td><td class="romaji">Tsujo Kogeki</td><td>Normal Attack</td></tr>
<tr><td class="jp">&#x56FA;&#x6709;&#x6280;</td><td class="romaji">Koyugi</td><td>Unique Skill</td></tr>
<tr><td class="jp">&#x56FA;&#x6709;&#x5965;&#x7FA9;</td><td class="romaji">Koyu Ogi</td><td>Super Move</td></tr>
<tr><td class="jp">&#x30D0;&#x30B5;&#x30E9;&#x653B;&#x6483;</td><td class="romaji">Basara Kogeki</td><td>Basara Attack</td></tr>
<tr><td class="jp">&#x30BF;&#x30E1;&#x653B;&#x6483;</td><td class="romaji">Tame Kogeki</td><td>Charge Attack</td></tr>
<tr><td class="jp">&#x30AC;&#x30FC;&#x30C9;</td><td class="romaji">Guard</td><td>Guard / Block</td></tr>
<tr><td class="jp">&#x56DE;&#x907F;</td><td class="romaji">Kaihi</td><td>Dodge / Evade</td></tr>
<tr><td class="jp">&#x5F3E;&#x304D;</td><td class="romaji">Hajiki</td><td>Parry</td></tr>
<tr><td class="jp">&#x5D29;&#x3057;</td><td class="romaji">Kuzushi</td><td>Guard Break</td></tr>
<tr><td class="jp">&#x6C17;&#x7D76;</td><td class="romaji">Kizetsu</td><td>Stunned</td></tr>
</table>
</div>
"""

# ===== RESULTS =====
html += """
<div class="section" id="results">
<h2>Battle Results</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x52DD;&#x5229;</td><td class="romaji">Shori</td><td>Victory</td><td>Win</td></tr>
<tr><td class="jp">&#x6577;&#x5317;</td><td class="romaji">Haiboku</td><td>Defeat</td><td>Lost</td></tr>
<tr><td class="jp">&#x6226;&#x529F;</td><td class="romaji">Senko</td><td>Battle Merit / Score</td><td>Performance rating</td></tr>
<tr><td class="jp">&#x8A55;&#x4FA1;</td><td class="romaji">Hyoka</td><td>Grade</td><td>S/A/B/C/D rank</td></tr>
<tr><td class="jp">&#x6483;&#x7834;&#x6570;</td><td class="romaji">Gekibasu</td><td>Enemies Defeated</td><td>Total kills</td></tr>
<tr><td class="jp">&#x6700;&#x5927;&#x9023;&#x6483;&#x6570;</td><td class="romaji">Max Combo</td><td>Max Combo</td><td>Highest combo</td></tr>
<tr><td class="jp">&#x5408;&#x6226;&#x6642;&#x9593;</td><td class="romaji">Kassen Jikan</td><td>Battle Time</td><td>Duration</td></tr>
<tr><td class="jp">&#x7372;&#x5F97;&#x7D4C;&#x9A13;&#x5024;</td><td class="romaji">EXP Gained</td><td>EXP Gained</td><td></td></tr>
<tr><td class="jp">&#x7372;&#x5F97;&#x91D1;</td><td class="romaji">Gold Earned</td><td>Gold Earned</td><td></td></tr>
<tr><td class="jp">&#x7372;&#x5F97;&#x30A2;&#x30A4;&#x30C6;&#x30E0;</td><td class="romaji">Items Acquired</td><td>Items Acquired</td><td></td></tr>
<tr><td class="jp">&#x6B66;&#x52F3;</td><td class="romaji">Bukun</td><td>Merit Points</td><td>Merit currency</td></tr>
<tr><td class="jp">&#x30EC;&#x30D9;&#x30EB;&#x30A2;&#x30C3;&#x30D7;</td><td class="romaji">Level Up</td><td>Level Up</td><td></td></tr>
<tr><td class="jp">&#x79F0;&#x53F7;</td><td class="romaji">Shogo</td><td>Title / Epithet</td><td>New title earned</td></tr>
</table>
</div>
"""

# ===== WEAPONS =====
html += '<div class="section" id="weapons"><h2>Weapon Type Icons</h2><div class="note">Icons extracted from game data files (DXT5 textures).</div><div class="grid">\n'
char_weapons = [
    (0,"Date Masamune","Dragon Claws"),(1,"Sanada Yukimura","Twin Spears"),
    (2,"Maeda Keiji","Odachi"),(3,"Tokugawa Ieyasu","Fists"),
    (4,"Ishida Mitsunari","Longsword-Iai"),(5,"Oda Nobunaga","Shotgun Sword"),
    (6,"Akechi Mitsuhide","Katana"),(7,"Mori Motonari","Ring Blade"),
    (8,"Chosokabe Motochika","Shamisen-Harpoon"),(9,"Kuroda Kanbei","Iron Ball"),
    (10,"Takeda Shingen","War Fan"),(11,"Uesugi Kenshin","Katana"),
    (12,"Hojo Ujimasa","Spear"),(13,"Oichi","Dark Hands"),
    (14,"Matsu","Rifle-Bayonet"),(15,"Shimazu Yoshihiro","Broadsword"),
    (16,"Fuma Kotaro","Dual Blades"),(17,"Honda Tadakatsu","Drill Spear"),
    (18,"Zabby","Fan-Umbrella"),(19,"Katsuie","Axe"),
    (20,"Sarutobi Sasuke","Dual Claws"),(21,"Kasuga","Dual Daggers"),
    (22,"Kobayakawa Takakage","Rod/Staff"),(23,"Mogami Yoshiaki","Rapier"),
    (24,"Tsutsui Junkei","Spear"),(25,"Otani Yoshitsugu","Cane Sword"),
    (26,"Tachibana Muneshige","Shield Sword"),(27,"Tenkai","Staff/Scepter"),
    (28,"Matsunaga Hisahide","Kunai/Blade"),(29,"Katakura Kojuro","Sword"),
]
for idx,char,weapon in char_weapons:
    icon = wep_icons.get(idx,"")
    html += f'  <div class="card">{icon_html(icon)}<div class="info"><b>{char}</b><div class="desc">{weapon}</div></div></div>\n'
html += "</div>\n</div>\n"

# ===== ACCESSORIES =====
html += '<div class="section" id="accessories"><h2>Accessories - All 192 Items with Real Icons</h2>\n<div class="note">All 182 accessory icons from Sengoku BASARA Wiki (Fandom). Rows 1-22 have 6 items each (132 items). Rows 23-27 are 4-piece sets with set bonuses (20 items + 5 bonuses). Rows 28-32 are Personal Items (30 items). Total: 192 items.</div>\n'

for row_num in range(1, 33):
    category = row_categories.get(row_num, f"Row {row_num}")
    is_set = row_num in [23,24,25,26,27]
    is_pi = row_num >= 28
    html += f'<h3>Row {row_num}: {category}</h3>\n<div class="grid">\n'
    icons = row_icons.get(row_num, [])
    descs = row_descs.get(row_num, [])
    for col in range(len(icons)):
        pos_key = icons[col]
        icon = wiki_icons.get(pos_key, "")
        desc = descs[col] if col < len(descs) else ""
        badge = '<span class="set-badge">SET</span>' if is_set else ''
        pi_badge = '<span class="pi-badge">PI</span>' if is_pi else ''
        pos_label = f"[{row_num}-{col+1}]"
        html += f'  <div class="card">{icon_html(icon)}<div class="info"><span class="pos">{pos_label}</span> {badge}{pi_badge}<div class="desc">{desc}</div></div></div>\n'
    if is_set:
        bonus = set_bonuses.get(row_num, "")
        html += f'  <div class="set-banner">{bonus}</div>\n'
    html += "</div>\n"

html += "</div>\n"

# ===== ITEMS, TERMS, UTAGE, DIFFICULTY, SYSTEM =====
html += """
<div class="section" id="items">
<h2>Items</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x56DE;&#x5FA9;&#x85AC;</td><td class="romaji">Kaifukuyaku</td><td>Recovery Medicine</td><td>Restores HP</td></tr>
<tr><td class="jp">&#x5927;&#x56DE;&#x5FA9;&#x85AC;</td><td class="romaji">Greater Recovery</td><td>Greater Recovery</td><td>Restores more HP</td></tr>
<tr><td class="jp">&#x7279;&#x52B9;&#x85AC;</td><td class="romaji">Tokkoyaku</td><td>Special Medicine</td><td>Full HP restore</td></tr>
<tr><td class="jp">&#x30D0;&#x30B5;&#x30E9;&#x56DE;&#x5FA9;&#x85AC;</td><td class="romaji">Basara Recovery</td><td>Basara Restorative</td><td>Fills Basara gauge</td></tr>
<tr><td class="jp">&#x6BD2;&#x6D88;&#x3057;</td><td class="romaji">Dokukeshi</td><td>Antidote</td><td>Cures poison</td></tr>
<tr><td class="jp">&#x76EE;&#x85AC;</td><td class="romaji">Megusuri</td><td>Eye Drops</td><td>Cures blindness</td></tr>
<tr><td class="jp">&#x98FD;&#x7DCA;&#x306E;&#x672D;</td><td class="romaji">Izuna Talisman</td><td>Izuna Talisman</td><td>Revive fallen ally</td></tr>
<tr><td class="jp">&#x6226;&#x795E;&#x306E;&#x8B77;&#x7B26;</td><td class="romaji">War God Talisman</td><td>War God's Talisman</td><td>Temp attack/defense boost</td></tr>
<tr><td class="jp">&#x4FEE;&#x7F85;&#x306E;&#x9B42;</td><td class="romaji">Shura Soul</td><td>Asura Soul</td><td>Temp invincibility</td></tr>
<tr><td class="jp">&#x9B42;&#x306E;&#x5668;</td><td class="romaji">Soul Vessel</td><td>Soul Vessel</td><td>Gain EXP instantly</td></tr>
<tr><td class="jp">&#x6B66;&#x52F3;&#x306E;&#x8A3C;</td><td class="romaji">Merit Token</td><td>Merit Token</td><td>Gain merit points</td></tr>
</table>
</div>

<div class="section" id="terms">
<h2>Game Terms</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x30D0;&#x30B5;&#x30E9;</td><td class="romaji">Basara</td><td>Basara</td><td>Extreme/audacious spirit</td></tr>
<tr><td class="jp">&#x5929;&#x4E0B;</td><td class="romaji">Tenka</td><td>The Land</td><td>Japan</td></tr>
<tr><td class="jp">&#x5929;&#x4E0B;&#x7D71;&#x4E00;</td><td class="romaji">Tenka Toitsu</td><td>Unification</td><td>Goal: unify the land</td></tr>
<tr><td class="jp">&#x6226;&#x56FD;</td><td class="romaji">Sengoku</td><td>Warring States</td><td>The Sengoku era</td></tr>
<tr><td class="jp">&#x5BB4;</td><td class="romaji">Utage</td><td>Banquet / Party</td><td>Game subtitle</td></tr>
<tr><td class="jp">&#x5408;&#x6226;</td><td class="romaji">Kassen</td><td>Battle</td><td>Story battles</td></tr>
<tr><td class="jp">&#x6B66;&#x5C06;</td><td class="romaji">Busho</td><td>Officer / Warlord</td><td>Playable &amp; enemy characters</td></tr>
<tr><td class="jp">&#x56FA;&#x6709;&#x6280;</td><td class="romaji">Koyugi</td><td>Unique Skill</td><td>Character-specific moves</td></tr>
<tr><td class="jp">&#x56FA;&#x6709;&#x5965;&#x7FA9;</td><td class="romaji">Koyu Ogi</td><td>Super Move</td><td>Uses Basara gauge</td></tr>
<tr><td class="jp">&#x30C9;&#x30E9;&#x30A4;&#x30D6;</td><td class="romaji">Drive</td><td>Drive</td><td>Boost mode</td></tr>
<tr><td class="jp">&#x899A;&#x9192;</td><td class="romaji">Kakusei</td><td>Awakening</td><td>Powered-up state</td></tr>
<tr><td class="jp">&#x5C5E;&#x6027;</td><td class="romaji">Zokusei</td><td>Element</td><td>Fire, Ice, Lightning, etc.</td></tr>
<tr><td class="jp">&#x72B6;&#x614B;&#x7570;&#x5E38;</td><td class="romaji">Status Ailment</td><td>Status Ailment</td><td>Poison, Stun, Seal, etc.</td></tr>
<tr><td class="jp">&#x6BD2;</td><td class="romaji">Doku</td><td>Poison</td><td>HP drains over time</td></tr>
<tr><td class="jp">&#x6C17;&#x7D76;</td><td class="romaji">Kizetsu</td><td>Stun</td><td>Cannot move</td></tr>
<tr><td class="jp">&#x5C01;&#x5370;</td><td class="romaji">Fuin</td><td>Seal</td><td>Skills locked</td></tr>
<tr><td class="jp">&#x6697;&#x95C7;</td><td class="romaji">Kurayami</td><td>Blind</td><td>Screen darkened</td></tr>
<tr><td class="jp">&#x51CD;&#x7D50;</td><td class="romaji">Toketsu</td><td>Freeze</td><td>Frozen in place</td></tr>
<tr><td class="jp">&#x71C3;&#x713C;</td><td class="romaji">Nensho</td><td>Burn</td><td>Fire damage over time</td></tr>
<tr><td class="jp">&#x9EBB;&#x75F9;</td><td class="romaji">Mahi</td><td>Paralysis</td><td>Movement slowed</td></tr>
</table>
</div>

<div class="section" id="utage">
<h2>Utage / Party Mode</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp">&#x5BB4;&#x30E2;&#x30FC;&#x30C9;</td><td class="romaji">Utage Mode</td><td>Party Mode</td><td>Main Utage menu</td></tr>
<tr><td class="jp">&#x6771;&#x6D77;&#x9053;&#x4E94;&#x5341;&#x4E09;&#x6B21;</td><td class="romaji">Tokaido 53 Stations</td><td>53 Stations of Tokaido</td><td>Endless survival - 53 stages</td></tr>
<tr><td class="jp">&#x6226;&#x56FD;&#x30C0;&#x30FC;&#x30C4;</td><td class="romaji">Sengoku Darts</td><td>Warring Darts</td><td>Dart mini-game</td></tr>
<tr><td class="jp">&#x6226;&#x56FD;&#x30C1;&#x30A7;&#x30A4;&#x30B9;</td><td class="romaji">Sengoku Chase</td><td>Warring Chase</td><td>Tag/chase mini-game</td></tr>
<tr><td class="jp">&#x6226;&#x56FD;&#x30D3;&#x30F3;&#x30B4;</td><td class="romaji">Sengoku Bingo</td><td>Warring Bingo</td><td>Bingo mini-game</td></tr>
<tr><td class="jp">&#x6226;&#x56FD;&#x8FB2;&#x5BB6;</td><td class="romaji">Sengoku Noka</td><td>Warring Farmer</td><td>Farming mini-game</td></tr>
<tr><td class="jp">&#x5929;&#x4E0B;&#x4E00;&#x6B66;&#x9053;&#x4F1A;</td><td class="romaji">Tenkaichi Budokai</td><td>Tournament</td><td>Bracket tournament mode</td></tr>
<tr><td class="jp">&#x5927;&#x6311;&#x6226;</td><td class="romaji">Dai Chosen</td><td>Grand Challenge</td><td>Survival/boss rush</td></tr>
</table>
</div>

<div class="section" id="difficulty">
<h2>Difficulty</h2>
<table>
<tr><th>#</th><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td>1</td><td class="jp">&#x3084;&#x3055;&#x3057;&#x3044;</td><td class="romaji">Yasashii</td><td>Easy</td><td>Low enemy HP &amp; aggression</td></tr>
<tr><td>2</td><td class="jp">&#x3075;&#x3064;&#x3046;</td><td class="romaji">Futsu</td><td>Normal</td><td>Standard difficulty</td></tr>
<tr><td>3</td><td class="jp">&#x3080;&#x305A;&#x304B;&#x3057;&#x3044;</td><td class="romaji">Muzukashii</td><td>Hard</td><td>Higher enemy stats</td></tr>
<tr><td>4</td><td class="jp">&#x7A76;&#x6975;</td><td class="romaji">Kikyoku</td><td>Extreme</td><td>Massive enemy damage</td></tr>
<tr><td>5</td><td class="jp">&#x4FEE;&#x7F85;</td><td class="romaji">Shura</td><td>Asura / Nightmare</td><td>Hardest mode</td></tr>
</table>
</div>

<div class="section" id="system">
<h2>System Messages</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp">&#x30BB;&#x30FC;&#x30D6;&#x3057;&#x307E;&#x3059;&#x304B;&#xFF1F;</td><td class="romaji">Save?</td><td>Would you like to save?</td></tr>
<tr><td class="jp">&#x30BB;&#x30FC;&#x30D6;&#x3057;&#x307E;&#x3057;&#x305F;</td><td class="romaji">Saved</td><td>Saved successfully.</td></tr>
<tr><td class="jp">&#x30ED;&#x30FC;&#x30C9;&#x3057;&#x3066;&#x3044;&#x307E;&#x3059;</td><td class="romaji">Loading</td><td>Loading...</td></tr>
<tr><td class="jp">&#x30C7;&#x30FC;&#x30BF;&#x304C;&#x7834;&#x640D;&#x3057;&#x3066;&#x3044;&#x307E;&#x3059;</td><td class="romaji">Data Corrupted</td><td>Data is corrupted.</td></tr>
<tr><td class="jp">&#x4E0A;&#x66F8;&#x304D;&#x3057;&#x307E;&#x3059;&#x304B;&#xFF1F;</td><td class="romaji">Overwrite?</td><td>Overwrite existing data?</td></tr>
<tr><td class="jp">&#x306F;&#x3044;</td><td class="romaji">Hai</td><td>Yes</td></tr>
<tr><td class="jp">&#x3044;&#x3044;&#x3048;</td><td class="romaji">Iie</td><td>No</td></tr>
<tr><td class="jp">&#x623B;&#x308B;</td><td class="romaji">Modoru</td><td>Return / Back</td></tr>
<tr><td class="jp">&#x6C7A;&#x5B9A;</td><td class="romaji">Kettei</td><td>Confirm / OK</td></tr>
<tr><td class="jp">&#x30AD;&#x30E3;&#x30F3;&#x30BB;&#x30EB;</td><td class="romaji">Cancel</td><td>Cancel</td></tr>
<tr><td class="jp">&#x88C5;&#x5099;&#x3057;&#x307E;&#x3057;&#x305F;</td><td class="romaji">Equipped</td><td>Equipped.</td></tr>
<tr><td class="jp">&#x8CFC;&#x5165;&#x3057;&#x307E;&#x3057;&#x305F;</td><td class="romaji">Purchased</td><td>Purchased.</td></tr>
<tr><td class="jp">&#x6240;&#x6301;&#x91D1;&#x304C;&#x8DB3;&#x308A;&#x307E;&#x305B;&#x3093;</td><td class="romaji">Not Enough Gold</td><td>Not enough gold.</td></tr>
<tr><td class="jp">&#x30EC;&#x30D9;&#x30EB;&#x304C;&#x4E0A;&#x304C;&#x3063;&#x305F;</td><td class="romaji">Level Up</td><td>Level increased!</td></tr>
<tr><td class="jp">&#x79F0;&#x53F7;&#x3092;&#x7372;&#x5F97;</td><td class="romaji">Title Earned</td><td>Earned a new title!</td></tr>
<tr><td class="jp">&#x89E3;&#x9664;</td><td class="romaji">Kaijo</td><td>Unlocked</td></tr>
</table>
</div>

<div class="footer">
  <p>Sengoku Basara 3: Utage (BLJM60389) - Complete Fan Translation Reference Guide</p>
  <p>All 182 accessory icons from Sengoku BASARA Wiki (Fandom). Weapon icons extracted from game data.</p>
  <p>Not affiliated with Capcom. For personal use with RPCS3 emulator.</p>
</div>
</div>
</body>
</html>
"""

with open(out_html, 'w') as f:
    f.write(html)

print(f"HTML saved: {out_html}")
print(f"Size: {os.path.getsize(out_html)/1024:.0f} KB")
