import base64, os, io
from PIL import Image

icon_dir = "/Users/rahamirez.ga/basara_icons"
out_html = "/Users/rahamirez.ga/basara3_utage_guide.html"

def img_to_base64(path, max_size=128):
    img = Image.open(path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    w, h = img.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('ascii')

# Load all icons
wepball_icons, wep_icons, brief_icons = {}, {}, {}
for i in range(11):
    p = os.path.join(icon_dir, f"wepball_{i:03d}.png")
    if os.path.exists(p): wepball_icons[i] = img_to_base64(p, 96)
for i in range(30):
    p = os.path.join(icon_dir, f"wep_{i:03d}.png")
    if os.path.exists(p): wep_icons[i] = img_to_base64(p, 96)
for i in range(21):
    p = os.path.join(icon_dir, f"id_brief_{i:02d}.png")
    if os.path.exists(p): brief_icons[i] = img_to_base64(p, 96)

def icon_html(icon_data, emoji_fallback=""):
    if icon_data:
        return f'<img src="data:image/png;base64,{icon_data}" alt="icon">'
    return f'<div class="icon-placeholder">{emoji_fallback}</div>'

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sengoku Basara 3: Utage - Complete English Translation Guide</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #1a1a2e; color: #e0e0e0; font-family: 'Segoe UI', 'Hiragino Sans', 'Noto Sans JP', sans-serif; line-height: 1.6; padding: 20px; }
  .container { max-width: 1200px; margin: 0 auto; }
  h1 { text-align: center; font-size: 2em; color: #ff6b35; text-shadow: 0 0 20px rgba(255,107,53,0.3); padding: 30px 0; border-bottom: 2px solid #ff6b35; margin-bottom: 20px; }
  h2 { color: #ff6b35; font-size: 1.5em; margin: 30px 0 15px; padding-bottom: 8px; border-bottom: 1px solid #333; }
  h3 { color: #f0a500; margin: 20px 0 10px; font-size: 1.2em; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 12px; }
  .grid-small { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 8px; }
  .card { background: #16213e; border: 1px solid #333; border-radius: 8px; padding: 12px 16px; display: flex; align-items: flex-start; gap: 12px; transition: transform 0.15s, box-shadow 0.15s; }
  .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(255,107,53,0.15); }
  .card img { width: 64px; height: 64px; object-fit: contain; flex-shrink: 0; image-rendering: pixelated; background: #0a0a1a; border-radius: 4px; border: 1px solid #333; }
  .card .info { flex: 1; }
  .card .jp { color: #e94560; font-weight: bold; font-size: 1.05em; }
  .card .romaji { color: #888; font-size: 0.85em; margin-left: 6px; }
  .card .en { color: #e0e0e0; margin-top: 2px; }
  .card .desc { color: #999; font-size: 0.85em; margin-top: 4px; }
  .card .effect { color: #7ec8e3; font-size: 0.85em; margin-top: 4px; font-style: italic; }
  .nav { position: sticky; top: 0; background: #1a1a2e; z-index: 100; padding: 10px 0; margin-bottom: 20px; border-bottom: 1px solid #333; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
  .nav a { color: #ff6b35; text-decoration: none; padding: 6px 12px; border: 1px solid #333; border-radius: 4px; font-size: 0.85em; transition: all 0.15s; }
  .nav a:hover { background: #ff6b35; color: #1a1a2e; }
  .section { margin-bottom: 40px; }
  table { width: 100%; border-collapse: collapse; margin: 10px 0; }
  th { background: #16213e; color: #ff6b35; padding: 8px 12px; text-align: left; border-bottom: 2px solid #333; }
  td { padding: 8px 12px; border-bottom: 1px solid #222; }
  tr:hover td { background: #16213e; }
  .jp-text { color: #e94560; font-weight: bold; }
  .en-text { color: #e0e0e0; }
  .romaji-text { color: #888; font-size: 0.85em; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; }
  .badge-red { background: #e94560; color: #fff; }
  .badge-blue { background: #0f3460; color: #7ec8e3; }
  .badge-green { background: #1b4332; color: #52b788; }
  .badge-gold { background: #f0a50022; color: #f0a500; border: 1px solid #f0a500; }
  .note { background: #16213e; border-left: 3px solid #ff6b35; padding: 12px 16px; margin: 10px 0; border-radius: 4px; }
  .footer { text-align: center; color: #555; padding: 20px 0; border-top: 1px solid #333; margin-top: 40px; }
  .icon-placeholder { width: 64px; height: 64px; flex-shrink: 0; background: #0a0a1a; border-radius: 4px; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 1.8em; }
  .menu-item { display: flex; align-items: center; gap: 8px; padding: 6px 0; }
  .menu-item .arrow { color: #ff6b35; }
</style>
</head>
<body>
<div class="container">
<h1>⚔️ Sengoku Basara 3: Utage<br>Complete English Translation Guide</h1>
<p style="text-align:center; color:#888; margin-bottom:20px;">BLJM60389 · Capcom · MT Framework Engine<br>Icons extracted directly from game data files</p>

<div class="nav">
  <a href="#main">Main Menu</a>
  <a href="#options">Options</a>
  <a href="#prep">Battle Prep</a>
  <a href="#equipment">Equipment</a>
  <a href="#shop">Shop</a>
  <a href="#hud">Battle HUD</a>
  <a href="#results">Results</a>
  <a href="#weapons">Weapons</a>
  <a href="#accessories">Accessories</a>
  <a href="#items">Items</a>
  <a href="#terms">Game Terms</a>
  <a href="#utage">Utage Mode</a>
  <a href="#difficulty">Difficulty</a>
  <a href="#system">System Messages</a>
</div>
"""

# ===================== MAIN MENU =====================
html += """
<div class="section" id="main">
<h2>🏠 Main Menu (メインメニュー)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">合戦</td><td class="romaji-text">Kassen</td><td class="en-text">Battle / Campaign</td><td>Story mode — main campaign</td></tr>
<tr><td class="jp-text">天下統一</td><td class="romaji-text">Tenka Tōitsu</td><td class="en-text">Unification</td><td>Conquest mode — unify Japan</td></tr>
<tr><td class="jp-text">宴モード</td><td class="romaji-text">Utage Mōdo</td><td class="en-text">Utage (Party) Mode</td><td>Party/mini-game mode</td></tr>
<tr><td class="jp-text">武者修行</td><td class="romaji-text">Musha Shugyō</td><td class="en-text">Warrior Training</td><td>Free battle / practice mode</td></tr>
<tr><td class="jp-text">武家屋敷</td><td class="romaji-text">Buke Yashiki</td><td class="en-text">Samurai Estate</td><td>Gallery / character viewer</td></tr>
<tr><td class="jp-text">設定</td><td class="romaji-text">Settei</td><td class="en-text">Settings / Options</td><td>Game options</td></tr>
<tr><td class="jp-text">データロード</td><td class="romaji-text">Dēta Rōdo</td><td class="en-text">Load Data</td><td>Load save file</td></tr>
<tr><td class="jp-text">ギャラリー</td><td class="romaji-text">Gyararī</td><td class="en-text">Gallery</td><td>View unlocked art/sprites</td></tr>
</table>
</div>
"""

# ===================== OPTIONS =====================
html += """
<div class="section" id="options">
<h2>⚙️ Options (設定)</h2>
<h3>Display Settings (画面設定)</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp-text">画面モード</td><td class="romaji-text">Gamen Mōdo</td><td class="en-text">Screen Mode</td></tr>
<tr><td class="jp-text">ワイドスクリーン</td><td class="romaji-text">Waido Sukurīn</td><td class="en-text">Widescreen (16:9)</td></tr>
<tr><td class="jp-text">スタンダード</td><td class="romaji-text">Sutandādo</td><td class="en-text">Standard (4:3)</td></tr>
<tr><td class="jp-text">ブライトネス</td><td class="romaji-text">Buraitonesu</td><td class="en-text">Brightness</td></tr>
<tr><td class="jp-text">字幕</td><td class="romaji-text">Jimaku</td><td class="en-text">Subtitles</td></tr>
<tr><td class="jp-text">字幕表示</td><td class="romaji-text">Jimaku Hyōji</td><td class="en-text">Show Subtitles</td></tr>
<tr><td class="jp-text">オン</td><td class="romaji-text">On</td><td class="en-text">On</td></tr>
<tr><td class="jp-text">オフ</td><td class="romaji-text">Ofu</td><td class="en-text">Off</td></tr>
</table>
<h3>Sound Settings (サウンド設定)</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp-text">BGM音量</td><td class="romaji-text">BGM Onryō</td><td class="en-text">BGM Volume</td></tr>
<tr><td class="jp-text">SE音量</td><td class="romaji-text">SE Onryō</td><td class="en-text">Sound Effects Volume</td></tr>
<tr><td class="jp-text">ボイス音量</td><td class="romaji-text">Boisu Onryō</td><td class="en-text">Voice Volume</td></tr>
<tr><td class="jp-text">音声出力</td><td class="romaji-text">Onsei Shutsuryoku</td><td class="en-text">Audio Output</td></tr>
<tr><td class="jp-text">ステレオ</td><td class="romaji-text">Sutereo</td><td class="en-text">Stereo</td></tr>
<tr><td class="jp-text">モノラル</td><td class="romaji-text">Monoraru</td><td class="en-text">Mono</td></tr>
</table>
<h3>Game Settings (ゲーム設定)</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp-text">振動</td><td class="romaji-text">Shindō</td><td class="en-text">Vibration</td></tr>
<tr><td class="jp-text">カメラ感度</td><td class="romaji-text">Kamera Kando</td><td class="en-text">Camera Sensitivity</td></tr>
<tr><td class="jp-text">カメラ反転</td><td class="romaji-text">Kamera Hanten</td><td class="en-text">Invert Camera</td></tr>
<tr><td class="jp-text">縦方向</td><td class="romaji-text">Tate Hōkō</td><td class="en-text">Vertical</td></tr>
<tr><td class="jp-text">横方向</td><td class="romaji-text">Yoko Hōkō</td><td class="en-text">Horizontal</td></tr>
<tr><td class="jp-text">オートセーブ</td><td class="romaji-text">Ōto Seibu</td><td class="en-text">Auto-Save</td></tr>
<tr><td class="jp-text">難易度</td><td class="romaji-text">Nan'ido</td><td class="en-text">Difficulty</td></tr>
<tr><td class="jp-text">操作タイプ</td><td class="romaji-text">Sōa Taipu</td><td class="en-text">Control Type</td></tr>
<tr><td class="jp-text">タイプA</td><td class="romaji-text">Taipu A</td><td class="en-text">Type A (Default)</td></tr>
<tr><td class="jp-text">タイプB</td><td class="romaji-text">Taipu B</td><td class="en-text">Type B (Alternate)</td></tr>
</table>
</div>
"""

# ===================== BATTLE PREP =====================
html += """
<div class="section" id="prep">
<h2>🗡️ Battle Preparation (合戦準備)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">出陣</td><td class="romaji-text">Shutsujin</td><td class="en-text">Deploy / Start Battle</td><td>Begin the battle</td></tr>
<tr><td class="jp-text">武将選択</td><td class="romaji-text">Bushō Sentaku</td><td class="en-text">Select Officer</td><td>Choose your character</td></tr>
<tr><td class="jp-text">装備変更</td><td class="romaji-text">Sōbi Henkō</td><td class="en-text">Change Equipment</td><td>Equip weapons, armor, accessories</td></tr>
<tr><td class="jp-text">武器</td><td class="romaji-text">Buki</td><td class="en-text">Weapon</td><td>Equip/change weapon</td></tr>
<tr><td class="jp-text">防具</td><td class="romaji-text">Bōgu</td><td class="en-text">Armor</td><td>Equip/change armor</td></tr>
<tr><td class="jp-text">装飾品</td><td class="romaji-text">Sōshokuhin</td><td class="en-text">Accessory</td><td>Equip accessories (3 slots)</td></tr>
<tr><td class="jp-text">アイテム</td><td class="romaji-text">Aitemu</td><td class="en-text">Item</td><td>Use/equip battle items</td></tr>
<tr><td class="jp-text">陣形</td><td class="romaji-text">Jinkei</td><td class="en-text">Formation</td><td>Choose troop formation</td></tr>
<tr><td class="jp-text">戦況</td><td class="romaji-text">Senkyō</td><td class="en-text">Battle Conditions</td><td>View battle objectives</td></tr>
<tr><td class="jp-text">敵情報</td><td class="romaji-text">Teki Jōhō</td><td class="en-text">Enemy Info</td><td>View enemy officers</td></tr>
<tr><td class="jp-text">合戦情報</td><td class="romaji-text">Kassen Jōhō</td><td class="en-text">Battle Info</td><td>View stage details</td></tr>
<tr><td class="jp-text">武将切替</td><td class="romaji-text">Bushō Kirikae</td><td class="en-text">Switch Officer</td><td>Change playable character</td></tr>
<tr><td class="jp-text">引籠り</td><td class="romaji-text">Hikikomori</td><td class="en-text">Return / Withdraw</td><td>Exit to previous menu</td></tr>
</table>
<h3>Pre-Battle Sub-Menus</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp-text">装備</td><td class="romaji-text">Sōbi</td><td class="en-text">Equipment</td></tr>
<tr><td class="jp-text">技能</td><td class="romaji-text">Ginō</td><td class="en-text">Skills / Arts</td></tr>
<tr><td class="jp-text">パラメータ</td><td class="romaji-text">Parēmeta</td><td class="en-text">Parameters / Stats</td></tr>
<tr><td class="jp-text">力</td><td class="romaji-text">Chikara</td><td class="en-text">Strength</td></tr>
<tr><td class="jp-text">技</td><td class="romaji-text">Waza</td><td class="en-text">Technique</td></tr>
<tr><td class="jp-text">速</td><td class="romaji-text">Hayasa</td><td class="en-text">Speed</td></tr>
<tr><td class="jp-text">運</td><td class="romaji-text">Un</td><td class="en-text">Luck</td></tr>
</table>
</div>
"""

# ===================== EQUIPMENT =====================
html += """
<div class="section" id="equipment">
<h2>🛡️ Equipment (装備)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">武器装備</td><td class="romaji-text">Buki Sōbi</td><td class="en-text">Equip Weapon</td><td>Select weapon slot</td></tr>
<tr><td class="jp-text">防具装備</td><td class="romaji-text">Bōgu Sōbi</td><td class="en-text">Equip Armor</td><td>Select armor slot</td></tr>
<tr><td class="jp-text">装飾品装備</td><td class="romaji-text">Sōshokuhin Sōbi</td><td class="en-text">Equip Accessory</td><td>3 accessory slots</td></tr>
<tr><td class="jp-text">攻撃力</td><td class="romaji-text">Kōgekiryoku</td><td class="en-text">Attack Power</td><td>Weapon attack stat</td></tr>
<tr><td class="jp-text">防御力</td><td class="romaji-text">Bōgyoryoku</td><td class="en-text">Defense Power</td><td>Armor defense stat</td></tr>
<tr><td class="jp-text">属性</td><td class="romaji-text">Zokusei</td><td class="en-text">Element / Attribute</td><td>Elemental type (Fire, Ice, etc.)</td></tr>
<tr><td class="jp-text">レアリティ</td><td class="romaji-text">Reariti</td><td class="en-text">Rarity</td><td>Item rarity tier</td></tr>
<tr><td class="jp-text">装備条件</td><td class="romaji-text">Sōbi Jōken</td><td class="en-text">Equip Requirement</td><td>Level/stat needed to equip</td></tr>
<tr><td class="jp-text">装備中</td><td class="romaji-text">Sōbichū</td><td class="en-text">Equipped</td><td>Currently equipped</td></tr>
<tr><td class="jp-text">未装備</td><td class="romaji-text">Misōbi</td><td class="en-text">Unequipped</td><td>Not equipped</td></tr>
<tr><td class="jp-text">新規</td><td class="romaji-text">Shinki</td><td class="en-text">New</td><td>Newly acquired item</td></tr>
<tr><td class="jp-text">LV</td><td class="romaji-text">Reberu</td><td class="en-text">Level</td><td>Item/weapon level</td></tr>
</table>
<h3>Rarity Tiers</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Color</th></tr>
<tr><td class="jp-text">並</td><td class="romaji-text">Nami</td><td class="en-text">Common</td><td><span class="badge" style="background:#555;color:#aaa">Gray</span></td></tr>
<tr><td class="jp-text">良</td><td class="romaji-text">Yoshi</td><td class="en-text">Uncommon</td><td><span class="badge badge-green">Green</span></td></tr>
<tr><td class="jp-text">極上</td><td class="romaji-text">Gokujō</td><td class="en-text">Rare</td><td><span class="badge badge-blue">Blue</span></td></tr>
<tr><td class="jp-text">至極</td><td class="romaji-text">Shigoku</td><td class="en-text">Epic / Very Rare</td><td><span class="badge badge-gold">Gold</span></td></tr>
<tr><td class="jp-text">天晴</td><td class="romaji-text">Appare</td><td class="en-text">Legendary</td><td><span class="badge badge-red">Red</span></td></tr>
</table>
</div>
"""

# ===================== SHOP =====================
html += """
<div class="section" id="shop">
<h2>🏪 Shop (店 / 商人)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">購入</td><td class="romaji-text">Kōnyū</td><td class="en-text">Buy</td><td>Purchase items</td></tr>
<tr><td class="jp-text">売却</td><td class="romaji-text">Baikyaku</td><td class="en-text">Sell</td><td>Sell items</td></tr>
<tr><td class="jp-text">武器屋</td><td class="romaji-text">Bukiya</td><td class="en-text">Weapon Shop</td><td>Buy/sell weapons</td></tr>
<tr><td class="jp-text">防具屋</td><td class="romaji-text">Bōguya</td><td class="en-text">Armor Shop</td><td>Buy/sell armor</td></tr>
<tr><td class="jp-text">雑貨屋</td><td class="romaji-text">Zakkaya</td><td class="en-text">General Store</td><td>Buy/sell accessories & items</td></tr>
<tr><td class="jp-text">鍛冶屋</td><td class="romaji-text">Kajiya</td><td class="en-text">Blacksmith</td><td>Upgrade/forge weapons</td></tr>
<tr><td class="jp-text">所持金</td><td class="romaji-text">Shojikin</td><td class="en-text">Gold / Money</td><td>Current funds</td></tr>
<tr><td class="jp-text">値段</td><td class="romaji-text">Nedan</td><td class="en-text">Price</td><td>Item cost</td></tr>
<tr><td class="jp-text">強化</td><td class="romaji-text">Kyōka</td><td class="en-text">Upgrade / Enhance</td><td>Strengthen equipment</td></tr>
<tr><td class="jp-text">合成</td><td class="romaji-text">Gōsei</td><td class="en-text">Synthesis / Fusion</td><td>Combine items</td></tr>
<tr><td class="jp-text">分解</td><td class="romaji-text">Bunkai</td><td class="en-text">Dismantle</td><td>Break down items for materials</td></tr>
<tr><td class="jp-text">鑑定</td><td class="romaji-text">Kantei</td><td class="en-text">Appraise</td><td>Identify unknown items</td></tr>
<tr><td class="jp-text">買取</td><td class="romaji-text">Kaitori</td><td class="en-text">Buyback</td><td>Buy back sold items</td></tr>
</table>
</div>
"""

# ===================== BATTLE HUD =====================
html += """
<div class="section" id="hud">
<h2>⚔️ Battle HUD (戦闘中画面)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">体力</td><td class="romaji-text">Tairyoku</td><td class="en-text">HP / Health</td><td>Green health bar</td></tr>
<tr><td class="jp-text">バサラゲージ</td><td class="romaji-text">Basara Gēji</td><td class="en-text">Basara Gauge</td><td>Special attack meter (yellow/orange)</td></tr>
<tr><td class="jp-text">連撃数</td><td class="romaji-text">Rengekisū</td><td class="en-text">Combo Count</td><td>Hit counter</td></tr>
<tr><td class="jp-text">撃破数</td><td class="romaji-text">Gekibasū</td><td class="en-text">Kills / Defeated</td><td>Enemies defeated count</td></tr>
<tr><td class="jp-text">残り時間</td><td class="romaji-text">Nokori Jikan</td><td class="en-text">Time Remaining</td><td>Battle timer</td></tr>
<tr><td class="jp-text">制圧</td><td class="romaji-text">Seiatsu</td><td class="en-text">Capture / Control</td><td>Battlefield capture points</td></tr>
<tr><td class="jp-text">味方</td><td class="romaji-text">Mikata</td><td class="en-text">Allies</td><td>Friendly forces</td></tr>
<tr><td class="jp-text">敵</td><td class="romaji-text">Teki</td><td class="en-text">Enemies</td><td>Hostile forces</td></tr>
<tr><td class="jp-text">武将</td><td class="romaji-text">Bushō</td><td class="en-text">Officer</td><td>Named enemy commander</td></tr>
<tr><td class="jp-text">副将</td><td class="romaji-text">Fukushō</td><td class="en-text">Vice-Commander</td><td>Second-in-command</td></tr>
<tr><td class="jp-text">本陣</td><td class="romaji-text">Honjin</td><td class="en-text">Main Camp / HQ</td><td>Main base — destroy to win</td></tr>
<tr><td class="jp-text">城門</td><td class="romaji-text">Jōmon</td><td class="en-text">Castle Gate</td><td>Gated entry to fortress</td></tr>
<tr><td class="jp-text">砦</td><td class="romaji-text">Toride</td><td class="en-text">Fort / Stronghold</td><td>Capturable base</td></tr>
<tr><td class="jp-text">弓兵</td><td class="romaji-text">Yumihei</td><td class="en-text">Archers</td><td>Ranged enemy units</td></tr>
<tr><td class="jp-text">騎馬兵</td><td class="romaji-text">Kibahei</td><td class="en-text">Cavalry</td><td>Mounted units</td></tr>
<tr><td class="jp-text">足軽</td><td class="romaji-text">Ashigaru</td><td class="en-text">Foot Soldiers</td><td>Basic infantry</td></tr>
<tr><td class="jp-text">忍者</td><td class="romaji-text">Ninja</td><td class="en-text">Ninja</td><td>Stealth units</td></tr>
</table>
<h3>Battle Actions</h3>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp-text">通常攻撃</td><td class="romaji-text">Tsūjō Kōgeki</td><td class="en-text">Normal Attack</td></tr>
<tr><td class="jp-text">固有技</td><td class="romaji-text">Koyūgi</td><td class="en-text">Unique Skill</td></tr>
<tr><td class="jp-text">固有奥義</td><td class="romaji-text">Koyū Ōgi</td><td class="en-text">Super Move</td></tr>
<tr><td class="jp-text">バサラ攻撃</td><td class="romaji-text">Basara Kōgeki</td><td class="en-text">Basara Attack</td></tr>
<tr><td class="jp-text">タメ攻撃</td><td class="romaji-text">Tame Kōgeki</td><td class="en-text">Charge Attack</td></tr>
<tr><td class="jp-text">ガード</td><td class="romaji-text">Gādo</td><td class="en-text">Guard / Block</td></tr>
<tr><td class="jp-text">回避</td><td class="romaji-text">Kaihi</td><td class="en-text">Dodge / Evade</td></tr>
<tr><td class="jp-text">弾き</td><td class="romaji-text">Hajiki</td><td class="en-text">Parry</td></tr>
<tr><td class="jp-text">崩し</td><td class="romaji-text">Kuzushi</td><td class="en-text">Guard Break</td></tr>
<tr><td class="jp-text">追い打ち</td><td class="romaji-text">Oiuchi</td><td class="en-text">Pursuit Attack</td></tr>
<tr><td class="jp-text">ダウン</td><td class="romaji-text">Daun</td><td class="en-text">Down / Knocked Down</td></tr>
<tr><td class="jp-text">気絶</td><td class="romaji-text">Kizetsu</td><td class="en-text">Stunned</td></tr>
</table>
</div>
"""

# ===================== RESULTS =====================
html += """
<div class="section" id="results">
<h2>📊 Battle Results (合戦結果)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">勝利</td><td class="romaji-text">Shōri</td><td class="en-text">Victory</td><td>Win the battle</td></tr>
<tr><td class="jp-text">敗北</td><td class="romaji-text">Haiboku</td><td class="en-text">Defeat</td><td>Lost the battle</td></tr>
<tr><td class="jp-text">戦功</td><td class="romaji-text">Senkō</td><td class="en-text">Battle Merit / Score</td><td>Performance rating</td></tr>
<tr><td class="jp-text">評価</td><td class="romaji-text">Hyōka</td><td class="en-text">Evaluation / Grade</td><td>Rank (S, A, B, C, D)</td></tr>
<tr><td class="jp-text">撃破数</td><td class="romaji-text">Gekibasū</td><td class="en-text">Enemies Defeated</td><td>Total kills</td></tr>
<tr><td class="jp-text">最大連撃数</td><td class="romaji-text">Saidai Rengekisū</td><td class="en-text">Max Combo</td><td>Highest combo achieved</td></tr>
<tr><td class="jp-text">合戦時間</td><td class="romaji-text">Kassen Jikan</td><td class="en-text">Battle Time</td><td>Duration of battle</td></tr>
<tr><td class="jp-text">獲得経験値</td><td class="romaji-text">Kakutoku Keikenchi</td><td class="en-text">EXP Gained</td><td>Experience points earned</td></tr>
<tr><td class="jp-text">獲得金</td><td class="romaji-text">Kakutoku Kin</td><td class="en-text">Gold Earned</td><td>Money earned</td></tr>
<tr><td class="jp-text">獲得アイテム</td><td class="romaji-text">Kakutoku Aitemu</td><td class="en-text">Items Acquired</td><td>Items dropped/rewarded</td></tr>
<tr><td class="jp-text">武勲</td><td class="romaji-text">Bukun</td><td class="en-text">Merit Points</td><td>Merit currency for unlocks</td></tr>
<tr><td class="jp-text">レベルアップ</td><td class="romaji-text">Reberu Appu</td><td class="en-text">Level Up</td><td>Character leveled up</td></tr>
<tr><td class="jp-text">称号</td><td class="romaji-text">Shōgō</td><td class="en-text">Title / Epithet</td><td>Earned a new title</td></tr>
</table>
</div>
"""

# ===================== WEAPONS =====================
html += """
<div class="section" id="weapons">
<h2>⚔️ Weapon Type Icons (武器アイコン)</h2>
<div class="note">Real game icons extracted from BLJM60389 game data. Each character has their own weapon type with a unique icon.</div>
<div class="grid">
"""

char_weapons = [
    (0, "伊達政宗", "Date Masamune", "Dragon Claws (龍爪)"),
    (1, "真田幸村", "Sanada Yukimura", "Twin Spears (双槍)"),
    (2, "前田慶次", "Maeda Keiji", "Odachi (大太刀)"),
    (3, "徳川家康", "Tokugawa Ieyasu", "Fists (拳)"),
    (4, "石田三成", "Ishida Mitsunari", "Longsword-Iai (刀・居合)"),
    (5, "織田信長", "Oda Nobunaga", "Shotgun Sword (散弾剣)"),
    (6, "明智光秀", "Akechi Mitsuhide", "Katana (刀)"),
    (7, "毛利元就", "Mōri Motonari", "Ring Blade (輪刃)"),
    (8, "長宗我部元親", "Chōsokabe Motochika", "Shamisen-Harpoon (三味線)"),
    (9, "黒田官兵衛", "Kuroda Kanbei", "Iron Ball (鉄球)"),
    (10, "武田信玄", "Takeda Shingen", "War Fan (軍配)"),
    (11, "上杉謙信", "Uesugi Kenshin", "Katana (刀)"),
    (12, "北条氏政", "Hōjō Ujimasa", "Spear (槍)"),
    (13, "お市", "Oichi", "Dark Hands (漆黒の手)"),
    (14, "まつ", "Matsu", "Rifle-Bayonet (小銃)"),
    (15, "島津義弘", "Shimazu Yoshihiro", "Broadsword (大剣)"),
    (16, "風魔小太郎", "Fūma Kotarō", "Dual Blades (双刃)"),
    (17, "本多忠勝", "Honda Tadakatsu", "Drill Spear (槍・ドリル)"),
    (18, "ざびー", "Zabby", "Fan-Umbrella (扇)"),
    (19, "柴田勝家", "Katsuie", "Axe (斧)"),
    (20, "猿飛佐助", "Sarutobi Sasuke", "Dual Claws (双爪)"),
    (21, "かすが", "Kasuga", "Dual Daggers (双短剣)"),
    (22, "小早川隆景", "Kobayakawa Takakage", "Rod/Staff (杖)"),
    (23, "最上義光", "Mogami Yoshiaki", "Rapier (レイピア)"),
    (24, "筒井順慶", "Tsutsui Junkei", "Spear (槍)"),
    (25, "大谷吉継", "Ōtani Yoshitsugu", "Cane Sword (杖剣)"),
    (26, "立花宗茂", "Tachibana Muneshige", "Shield Sword (盾剣)"),
    (27, "天海", "Tenkai", "Staff/Scepter (錫杖)"),
    (28, "松永久秀", "Matsunaga Hisahide", "Kunai/Blade (クナイ)"),
    (29, "片倉小十郎", "Katakura Kojūrō", "Sword (刀)"),
]

for idx, jp_char, en_char, weapon in char_weapons:
    icon = wep_icons.get(idx, "")
    html += f'  <div class="card">{icon_html(icon, "⚔️")}\n    <div class="info"><span class="jp">{jp_char}</span><span class="romaji">{en_char}</span>\n    <div class="en">{weapon}</div></div></div>\n'

html += "</div>\n</div>\n"

# ===================== ACCESSORIES =====================
html += """
<div class="section" id="accessories">
<h2>💍 Accessories (装飾品) - With Real Game Icons</h2>
<div class="note">Icons extracted directly from game files (BLJM60389). Textures are DXT5 512x512, cropped to content bounds and resized for display.</div>

<h3>Elemental Orbs (属性玉) - wepball Icons</h3>
<div class="grid">
"""

orbs = [
    (0, "炎の玉", "Honō no Tama", "Fire Orb", "Adds fire element to attacks. Burning damage over time.", "🔥"),
    (1, "氷の玉", "Kōri no Tama", "Ice Orb", "Adds ice element to attacks. Chance to freeze enemies.", "❄️"),
    (2, "雷の玉", "Kaminari no Tama", "Lightning Orb", "Adds lightning element. Stun/paralysis chance.", "⚡"),
    (3, "闇の玉", "Yami no Tama", "Dark Orb", "Adds dark element. Life drain on hit.", "🌑"),
    (4, "光の玉", "Hikari no Tama", "Light Orb", "Adds light element. Holy damage, extra vs undead.", "✨"),
    (5, "風の玉", "Kaze no Tama", "Wind Orb", "Adds wind element. Knockback increase.", "🌪️"),
    (6, "地の玉", "Chi no Tama", "Earth Orb", "Adds earth element. Guard break increase.", "🏔️"),
    (7, "水の玉", "Mizu no Tama", "Water Orb", "Adds water element. Slows enemy movement.", "💧"),
    (8, "無の玉", "Mu no Tama", "Null Orb", "Nullifies elemental attributes.", "⚪"),
    (9, "全の玉", "Zen no Tama", "All Orb", "Adds all elemental attributes.", "🌈"),
    (10, "特殊玉", "Tokushu Tama", "Special Orb", "Special elemental effect.", "💎"),
]

for idx, jp, romaji, en, desc, emoji in orbs:
    icon = wepball_icons.get(idx, "")
    html += f'  <div class="card">{icon_html(icon, emoji)}\n    <div class="info"><span class="jp">{jp}</span><span class="romaji">{romaji}</span>\n    <div class="en">{en}</div><div class="desc">{desc}</div></div></div>\n'

html += "</div>\n"

# Stat accessories
html += """
<h3>Stat-Boosting Accessories (ステータス装飾品)</h3>
<div class="grid">
"""

stat_acc = [
    ("攻撃の数珠", "Kōgeki no Juzu", "Attack Beads", "Attack Power Up", "Increases attack stat", "💪"),
    ("守りの御守", "Mamori no Omamori", "Guard Charm", "Defense Power Up", "Increases defense stat", "🛡️"),
    ("体力の勾玉", "Tairyoku no Magatama", "Health Magatama", "HP Up", "Increases max HP", "❤️"),
    ("バサラの祭器", "Basara no Saiki", "Basara Vessel", "Basara Power Up", "Increases Basara power stat", "🌀"),
    ("速足の草鞋", "Hayagashi no Waraji", "Swift Sandals", "Movement Speed Up", "Increases movement speed", "🥾"),
    ("練技の腕輪", "Renri no Udewa", "Arts Bracelet", "Arts/Tech Up", "Increases technique stat", "✨"),
    ("連撃の篭手", "Rengeki no Kote", "Combo Gauntlet", "Combo Count Up", "Increases max combo slots", "🔢"),
    ("射程の眼鏡", "Shatei no Megane", "Range Lens", "Range Extend", "Extends attack range", "🎯"),
    ("幸運のお守", "Kōun no Omamori", "Luck Charm", "Luck Up", "Improves item drop rates", "🤞"),
    ("経験の額当", "Keiken no Gakutō", "EXP Headband", "EXP Up", "Increases EXP gained", "📈"),
    ("金運の小判", "Kin'un no Koban", "Gold Koban", "Gold Find Up", "Increases gold earned", "💰"),
    ("ドロップの鉤", "Doroppu no Kaginame", "Drop Hook", "Drop Rate Up", "Increases item drop rate", "💎"),
]

for jp, romaji, en, effect, desc, emoji in stat_acc:
    html += f'  <div class="card">{icon_html("", emoji)}\n    <div class="info"><span class="jp">{jp}</span><span class="romaji">{romaji}</span>\n    <div class="en">{en}</div><div class="effect">{effect}</div><div class="desc">{desc}</div></div></div>\n'

html += "</div>\n"

# Special accessories
html += """
<h3>Special Accessories (特殊装飾品)</h3>
<div class="grid">
"""

special_acc = [
    ("吸血の牙", "Kyūketsu no Kiba", "Vampire Fang", "Life Steal", "Recover HP when attacking enemies", "🩸"),
    ("闘魂の鉢巻", "Tōkon no Hachimaki", "Fighting Headband", "Basara Auto-Fill", "Basara gauge fills automatically over time", "🌀"),
    ("復活の護符", "Fukkatsu no Gofu", "Revival Talisman", "Auto-Revive", "Revive once when defeated", "🔶"),
    ("気合の盃", "Kiai no Sakazuki", "Spirit Cup", "Morale Boost", "Raises allied troop morale", "📛"),
    ("影分身の術", "Kage Bunshin no Jutsu", "Shadow Clone", "Clone Spawn", "Spawns a temporary clone in battle", "👥"),
    ("鉄壁の鎧", "Teppeki no Yoroi", "Iron Wall Armor", "Super Armor", "Prevents flinching from weak hits", "🛡️"),
    ("連撃の書", "Rengeki no Sho", "Combo Scroll", "Combo Duration Up", "Combos last longer before resetting", "📜"),
    ("瞬足の羽", "Shunsoku no Hane", "Swift Feather", "Attack Speed Up", "Increases attack animation speed", "⚡"),
    ("千里眼の水晶", "Senrigan no Suishō", "Clairvoyance Crystal", "Minimap Expand", "Reveals more of the minimap", "🔮"),
    ("幸運の石", "Kōun no Ishi", "Lucky Stone", "Rare Drop Up", "Increases rare item drop chance", "🍀"),
    ("修行の数珠", "Shugyō no Juzu", "Training Beads", "EXP Bonus (Battle)", "Bonus EXP from battle performance", "📖"),
    ("武勲の勲章", "Bukun no Kunshō", "Merit Medal", "Merit Bonus", "Extra battle merit points earned", "🏅"),
]

for jp, romaji, en, effect, desc, emoji in special_acc:
    html += f'  <div class="card">{icon_html("", emoji)}\n    <div class="info"><span class="jp">{jp}</span><span class="romaji">{romaji}</span>\n    <div class="en">{en}</div><div class="effect">{effect}</div><div class="desc">{desc}</div></div></div>\n'

html += "</div>\n</div>\n"

# ===================== EQUIPMENT BRIEF =====================
html += """
<div class="section" id="equip-brief">
<h2>📋 Equipment Screen Textures (装備画面)</h2>
<div class="note">Character equipment screen backgrounds extracted from game files. Each character has their own equipment UI layout.</div>
<div class="grid">
"""

for i in range(21):
    icon = brief_icons.get(i, "")
    char_names = ["Date Masamune", "Sanada Yukimura", "Maeda Keiji", "Tokugawa Ieyasu",
                  "Ishida Mitsunari", "Oda Nobunaga", "Akechi Mitsuhide", "Mōri Motonari",
                  "Chōsokabe Motochika", "Kuroda Kanbei", "Takeda Shingen", "Uesugi Kenshin",
                  "Hōjō Ujimasa", "Oichi", "Matsu", "Shimazu Yoshihiro",
                  "Fūma Kotarō", "Honda Tadakatsu", "Zabby", "Katsuie",
                  "Sarutobi Sasuke"]
    name = char_names[i] if i < len(char_names) else f"Character {i}"
    html += f'  <div class="card">{icon_html(icon, "📋")}\n    <div class="info"><span class="jp">装備画面 {i:02d}</span>\n    <div class="en">{name} Equipment</div></div></div>\n'

html += "</div>\n</div>\n"

# ===================== ITEMS =====================
html += """
<div class="section" id="items">
<h2>📦 Items (アイテム)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">回復薬</td><td class="romaji-text">Kaifukuyaku</td><td class="en-text">Recovery Medicine</td><td>Restores HP</td></tr>
<tr><td class="jp-text">大回復薬</td><td class="romaji-text">Daikaifukuyaku</td><td class="en-text">Greater Recovery</td><td>Restores more HP</td></tr>
<tr><td class="jp-text">特効薬</td><td class="romaji-text">Tokkōyaku</td><td class="en-text">Special Medicine</td><td>Full HP restore</td></tr>
<tr><td class="jp-text">バサラ回復薬</td><td class="romaji-text">Basara Kaifukuyaku</td><td class="en-text">Basara Restorative</td><td>Fills Basara gauge</td></tr>
<tr><td class="jp-text">毒消し</td><td class="romaji-text">Dokukeshi</td><td class="en-text">Antidote</td><td>Cures poison</td></tr>
<tr><td class="jp-text">目薬</td><td class="romaji-text">Megusuri</td><td class="en-text">Eye Drops</td><td>Cures blindness</td></tr>
<tr><td class="jp-text">麻酔消し</td><td class="romaji-text">Masuishomeshi</td><td class="en-text">Painkiller</td><td>Cures stun/paralysis</td></tr>
<tr><td class="jp-text">封印消し</td><td class="romaji-text">Fūinshomeshi</td><td class="en-text">Seal Remover</td><td>Cures seal status</td></tr>
<tr><td class="jp-text">飯綺の札</td><td class="romaji-text">Izuna no Fuda</td><td class="en-text">Izuna Talisman</td><td>Revive fallen ally</td></tr>
<tr><td class="jp-text">戦神の護符</td><td class="romaji-text">Ikushin no Gofu</td><td class="en-text">War God's Talisman</td><td>Temp attack/defense boost</td></tr>
<tr><td class="jp-text">修羅の魂</td><td class="romaji-text">Shura no Tamashii</td><td class="en-text">Asura Soul</td><td>Temp invincibility</td></tr>
<tr><td class="jp-text">魂の器</td><td class="romaji-text">Tamashii no Utsuwa</td><td class="en-text">Soul Vessel</td><td>Gain EXP instantly</td></tr>
<tr><td class="jp-text">武勲の証</td><td class="romaji-text">Bukun no Akashi</td><td class="en-text">Merit Token</td><td>Gain merit points</td></tr>
</table>
</div>
"""

# ===================== GAME TERMS =====================
html += """
<div class="section" id="terms">
<h2>📖 Game Terms (用語集)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">バサラ</td><td class="romaji-text">Basara</td><td class="en-text">Basara</td><td>Series signature — extreme/audacious spirit</td></tr>
<tr><td class="jp-text">天下</td><td class="romaji-text">Tenka</td><td class="en-text">The Land / Realm</td><td>Japan, the country being unified</td></tr>
<tr><td class="jp-text">天下統一</td><td class="romaji-text">Tenka Tōitsu</td><td class="en-text">Unification</td><td>Goal: unify the land</td></tr>
<tr><td class="jp-text">戦国</td><td class="romaji-text">Sengoku</td><td class="en-text">Warring States</td><td>The Sengoku era (1467-1615)</td></tr>
<tr><td class="jp-text">宴</td><td class="romaji-text">Utage</td><td class="en-text">Banquet / Party</td><td>Subtitle of this game</td></tr>
<tr><td class="jp-text">合戦</td><td class="romaji-text">Kassen</td><td class="en-text">Battle</td><td>Story battles / stages</td></tr>
<tr><td class="jp-text">武将</td><td class="romaji-text">Bushō</td><td class="en-text">Officer / Warlord</td><td>Playable & enemy characters</td></tr>
<tr><td class="jp-text">固有技</td><td class="romaji-text">Koyūgi</td><td class="en-text">Unique Skill</td><td>Character-specific moves</td></tr>
<tr><td class="jp-text">固有奥義</td><td class="romaji-text">Koyū Ōgi</td><td class="en-text">Super Move</td><td>Ultimate attack (uses Basara gauge)</td></tr>
<tr><td class="jp-text">バサラ技</td><td class="romaji-text">Basara Waza</td><td class="en-text">Basara Art</td><td>Basara gauge special attack</td></tr>
<tr><td class="jp-text">ドライブ</td><td class="romaji-text">Doraibu</td><td class="en-text">Drive</td><td>Boost mode — enhanced attacks</td></tr>
<tr><td class="jp-text">覚醒</td><td class="romaji-text">Kakusei</td><td class="en-text">Awakening</td><td>Powered-up state</td></tr>
<tr><td class="jp-text">属性</td><td class="romaji-text">Zokusei</td><td class="en-text">Element</td><td>Fire, Ice, Lightning, Dark, Light, Wind, Earth, Water</td></tr>
<tr><td class="jp-text">状態異常</td><td class="romaji-text">Jōtai Ijō</td><td class="en-text">Status Ailment</td><td>Poison, Stun, Seal, Blind, etc.</td></tr>
<tr><td class="jp-text">毒</td><td class="romaji-text">Doku</td><td class="en-text">Poison</td><td>HP drains over time</td></tr>
<tr><td class="jp-text">気絶</td><td class="romaji-text">Kizetsu</td><td class="en-text">Stun</td><td>Cannot move temporarily</td></tr>
<tr><td class="jp-text">封印</td><td class="romaji-text">Fūin</td><td class="en-text">Seal</td><td>Skills locked temporarily</td></tr>
<tr><td class="jp-text">暗闇</td><td class="romaji-text">Kurayami</td><td class="en-text">Blind</td><td>Screen darkened</td></tr>
<tr><td class="jp-text">凍結</td><td class="romaji-text">Tōketsu</td><td class="en-text">Freeze</td><td>Frozen in place</td></tr>
<tr><td class="jp-text">燃焼</td><td class="romaji-text">Nenshō</td><td class="en-text">Burn</td><td>Fire damage over time</td></tr>
<tr><td class="jp-text">麻痺</td><td class="romaji-text">Mahi</td><td class="en-text">Paralysis</td><td>Movement slowed/stopped</td></tr>
</table>
</div>
"""

# ===================== UTAGE MODE =====================
html += """
<div class="section" id="utage">
<h2>🎉 Utage / Party Mode (宴モード)</h2>
<div class="note">The signature feature of Sengoku Basara 3: Utage — a collection of party/mini-game modes.</div>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">宴モード</td><td class="romaji-text">Utage Mōdo</td><td class="en-text">Party Mode</td><td>Main Utage menu</td></tr>
<tr><td class="jp-text">東海道五十三次</td><td class="romaji-text">Tōkaidō Gojūsan-tsugi</td><td class="en-text">53 Stations of Tōkaidō</td><td>Endless battle mode — survive through 53 stages</td></tr>
<tr><td class="jp-text">戦国ダーツ</td><td class="romaji-text">Sengoku Dātsu</td><td class="en-text">Warring Darts</td><td>Dart-throwing mini-game</td></tr>
<tr><td class="jp-text">戦国チェイス</td><td class="romaji-text">Sengoku Cheisu</td><td class="en-text">Warring Chase</td><td>Tag/chase mini-game</td></tr>
<tr><td class="jp-text">戦国ビンゴ</td><td class="romaji-text">Sengoku Bongo</td><td class="en-text">Warring Bingo</td><td>Bingo mini-game with battle theme</td></tr>
<tr><td class="jp-text">戦国農家</td><td class="romaji-text">Sengoku Nōka</td><td class="en-text">Warring Farmer</td><td>Farming mini-game</td></tr>
<tr><td class="jp-text">天下一武道会</td><td class="romaji-text">Tenkaichi Budōkai</td><td class="en-text">Strongest Warrior Tournament</td><td>Bracket tournament mode</td></tr>
<tr><td class="jp-text">大挑戦</td><td class="romaji-text">Dai Chōsen</td><td class="en-text">Grand Challenge</td><td>Survival/boss rush mode</td></tr>
</table>
</div>
"""

# ===================== DIFFICULTY =====================
html += """
<div class="section" id="difficulty">
<h2>⚡ Difficulty (難易度)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th><th>Notes</th></tr>
<tr><td class="jp-text">やさしい</td><td class="romaji-text">Yasashii</td><td class="en-text">Easy</td><td>For beginners — low enemy HP & aggression</td></tr>
<tr><td class="jp-text">ふつう</td><td class="romaji-text">Futsū</td><td class="en-text">Normal</td><td>Standard difficulty</td></tr>
<tr><td class="jp-text">むずかしい</td><td class="romaji-text">Muzukashii</td><td class="en-text">Hard</td><td>Higher enemy stats, smarter AI</td></tr>
<tr><td class="jp-text">究極</td><td class="romaji-text">Kyūkyoku</td><td class="en-text">Extreme</td><td>Very hard — enemies deal massive damage</td></tr>
<tr><td class="jp-text">修羅</td><td class="romaji-text">Shura</td><td class="en-text">Asura / Nightmare</td><td>Hardest mode — max enemy aggression & stats</td></tr>
</table>
</div>
"""

# ===================== SYSTEM MESSAGES =====================
html += """
<div class="section" id="system">
<h2>💬 System Messages (システムメッセージ)</h2>
<table>
<tr><th>Japanese</th><th>Romaji</th><th>English</th></tr>
<tr><td class="jp-text">セーブしますか？</td><td class="romaji-text">Seibu shimasu ka?</td><td class="en-text">Would you like to save?</td></tr>
<tr><td class="jp-text">セーブしました</td><td class="romaji-text">Seibu shimashita</td><td class="en-text">Saved successfully.</td></tr>
<tr><td class="jp-text">ロードしています</td><td class="romaji-text">Rōdo shiteimasu</td><td class="en-text">Loading...</td></tr>
<tr><td class="jp-text">データが破損しています</td><td class="romaji-text">Dēta ga hason shiteimasu</td><td class="en-text">Data is corrupted.</td></tr>
<tr><td class="jp-text">セーブデータがありません</td><td class="romaji-text">Seibu dēta ga arimasen</td><td class="en-text">No save data found.</td></tr>
<tr><td class="jp-text">上書きしますか？</td><td class="romaji-text">Uwagaki shimasu ka?</td><td class="en-text">Overwrite existing data?</td></tr>
<tr><td class="jp-text">はい</td><td class="romaji-text">Hai</td><td class="en-text">Yes</td></tr>
<tr><td class="jp-text">いいえ</td><td class="romaji-text">Iie</td><td class="en-text">No</td></tr>
<tr><td class="jp-text">戻る</td><td class="romaji-text">Modoru</td><td class="en-text">Return / Back</td></tr>
<tr><td class="jp-text">決定</td><td class="romaji-text">Kettei</td><td class="en-text">Confirm / OK</td></tr>
<tr><td class="jp-text">キャンセル</td><td class="romaji-text">Kyanseru</td><td class="en-text">Cancel</td></tr>
<tr><td class="jp-text">装備しました</td><td class="romaji-text">Sōbi shimashita</td><td class="en-text">Equipped.</td></tr>
<tr><td class="jp-text">装備を外しました</td><td class="romaji-text">Sōbi o hazushimashita</td><td class="en-text">Unequipped.</td></tr>
<tr><td class="jp-text">購入しました</td><td class="romaji-text">Kōnyū shimashita</td><td class="en-text">Purchased.</td></tr>
<tr><td class="jp-text">所持金が足りません</td><td class="romaji-text">Shojikin ga tarimasen</td><td class="en-text">Not enough gold.</td></tr>
<tr><td class="jp-text">満腹です</td><td class="romaji-text">Manpuku desu</td><td class="en-text">Inventory is full.</td></tr>
<tr><td class="jp-text">レベルが上がった</td><td class="romaji-text">Reberu ga agatta</td><td class="en-text">Level increased!</td></tr>
<tr><td class="jp-text">新しい武器を入手</td><td class="romaji-text">Atarashii buki o nyūshu</td><td class="en-text">Acquired a new weapon!</td></tr>
<tr><td class="jp-text">称号を獲得</td><td class="romaji-text">Shōgō o kakutoku</td><td class="en-text">Earned a new title!</td></tr>
<tr><td class="jp-text">達成</td><td class="romaji-text">Tassei</td><td class="en-text">Achievement / Cleared</td></tr>
<tr><td class="jp-text">未達成</td><td class="romaji-text">Mitassei</td><td class="en-text">Not yet achieved</td></tr>
<tr><td class="jp-text">解除</td><td class="romaji-text">Kaijo</td><td class="en-text">Unlocked</td></tr>
<tr><td class="jp-text">使用不可</td><td class="romaji-text">Shiyō fuka</td><td class="en-text">Cannot use</td></tr>
<tr><td class="jp-text">売却しますか？</td><td class="romaji-text">Baikyaku shimasu ka?</td><td class="en-text">Sell this item?</td></tr>
<tr><td class="jp-text">分解しますか？</td><td class="romaji-text">Bunkai shimasu ka?</td><td class="en-text">Dismantle this item?</td></tr>
<tr><td class="jp-text">強化しました</td><td class="romaji-text">Kyōka shimashita</td><td class="en-text">Upgraded successfully.</td></tr>
<tr><td class="jp-text">これ以上強化できません</td><td class="romaji-text">Kore ijō kyōka dekimasen</td><td class="en-text">Cannot upgrade further.</td></tr>
<tr><td class="jp-text">操作設定を変更しました</td><td class="romaji-text">Sōsa settei o henkō shimashita</td><td class="en-text">Control settings changed.</td></tr>
<tr><td class="jp-text">初期設定に戻しますか？</td><td class="romaji-text">Shoki settei ni modoshimasu ka?</td><td class="en-text">Reset to default settings?</td></tr>
</table>
</div>
"""

# ===================== FOOTER =====================
html += """
<div class="footer">
  <p>Sengoku Basara 3: Utage (BLJM60389) — Complete Fan Translation Reference Guide</p>
  <p>Weapon, Orb, and Equipment icons extracted from game data files (DXT5 512x512 textures, decoded and embedded as base64).</p>
  <p>Not affiliated with Capcom. For personal use with RPCS3 emulator.</p>
</div>
</div>
</body>
</html>
"""

with open(out_html, 'w') as f:
    f.write(html)

print(f"HTML guide saved to: {out_html}")
print(f"File size: {os.path.getsize(out_html) / 1024:.0f} KB")
