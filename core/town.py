class Town:
    def __init__(self):
        # 施設レベル（初期値1）
        self.facilities = {
            "school": 1,  # 数学・論理（構造に影響）
            "market": 1,  # 経済・交渉（報酬に影響）
            "lab": 1,      # 物理・化学（将来の拡張用）
            "workshop": 1  # 製作（クラフトに影響）
        }

    def get_logic_bonus(self):
        # 学校レベルが上がるほどLogicボーナスが増える
        return self.facilities["school"]

    def get_economy_bonus(self):
        # 市場レベルが上がるほど報酬倍率が増える
        return self.facilities["market"] * 0.1 # レベル1ごとに+10%
    
    def get_craft_bonus(self):
    # 工房レベルに応じて、製作時の素材消費を抑えるなどのボーナス
        return self.facilities["workshop"] * 0.05

    def get_upgrade_cost(self, f_name):
        # レベルが上がるほどコストが増える計算式
        return 100 * (self.facilities[f_name] ** 2)

    def upgrade(self, f_name, player):
        gold_cost = self.get_upgrade_cost(f_name)
        mat_cost = self.facilities[f_name] * 2  # レベル1→2で2個、2→3で4個...
        
        if player.gold >= gold_cost and player.material >= mat_cost:
            player.gold -= gold_cost
            player.material -= mat_cost
            self.facilities[f_name] += 1
            return True
        return False