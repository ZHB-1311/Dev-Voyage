# backend/src/backend/config.py
"""
功能配置中心
所有可开关的功能都在这里统一管理
"""

# 功能开关
FEATURES = {
    "comment": True,      # 评论功能（本章实现）
    "like": True,        # 点赞功能（练习题）
    "favorite": False,    # 收藏功能（练习题）
}


def is_feature_enabled(feature_name: str) -> bool:
    """检查某个功能是否开启"""
    return FEATURES.get(feature_name, False)


def get_all_features() -> dict:
    """获取所有功能的状态"""
    return FEATURES.copy()