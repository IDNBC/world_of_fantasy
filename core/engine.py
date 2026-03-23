import random
import math

class Area:
    def __init__(self, name, struct, life, control):
        self.name = name
        self.struct = struct   # 構造（数学）
        self.life = life       # 生命（生物）
        self.control = control # 制御（物理）

        # 基本ステータス
        self.difficulty = (struct * 0.7) + (life * 0.3)
        self.reward_base = math.log(struct + 2) * life * 10
        self.max_durability = 3 + control
        self.durability = self.max_durability
        
        self.time_required = 30 * (2 + struct * 0.5)
        self.timer = 0
        self.is_exploring = False
        self.last_event = "NONE" # 最後に起きたイベント名

    def start_explore(self):
        if self.durability > 0:
            self.is_exploring = True
            self.timer = self.time_required
            self.last_event = "ENTERING..."

    def update(self, player):
        if not self.is_exploring:
            return None

        self.timer -= 1
        
        # 探索の途中でイベントテキストを更新（雰囲気作り）
        if self.timer == int(self.time_required * 0.7):
            self.last_event = "SEARCHING..."
        elif self.timer == int(self.time_required * 0.3):
            self.last_event = "ENCOUNTER!"

        if self.timer <= 0:
            self.is_exploring = False
            self.durability -= 1
            return self.resolve_exploration(player)
        return None

    def resolve_exploration(self, player):
        roll = random.random()
        
        # スキル「survival」による戦闘力補正
        survival_bonus = player.skills["survival"] * 2
        # スキル「greed」による報酬補正
        greed_multiplier = 1.0 + (player.skills["greed"] * 0.2)

        if roll < 0.4: # 戦闘
            self.last_event = "MONSTER BATTLE"
            power = player.level + (player.base_logic * 0.5) + survival_bonus
            if power >= self.difficulty:
                gold = int(self.reward_base * 1.5 * greed_multiplier)
                mat = random.randint(1, 3) if random.random() < 0.8 else 1 # 戦闘勝利で素材が出る確率を80%に
                return {"gold": gold, "exp": 20, "material": mat, "msg": "BATTLE WIN!"}
            else:
                return {"gold": int(self.reward_base * 0.3), "exp": 5, "material": 0, "msg": "BATTLE LOSS..."}
        
        elif roll < 0.7: # お宝
            self.last_event = "TREASURE FOUND"
            gold = int(self.reward_base * 2.0 * greed_multiplier)
            mat = random.randint(3, 8) # お宝からは素材が出やすい
            return {"gold": gold, "exp": 10, "material": mat, "msg": "JACKPOT!"}
        
        else:
            self.last_event = "ACCIDENT..."
            mat = 1 if random.random() < 0.3 else 0
            return {"gold": int(self.reward_base * 0.2), "exp": 2, "material": mat, "msg": "TRAPPED!"}