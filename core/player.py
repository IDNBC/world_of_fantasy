from core.models import JobDatabase

class Player:
    def __init__(self):
        self.gold = 500
        self.material = 0  # ← ここが抜けていたためクラッシュしていました
        self.level = 1
        self.exp = 0 # レベルアップテストするときは95などにする
        self.next_exp = 100
        # player.py の __init__ に追加
        self.weapon = None
        self.armor = None
        self.current_job = "WARRIOR"
        self.unlocked_jobs = ["WARRIOR", "MAGE", "THIEF"]

        # # ジョブごとの経験値とレベル管理 {ジョブ名: レベル}
        # self.job_levels = {name: 1 for name in self.job_database_keys()}
        # self.job_exp = {name: 0 for name in self.job_database_keys()}

        # 修正：Playerのメソッドではなく、JobDatabaseから直接キー（職業名）を取得する
        self.job_levels = {name: 1 for name in JobDatabase.JOBS.keys()}
        self.job_exp = {name: 0 for name in JobDatabase.JOBS.keys()}

        # 【新規】スキルツリー（簡易版）
        self.skill_points = 0
        self.skills = {
            "analysis": 0,  # 構造解析：エリア生成にボーナス
            "survival": 0,  # 生存術：戦闘勝利確率・事故回避
            "crafting": 0 # 新設：製作スキル
        }
        
        # 基礎能力（将来的にスキルポイントで振り分け可能にする）
        self.base_logic = 1    # 構造への理解
        self.base_economy = 1  # 市場への理解

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.next_exp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.next_exp
        self.next_exp = int(self.next_exp * 1.2)
        self.skill_points += 1  # レベルアップでポイント付与
        # レベルアップ時に少し能力が上がる
        self.base_logic += 1 
        return True
    
    def get_job_stats(self):
        """現在のジョブとレベルに基づいたボーナスを計算"""
        job = JobDatabase.JOBS[self.current_job]
        lv = self.job_levels[self.current_job]
        return {
            "hp": job.hp_bonus * lv,
            "atk": job.atk_bonus * lv,
            "logic": job.logic_bonus * lv
        }

    def gain_job_exp(self, amount):
        """現在のジョブに経験値を加算"""
        self.job_exp[self.current_job] += amount
        # レベルアップ判定 (例: 次のレベルまで 100固定、あるいはスケーリング)
        if self.job_exp[self.current_job] >= 100:
            self.job_levels[self.current_job] += 1
            self.job_exp[self.current_job] = 0
            return True # レベルアップ通知用
        return False

    # 補助メソッド
    def get_total_logic(self, town):
        # スキル「analysis」を構造計算に接続
        return self.base_logic + town.get_logic_bonus() + self.skills["analysis"]

    def get_total_economy(self, town):
        return self.base_economy + town.get_economy_bonus()
    
    # core/player.py 内に追加
    def equip(self, item):
        if item.category == "WEAPON":
            self.weapon = item
        elif item.category == "ARMOR":
            self.armor = item

    def can_craft(self, recipe):
    # 製作可能かチェック
        return (self.material >= recipe.material_cost and 
            self.skills["crafting"] >= recipe.required_level)