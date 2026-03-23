import pyxel
import random
from core.engine import Area
from core.player import Player
from core.town import Town

class App:
    def __init__(self):
        pyxel.init(160, 120, title="World of Fantasy")
        self.player = Player()
        self.town = Town()
        self.state = "TOWN"
        self.current_area = None
        self.msg = "WELCOME"
        pyxel.run(self.update, self.draw)

    def update(self):
        # 画面切り替え
        if pyxel.btnp(pyxel.KEY_1): self.state = "TOWN"
        if pyxel.btnp(pyxel.KEY_2): self.state = "CREATE"
        if pyxel.btnp(pyxel.KEY_3) and self.current_area: self.state = "EXPLORE"

        # 各画面のメインロジック
        if self.state == "TOWN":
            self.update_town()
        elif self.state == "CREATE":
            self.update_create()
        elif self.state == "EXPLORE":
            self.update_explore()

    def update_town(self):
        # 1. 内部関数の定義
        def try_upgrade(f_name, label):
            g_cost = self.town.get_upgrade_cost(f_name)
            m_cost = self.town.facilities[f_name] * 2
            
            if self.player.gold < g_cost:
                self.msg = f"NEED {g_cost}G"
            elif self.player.material < m_cost:
                self.msg = f"NEED {m_cost}M (MATERIAL)"
            else:
                if self.town.upgrade(f_name, self.player):
                    self.msg = f"{label} UPGRADED!"

        # 2. 【重要】定義した関数をここで呼び出す
        if pyxel.btnp(pyxel.KEY_S):
            try_upgrade("school", "SCHOOL")
        if pyxel.btnp(pyxel.KEY_M):
            try_upgrade("market", "MARKET")
        
        # スキル振り分け（ここは今のままでOK）
        if self.player.skill_points > 0:
            if pyxel.btnp(pyxel.KEY_Z):
                self.player.skills["analysis"] += 1
                self.player.skill_points -= 1
                self.msg = "ANALYSIS UP!"
            # ... X, C も同様に ...
        
        # スキル振り分け（新規：ポイントがある時のみ）
        if self.player.skill_points > 0:
            if pyxel.btnp(pyxel.KEY_Z): # Analysis
                self.player.skills["analysis"] += 1
                self.player.skill_points -= 1
            if pyxel.btnp(pyxel.KEY_X): # Survival
                self.player.skills["survival"] += 1
                self.player.skill_points -= 1
            if pyxel.btnp(pyxel.KEY_C): # Greed
                self.player.skills["greed"] += 1
                self.player.skill_points -= 1

    def update_create(self):
        if pyxel.btnp(pyxel.KEY_A):
            # 街の恩恵を受けたLogicでエリア生成
            logic = self.player.get_total_logic(self.town)
            # engine.py側の引数が (name, struct, life, control) であることを確認
            self.current_area = Area("RUIN", logic, 2, 2)
            self.msg = f"CREATED (LOGIC:{logic})"

    def update_explore(self):
        if not self.current_area: return

        # 探索開始
        if pyxel.btnp(pyxel.KEY_E) and not self.current_area.is_exploring:
            if self.current_area.durability > 0:
                self.current_area.start_explore()
        
        # 探索中・完了の更新
        # res = self.current_area.update(self.player.level)
        res = self.current_area.update(self.player)
        
        # 探索が完了した瞬間のみ実行される
        if res is not None:
            bonus = self.player.get_total_economy(self.town)
            final_gold = int(res["gold"] * (1 + bonus))
            
            self.player.gold += final_gold
            self.player.gain_exp(res["exp"])
            
            # 【ここを追加】素材をプレイヤーに渡す
            obtained_mat = res.get("material", 0)
            self.player.material += obtained_mat
            
            # メッセージも分かりやすく
            if obtained_mat > 0:
                self.msg = f"{res['msg']} (+{final_gold}G / +{obtained_mat}M)"
            else:
                self.msg = f"{res['msg']} (+{final_gold}G)"

    def draw(self):
        pyxel.cls(0)
        
        # ヘッダー (LV, Gold, Logic, EXPバー)
        pyxel.rect(0, 0, 160, 12, 1)
        exp_rate = min(1.0, self.player.exp / self.player.next_exp)
        pyxel.rect(0, 11, 160 * exp_rate, 1, 10) 
        
        # logic = self.player.get_total_logic(self.town)
        # pyxel.text(5, 3, f"LV:{self.player.level} G:{self.player.gold} LOGIC:{logic}", 7)

        s = f"LV:{self.player.level}  G:{self.player.gold}  M:{self.player.material}"
        pyxel.text(5, 3, s, 7)
        
        if self.state == "TOWN":
            self.draw_town()
        elif self.state == "CREATE":
            self.draw_create()
        elif self.state == "EXPLORE":
            self.draw_explore()

        # 下部メッセージ
        pyxel.text(5, 110, self.msg, 10)

    # def draw_town(self):
    #     pyxel.text(10, 30, "--- TOWN FACILITIES ---", 3)
    #     s_lv = self.town.facilities["school"]
    #     s_cost = self.town.get_upgrade_cost("school")
    #     pyxel.text(10, 50, f"[S] SCHOOL LV:{s_lv} (COST:{s_cost})", 7)
        
    #     m_lv = self.town.facilities["market"]
    #     m_cost = self.town.get_upgrade_cost("market")
    #     pyxel.text(10, 60, f"[M] MARKET LV:{m_lv} (COST:{m_cost})", 7)
    #     pyxel.text(10, 90, "1:TOWN  2:GUILD  3:GATE", 5)

    #     # (既存の施設表示は維持)
    #     pyxel.text(10, 80, f"--- SKILLS (PTS:{self.player.skill_points}) ---", 10)
    #     pyxel.text(10, 90, f"[Z] ANALYSIS (LV:{self.player.skills['analysis']})", 7)
    #     pyxel.text(10, 100, f"[X] SURVIVAL (LV:{self.player.skills['survival']})", 7)
    #     pyxel.text(10, 110, f"[C] GREED    (LV:{self.player.skills['greed']})", 7)

    def draw_town(self):
        # --- 左側：TOWN FACILITIES ---
        pyxel.text(10, 25, "- FACILITIES -", 3)
        
        s_lv = self.town.facilities["school"]
        s_cost = self.town.get_upgrade_cost("school")
        pyxel.text(10, 40, f"[S] SCHOOL", 7)
        pyxel.text(10, 48, f"    LV:{s_lv} C:{s_cost}", 13)
        
        m_lv = self.town.facilities["market"]
        m_cost = self.town.get_upgrade_cost("market")
        pyxel.text(10, 60, f"[M] MARKET", 7)
        pyxel.text(10, 68, f"    LV:{m_lv} C:{m_cost}", 13)
        
        # --- 右側：SKILLS ---
        pyxel.text(90, 25, "- SKILLS -", 10)
        pyxel.text(90, 33, f" POINTS: {self.player.skill_points}", 6)
        
        skills = [
            ("Z", "ANALYSIS", "analysis"),
            ("X", "SURVIVAL", "survival"),
            ("C", "GREED", "greed")
        ]
        
        for i, (key, name, s_key) in enumerate(skills):
            y_pos = 45 + (i * 18)
            col = 7 if self.player.skill_points > 0 else 12
            pyxel.text(90, y_pos, f"[{key}] {name}", col)
            pyxel.text(90, y_pos + 8, f"    LV: {self.player.skills[s_key]}", 13)

        # 下部操作ガイド
        pyxel.rect(0, 100, 160, 1, 1)
        pyxel.text(15, 103, "1:TOWN   2:GUILD   3:GATE", 5)

    def draw_create(self):
        pyxel.text(10, 30, "--- ADVENTURER GUILD ---", 14)
        pyxel.text(10, 50, "[A] CREATE NEW AREA", 7)
        if self.current_area:
            pyxel.text(10, 70, f"READY: {self.current_area.name}", 11)
            pyxel.text(10, 80, f"DURABILITY: {self.current_area.durability}", 7)

    def draw_explore(self):
        if not self.current_area:
            pyxel.text(10, 50, "NO AREA SELECTED", 7)
            return
            
        a = self.current_area
        pyxel.text(10, 30, f"AREA: {a.name}", 11)
        pyxel.text(10, 40, f"STATUS: {a.last_event}", 7) # イベント表示
        pyxel.text(10, 50, f"DURABILITY: {'*' * a.durability}", 14)
        
        if a.is_exploring:
            progress = (a.time_required - a.timer) / a.time_required
            pyxel.rect(10, 60, 140, 4, 13)
            pyxel.rect(10, 60, 140 * progress, 4, 11)
            pyxel.text(10, 70, "EXPLORING...", 7)
        else:
            if a.durability > 0:
                pyxel.text(10, 60, "PRESS [E] TO EXPLORE", 6)
            else:
                pyxel.text(10, 60, "AREA COLLAPSED", 8)

App()