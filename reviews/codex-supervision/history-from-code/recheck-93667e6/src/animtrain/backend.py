"""训练后端适配器契约(msg_195,纯标准库,零依赖)。

未来可接 LLaMAFactory / Unsloth / 其他后端;当前阶段只定义接口契约,
**任何实现必须在用户批准模型与训练路线后接入**——默认一律
NOT_APPROVED,不得下载模型、安装依赖或启动训练。
"""
from __future__ import annotations

from dataclasses import dataclass

# 当前阶段允许的状态值;训练真实执行前一律 NOT_APPROVED
STATUS_NOT_APPROVED = "NOT_APPROVED"
STATUS_NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
STATUS_PREPARED = "PREPARED"
ALLOWED_STATUS = {STATUS_NOT_APPROVED, STATUS_NOT_IMPLEMENTED, STATUS_PREPARED}


class BackendNotApproved(RuntimeError):
    """后端操作在未批准阶段被调用的统一异常。

    契约:任何 load/train/save/evaluate 在用户批准前必须抛此异常,
    不得静默空转或假装成功。
    """


@dataclass
class TrainResult:
    """训练/评测入口的契约返回值骨架。

    当前阶段只允许 status ∈ {NOT_APPROVED, NOT_IMPLEMENTED, PREPARED};
    未来实现后才允许 success 类状态。
    """
    status: str = STATUS_NOT_APPROVED
    message: str = "训练后端未批准:需用户确认模型/训练路线后方可接入实现"
    run_id: str = ""


class TrainingBackend:
    """后端适配器契约(load/train/save/evaluate)。

    所有方法默认抛 BackendNotApproved;子类(未来实现)须保持同一签名
    并先通过用户批准门禁。不在此模块绑定任何真实后端或依赖。
    """
    name = "base"

    def load_model(self, config: dict) -> str:
        """加载模型:contract 入口。未批准阶段必须抛 BackendNotApproved。"""
        raise BackendNotApproved(
            f"{self.name}: load_model 未批准——不下载模型、不安装依赖;"
            "需用户批准模型/训练路线后方可接入实现")

    def train(self, config: dict, data_manifest: str) -> TrainResult:
        """训练:contract 入口。未批准阶段必须抛 BackendNotApproved。"""
        raise BackendNotApproved(
            f"{self.name}: train 未批准——不启动训练;"
            "需用户批准 + preflight --ready 通过后方可接入实现")

    def save_checkpoint(self, run_id: str, output_dir: str) -> str:
        """保存 checkpoint:contract 入口。未批准阶段必须抛 BackendNotApproved。"""
        raise BackendNotApproved(
            f"{self.name}: save_checkpoint 未批准")

    def evaluate(self, config: dict, eval_manifest: str) -> TrainResult:
        """评测:contract 入口。未批准阶段必须抛 BackendNotApproved;
        eval/test 独立生成并冻结前不得调用。"""
        raise BackendNotApproved(
            f"{self.name}: evaluate 未批准——eval/test 未独立生成并冻结")


# 未来后端注册表占位:名字保留,实现一律 stub(未批准)
_REGISTRY: dict[str, type[TrainingBackend]] = {}


def register_backend(name: str, cls: type[TrainingBackend]) -> None:
    """注册后端实现(未来接入时使用;当前不注册任何真实实现)。"""
    _REGISTRY[name] = cls


def get_backend(name: str) -> TrainingBackend:
    """按名取后端。未注册/未批准 → 返回默认契约后端(全部操作抛
    BackendNotApproved),绝不静默返回假实现。"""
    cls = _REGISTRY.get(name)
    if cls is None:
        return TrainingBackend()  # base:全操作 NOT_APPROVED
    return cls()
