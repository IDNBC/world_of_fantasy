# 修正後の models.py イメージ
class Equipment:
    def __init__(self, name, category, power=0, cost_m=0):
        self.name = name
        self.category = category
        self.power = power
        self.cost_m = cost_m

class Recipe:
    def __init__(self, name, target_item, material_cost, required_level=1):
        self.name = name
        self.target_item = target_item
        self.material_cost = material_cost
        self.required_level = required_level

class ItemDatabase:
    # 装備データ（一箇所にまとめる）
    EQUIPMENTS = {
        "WOODEN_STAFF": Equipment("木の杖", "WEAPON", power=2),
        "IRON_SWORD":   Equipment("鉄の剣", "WEAPON", power=5),
        "CLOTH_CLOAK":  Equipment("布の服", "ARMOR"),
        "LEATHER_ARMOR": Equipment("革の鎧", "ARMOR", power=2),
    }
    
    # レシピデータ
    RECIPES = [
        Recipe("IRON SWORD", EQUIPMENTS["IRON_SWORD"], material_cost=15, required_level=1),
        Recipe("LEATHER ARMOR", EQUIPMENTS["LEATHER_ARMOR"], material_cost=10, required_level=2),
    ]


# core/models.py

class Job:
    def __init__(self, name, description, hp_bonus, atk_bonus, logic_bonus, is_initial=False):
        self.name = name
        self.description = description
        self.hp_bonus = hp_bonus      # 生存率への影響
        self.atk_bonus = atk_bonus    # 物理戦闘への影響
        self.logic_bonus = logic_bonus # 魔法/解析への影響
        self.is_initial = is_initial  # 最初から選べるか

class JobDatabase:
    JOBS = {
        "WARRIOR": Job("WARRIOR", "High ATK and HP.", hp_bonus=5, atk_bonus=3, logic_bonus=0, is_initial=True),
        "MAGE":    Job("MAGE", "High LOGIC bonus.", hp_bonus=1, atk_bonus=0, logic_bonus=5, is_initial=True),
        "THIEF":   Job("THIEF", "Balanced and lucky.", hp_bonus=2, atk_bonus=1, logic_bonus=2, is_initial=True),
        "PALADIN": Job("PALADIN", "Holy Knight (Locked).", hp_bonus=10, atk_bonus=5, logic_bonus=3, is_initial=False),
    }