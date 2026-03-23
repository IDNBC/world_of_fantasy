class Player:
    def __init__(self):
        self.gold = 500
        self.material = 0  # ← ここが抜けていたためクラッシュしていました
        self.level = 1
        self.exp = 0
        self.next_exp = 100

        # 【新規】スキルツリー（簡易版）
        self.skill_points = 0
        self.skills = {
            "analysis": 0,  # 構造解析：エリア生成にボーナス
            "survival": 0,  # 生存術：戦闘勝利確率・事故回避
            "greed": 0      # 強欲：獲得ゴールド・素材UP
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

    # def get_total_logic(self, town):
    #     return self.base_logic + town.get_logic_bonus()

    # def get_total_economy(self, town):
    #     return self.base_economy + town.get_economy_bonus()
    
    # 補助メソッド
    def get_total_logic(self, town):
        # スキル「analysis」を構造計算に接続
        return self.base_logic + town.get_logic_bonus() + self.skills["analysis"]

    def get_total_economy(self, town):
        return self.base_economy + town.get_economy_bonus()